import inspect
import warnings
from dataclasses import MISSING as DC_MISSING, Field as DCField, fields as dc_fields, is_dataclass, replace
from inspect import Parameter, Signature
from types import MappingProxyType
from typing import Any, Dict

from ..feature_requirement import HAS_ATTRS_PKG, HAS_PY_39
from ..model_tools.definitions import (
    AttrAccessor,
    BaseField,
    Default,
    DefaultFactory,
    DefaultValue,
    FullShape,
    InputField,
    InputShape,
    IntrospectionImpossible,
    ItemAccessor,
    NoDefault,
    NoTargetPackage,
    OutputField,
    OutputShape,
    ParamKind,
    ParamKwargs,
    Shape,
)
from ..type_tools import get_all_type_hints, is_named_tuple_class, is_typed_dict_class

try:
    import attrs
except ImportError:
    attrs = None  # type: ignore[assignment]


# ======================
#       Function
# ======================

_PARAM_KIND_CONV: Dict[Any, ParamKind] = {
    Parameter.POSITIONAL_ONLY: ParamKind.POS_ONLY,
    Parameter.POSITIONAL_OR_KEYWORD: ParamKind.POS_OR_KW,
    Parameter.KEYWORD_ONLY: ParamKind.KW_ONLY,
}


def _is_empty(value):
    return value is Signature.empty


def get_callable_shape(func, params_slice=slice(0, None)) -> Shape[InputShape, None]:
    try:
        signature = inspect.signature(func)
    except TypeError:
        raise IntrospectionImpossible

    params = list(signature.parameters.values())[params_slice]
    kinds = [p.kind for p in params]

    if Parameter.VAR_POSITIONAL in kinds:
        raise IntrospectionImpossible(
            f'Can not create InputShape'
            f' from the function that has {Parameter.VAR_POSITIONAL}'
            f' parameter'
        )

    param_kwargs = next(
        (
            ParamKwargs(Any if _is_empty(param.annotation) else param.annotation)
            for param in params if param.kind == Parameter.VAR_KEYWORD
        ),
        None,
    )

    type_hints = get_all_type_hints(func)

    return Shape(
        input=InputShape(
            constructor=func,
            fields=tuple(
                InputField(
                    type=type_hints.get(param.name, Any),
                    id=param.name,
                    is_required=_is_empty(param.default) or param.kind == Parameter.POSITIONAL_ONLY,
                    default=NoDefault() if _is_empty(param.default) else DefaultValue(param.default),
                    metadata=MappingProxyType({}),
                    param_kind=_PARAM_KIND_CONV[param.kind],
                    param_name=param.name,
                )
                for param in params
                if param.kind != Parameter.VAR_KEYWORD
            ),
            kwargs=param_kwargs,
            overriden_types=frozenset(
                param.name
                for param in params
                if param.kind != Parameter.VAR_KEYWORD
            ),
        ),
        output=None,
    )


# ======================
#       NamedTuple
# ======================

def get_named_tuple_shape(tp) -> FullShape:
    # pylint: disable=protected-access
    if not is_named_tuple_class(tp):
        raise IntrospectionImpossible

    type_hints = get_all_type_hints(tp)
    if tuple in tp.__bases__:
        overriden_types = frozenset(tp._fields)
    else:
        overriden_types = frozenset(tp.__annotations__.keys() & set(tp._fields))

    # noinspection PyProtectedMember
    input_shape = InputShape(
        constructor=tp,
        kwargs=None,
        fields=tuple(
            InputField(
                id=field_id,
                type=type_hints.get(field_id, Any),
                default=(
                    DefaultValue(tp._field_defaults[field_id])
                    if field_id in tp._field_defaults else
                    NoDefault()
                ),
                is_required=field_id not in tp._field_defaults,
                param_name=field_id,
                metadata=MappingProxyType({}),
                param_kind=ParamKind.POS_OR_KW,
            )
            for field_id in tp._fields
        ),
        overriden_types=overriden_types,
    )

    return Shape(
        input=input_shape,
        output=OutputShape(
            fields=tuple(
                OutputField(
                    id=fld.id,
                    type=fld.type,
                    default=fld.default,
                    metadata=fld.metadata,
                    accessor=AttrAccessor(attr_name=fld.id, is_required=True),
                )
                for fld in input_shape.fields
            ),
            overriden_types=overriden_types,
        )
    )


