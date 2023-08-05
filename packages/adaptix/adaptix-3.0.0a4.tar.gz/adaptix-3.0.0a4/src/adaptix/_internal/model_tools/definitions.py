# pylint: disable=invalid-overridden-method,arguments-differ
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, FrozenSet, Generic, Hashable, Mapping, Optional, TypeVar, Union

from ..common import Catchable, TypeHint, VarTuple
from ..struct_path import Attr, PathElement
from ..utils import SingletonMeta, pairs

T = TypeVar('T')


class NoDefault(metaclass=SingletonMeta):
    pass


@dataclass(frozen=True)
class DefaultValue(Generic[T]):
    value: T

    def __hash__(self):
        try:
            return hash(self.value)
        except TypeError:
            return 236  # some random number that fits in byte


@dataclass(frozen=True)
class DefaultFactory(Generic[T]):
    factory: Callable[[], T]


Default = Union[NoDefault, DefaultValue[T], DefaultFactory[T]]


class Accessor(Hashable, ABC):
    @property
    @abstractmethod
    def getter(self) -> Callable[[Any], Any]:
        ...

    @property
    @abstractmethod
    def access_error(self) -> Optional[Catchable]:
        ...

    @property
    @abstractmethod
    def path_element(self) -> PathElement:
        ...


class DescriptorAccessor(Accessor, ABC):
    def __init__(self, attr_name: str, access_error: Optional[Catchable]):
        self._attr_name = attr_name
        self._access_error = access_error

    # noinspection PyMethodOverriding
    def getter(self, obj):
        return getattr(obj, self._attr_name)

    @property
    def access_error(self) -> Optional[Catchable]:
        return self._access_error

    @property
    def path_element(self) -> PathElement:
        return Attr(self.attr_name)

    @property
    def attr_name(self) -> str:
        return self._attr_name

    def __eq__(self, other):
        if isinstance(other, DescriptorAccessor):
            return self._attr_name == other._attr_name and self._access_error == other._access_error
        return NotImplemented

    def __hash__(self):
        return hash((self._attr_name, self._access_error))

    def __repr__(self):
        return f"{type(self)}(attr_name={self.attr_name}, access_error={self.access_error})"


class AttrAccessor(DescriptorAccessor):
    def __init__(self, attr_name: str, is_required: bool):
        access_error = None if is_required else AttributeError
        super().__init__(attr_name, access_error)

    @property
    def is_required(self) -> bool:
        return self.access_error is None

    def __repr__(self):
        return f"{type(self).__name__}(attr_name={self.attr_name}, is_required={self.is_required})"


@dataclass(frozen=True)
class ItemAccessor(Accessor):
    item_name: str
    is_required: bool

    # noinspection PyMethodOverriding
    def getter(self, obj):
        return obj[self.item_name]

    @property
    def access_error(self) -> Optional[Catchable]:
        return None if self.is_required else KeyError

    @property
    def path_element(self) -> PathElement:
        return self.item_name

    def __hash__(self):
        return hash((self.item_name, self.is_required))


def is_valid_field_id(value: str) -> bool:
    return value.isidentifier()


@dataclass(frozen=True)
class BaseField:
    type: TypeHint
    id: str
    default: Default
    # Mapping almost never defines __hash__,
    # so it will be more convenient to exclude this field
    # from hash computation
    metadata: Mapping[Any, Any] = field(hash=False)

    def __post_init__(self):
        if not is_valid_field_id(self.id):
            raise ValueError(f"name of field must be python identifier, now it is a {self.id!r}")


class ParamKind(Enum):
    POS_ONLY = 0
    POS_OR_KW = 1
    KW_ONLY = 3  # 2 is for VAR_POS


@dataclass(frozen=True)
class InputField(BaseField):
    is_required: bool
    param_kind: ParamKind
    param_name: str

    @property
    def is_optional(self):
        return not self.is_required

    def __post_init__(self):
        super().__post_init__()
        if not self.param_name.isidentifier():
            raise ValueError(f"param_name must be python identifier, now it is a {self.param_name!r}")

        if self.param_kind == ParamKind.POS_ONLY and not self.is_required:
            raise ValueError(f"{type(self)} can not be positional only and optional")


@dataclass(frozen=True)
class OutputField(BaseField):
    accessor: Accessor

    @property
    def is_optional(self) -> bool:
        return not self.is_required

    @property
    def is_required(self) -> bool:
        return self.accessor.access_error is None


@dataclass(frozen=True)
class BaseShape:
    """Signature of class. Divided into 2 parts: input and output.
    See doc :class InputShape: and :class OutputShape: for more details
    """
    fields: VarTuple[BaseField]
    overriden_types: FrozenSet[str]
    fields_dict: Mapping[str, BaseField] = field(init=False, hash=False, repr=False, compare=False)

    def _validate(self):
        field_ids = {fld.id for fld in self.fields}
        if len(field_ids) != len(self.fields):
            duplicates = {
                fld.id for fld in self.fields
                if fld.id in field_ids
            }
            raise ValueError(f"Field names {duplicates} are duplicated")

        wild_overriden_types = self.overriden_types - field_ids
        if wild_overriden_types:
            raise ValueError(f"overriden_types contains non existing fields {wild_overriden_types} ")

    def __post_init__(self):
        self._validate()
        super().__setattr__('fields_dict', {fld.id: fld for fld in self.fields})


@dataclass(frozen=True)
class ParamKwargs:
    type: TypeHint


@dataclass(frozen=True)
class InputShape(BaseShape, Generic[T]):
    """Description of desired object creation

    :param constructor: callable that produces an instance of the class.
    :param fields: parameters of the constructor
    """
    fields: VarTuple[InputField]
    kwargs: Optional[ParamKwargs]
    constructor: Callable[..., T]
    fields_dict: Mapping[str, InputField] = field(init=False, hash=False, repr=False, compare=False)

    @property
    def allow_kwargs(self) -> bool:
        return self.kwargs is not None

    def _validate(self):
        super()._validate()

        param_names = {fld.param_name for fld in self.fields}
        if len(param_names) != len(self.fields):
            duplicates = {
                fld.param_name for fld in self.fields
                if fld.param_name in param_names
            }
            raise ValueError(f"Param names {duplicates} are duplicated")

        for past, current in pairs(self.fields):
            if past.param_kind.value > current.param_kind.value:
                raise ValueError(
                    f"Inconsistent order of fields,"
                    f" {current.param_kind} must be after {past.param_kind}"
                )

            if (
                past.is_optional
                and current.is_required
                and current.param_kind != ParamKind.KW_ONLY
            ):
                raise ValueError(
                    f"All not required fields must be after required ones"
                    f" except {ParamKind.KW_ONLY} fields"
                )


@dataclass(frozen=True)
class OutputShape(BaseShape):
    """Description of extraction data from an object

    :param fields: fields (can be not only attributes) of object
    """
    fields: VarTuple[OutputField]
    fields_dict: Mapping[str, OutputField] = field(init=False, hash=False, repr=False, compare=False)


Inp = TypeVar('Inp', bound=Optional[InputShape])
Out = TypeVar('Out', bound=Optional[OutputShape])


@dataclass
class Shape(Generic[Inp, Out]):
    input: Inp
    output: Out


FullShape = Shape[InputShape, OutputShape]
ShapeIntrospector = Callable[[Any], Shape]


class IntrospectionImpossible(Exception):
    pass


class NoTargetPackage(IntrospectionImpossible):
    pass