# =====================
#       TypedDict
# =====================

class TypedDictAt38Warning(UserWarning):
    """Runtime introspection of TypedDict at python3.8 does not support inheritance.
    Please, update python or consider limitations suppressing this warning
    """

    def __str__(self):
        return (
            "Runtime introspection of TypedDict at python3.8 does not support inheritance."
            " Please, update python or consider limitations suppressing this warning"
        )


if HAS_PY_39:
    def _td_make_requirement_determinant(tp):
        required_fields = tp.__required_keys__
        return lambda name: name in required_fields
else:
    def _td_make_requirement_determinant(tp):
        warnings.warn(TypedDictAt38Warning(), stacklevel=3)
        is_total = tp.__total__
        return lambda name: is_total


def _get_td_hints(tp):
    elements = list(get_all_type_hints(tp).items())
    elements.sort(key=lambda v: v[0])
    return elements


def get_typed_dict_shape(tp) -> FullShape:
    # __annotations__ of TypedDict contains also parents type hints unlike any other classes,
    # so overriden_types always contains all fields
    if not is_typed_dict_class(tp):
        raise IntrospectionImpossible

    requirement_determinant = _td_make_requirement_determinant(tp)
    type_hints = _get_td_hints(tp)
    return Shape(
        input=InputShape(
            constructor=tp,
            fields=tuple(
                InputField(
                    type=tp,
                    id=name,
                    default=NoDefault(),
                    is_required=requirement_determinant(name),
                    metadata=MappingProxyType({}),
                    param_kind=ParamKind.KW_ONLY,
                    param_name=name,
                )
                for name, tp in type_hints
            ),
            kwargs=None,
            overriden_types=frozenset(tp.__annotations__.keys()),
        ),
        output=OutputShape(
            fields=tuple(
                OutputField(
                    type=tp,
                    id=name,
                    default=NoDefault(),
                    accessor=ItemAccessor(name, requirement_determinant(name)),
                    metadata=MappingProxyType({}),
                )
                for name, tp in type_hints
            ),
            overriden_types=frozenset(tp.__annotations__.keys()),
        ),
    )


# ======================
#       Dataclass
# ======================

def all_dc_fields(cls) -> Dict[str, DCField]:
    """Builtin introspection function hides
    some fields like InitVar or ClassVar.
    That function return full dict
    """
    return cls.__dataclass_fields__


def get_dc_default(field: DCField) -> Default:
    if field.default is not DC_MISSING:
        return DefaultValue(field.default)
    if field.default_factory is not DC_MISSING:
        return DefaultFactory(field.default_factory)
    return NoDefault()


def create_inp_field_from_dc_fields(dc_field: DCField, type_hints):
    default = get_dc_default(dc_field)
    return InputField(
        type=type_hints[dc_field.name],
        id=dc_field.name,
        default=default,
        is_required=default == NoDefault(),
        metadata=dc_field.metadata,
        param_kind=ParamKind.POS_OR_KW,
        param_name=dc_field.name,
    )


def get_dataclass_shape(tp) -> FullShape:
    """This function does not work properly if __init__ signature differs from
    that would be created by dataclass decorator.

    It happens because we can not distinguish __init__ that generated
    by @dataclass and __init__ that created by other ways.
    And we can not analyze only __init__ signature
    because @dataclass uses private constant
    as default value for fields with default_factory
    """

    if not is_dataclass(tp):
        raise IntrospectionImpossible

    name_to_dc_field = all_dc_fields(tp)
    dc_fields_public = dc_fields(tp)
    init_params = list(
        inspect.signature(tp.__init__).parameters.keys()
    )[1:]
    type_hints = get_all_type_hints(tp)

    return Shape(
        input=InputShape(
            constructor=tp,
            fields=tuple(
                create_inp_field_from_dc_fields(name_to_dc_field[field_id], type_hints)
                for field_id in init_params
            ),
            kwargs=None,
            overriden_types=frozenset(
                field_id for field_id in init_params
                if field_id in tp.__annotations__
            ),
        ),
        output=OutputShape(
            fields=tuple(
                OutputField(
                    type=type_hints[field.name],
                    id=field.name,
                    default=get_dc_default(name_to_dc_field[field.name]),
                    accessor=AttrAccessor(field.name, True),
                    metadata=field.metadata,
                )
                for field in dc_fields_public
            ),
            overriden_types=frozenset(
                field.name for field in dc_fields_public
                if field.name in tp.__annotations__
            ),
        )
    )


# ======================
#       ClassInit
# ======================

def get_class_init_shape(tp) -> Shape[InputShape, None]:
    if not isinstance(tp, type):
        raise IntrospectionImpossible

    shape = get_callable_shape(
        tp.__init__,  # type: ignore[misc]
        slice(1, None)
    )

    return replace(
        shape,
        input=replace(
            shape.input,
            constructor=tp,
        )
    )

# =================
#       Attrs
# =================


def _get_attrs_default(attrs_field) -> Default:
    default: Any = attrs_field.default

    if isinstance(default, attrs.Factory):  # type: ignore
        if default.takes_self:
            # TODO: add support
            raise ValueError("Factory with self parameter does not supported yet")
        return DefaultFactory(default.factory)

    if default is attrs.NOTHING:
        return NoDefault()

    return DefaultValue(default)


def _get_attrs_field_type(attrs_field, type_hints):
    try:
        return type_hints[attrs_field.name]
    except KeyError:
        return Any if attrs_field.type is None else attrs_field.type


NoneType = type(None)


def _process_attr_input_field(
    field: InputField,
    param_name_to_base_field: Dict[str, BaseField],
    has_custom_init: bool,
):
    try:
        base_field = param_name_to_base_field[field.id]
    except KeyError:
        return field

    # When input shape is generating we rely on __init__ signature,
    # but when field type is None attrs thinks that there is no type hint,
    # so if there is no custom __init__ (that can do not set type for this attribute),
    # we should use NoneType as type of field
    if not has_custom_init and field.type == Any and base_field.type == NoneType:
        field = replace(field, type=NoneType)

    return replace(
        field,
        default=(
            base_field.default
            if isinstance(field.default, DefaultValue) and field.default.value is attrs.NOTHING else
            field.default
        ),
        metadata=base_field.metadata,
        id=base_field.id,
    )


def _get_attrs_param_name(attrs_field):
    if hasattr(attrs_field, 'alias'):
        return attrs_field.alias
    return (
        attrs_field.name[1:]
        if attrs_field.name.startswith("_") and not attrs_field.name.startswith("__") else
        attrs_field.name
    )


def get_attrs_shape(tp) -> FullShape:
    if not HAS_ATTRS_PKG:
        raise NoTargetPackage

    try:
        is_attrs = attrs.has(tp)
    except TypeError:
        raise IntrospectionImpossible
    if not is_attrs:
        raise IntrospectionImpossible

    type_hints = get_all_type_hints(tp)

    try:
        attrs_fields = attrs.fields(tp)
    except (TypeError, attrs.exceptions.NotAnAttrsClassError):
        raise IntrospectionImpossible

    attrs_fields_dict = {
        field.name: field for field in attrs_fields
    }
    param_name_to_base_field = {
        _get_attrs_param_name(attrs_fld): BaseField(
            # if field is not annotated, type attribute will store None value
            type=_get_attrs_field_type(attrs_fld, type_hints),
            default=_get_attrs_default(attrs_fld),
            metadata=attrs_fld.metadata,
            id=attrs_fld.name,
        )
        for attrs_fld in attrs_fields
    }

    has_custom_init = hasattr(tp, '__attrs_init__')

    shape = get_class_init_shape(tp)
    input_fields = tuple(
        _process_attr_input_field(field, param_name_to_base_field, has_custom_init)
        for field in shape.input.fields
    )
    input_shape = replace(
        shape.input,
        fields=input_fields,
        overriden_types=frozenset(
            (fld.id for fld in input_fields)
            if has_custom_init else
            (fld.id for fld in input_fields if not attrs_fields_dict[fld.id].inherited)
        ),
    )
    output_fields = tuple(
        OutputField(
            id=field.id,
            type=field.type,
            default=(
                input_shape.fields_dict[field.id].default
                if field.id in input_shape.fields_dict else
                NoDefault()
            ),
            metadata=field.metadata,
            accessor=AttrAccessor(field.id, is_required=True),
        )
        for field in param_name_to_base_field.values()
    )
    return Shape(
        input=input_shape,
        output=OutputShape(
            fields=output_fields,
            overriden_types=frozenset(
                fld.id for fld in output_fields if not attrs_fields_dict[fld.id].inherited
            ),
        ),
    )
