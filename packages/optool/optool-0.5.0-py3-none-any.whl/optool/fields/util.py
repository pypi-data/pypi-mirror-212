from __future__ import annotations

import re
from typing import Any, Callable, Dict, Iterable, Optional, Type, TypeVar, Union

import numpy as np
import pydantic
from pydantic.fields import ModelField
from pydantic.validators import find_validators

from optool import BaseModel
from optool.uom import PhysicalDimension

TypeDefinition = Union[type, tuple[type, ...]]
ValidationFunc = Callable[[Any], Any]

T = TypeVar("T")


class WrongTypeError(ValueError):

    def __init__(self, *, expected: TypeDefinition, value: Any) -> None:
        super().__init__(f"expected {expected}, but got {value}")


class WrongSubTypeError(ValueError):

    def __init__(self, *, expected_type: TypeDefinition, expected_subtype: TypeDefinition,
                 actual_subtype: TypeDefinition, value: Any) -> None:
        super().__init__(f"expected sub-type {expected_subtype} of {expected_type}, "
                         f"but got sub-type {actual_subtype} of {type(value)}")


class ArbitrarySubTypeError(ValueError):

    def __init__(self, *, name: str, field: ModelField) -> None:
        sub_type = None if field.sub_fields is None else field.sub_fields[0].type_
        super().__init__(f"the sub-field of {name!r} has the type {field.type_} (with sub-type {sub_type}), "
                         f"but {field.type_} does not offer any specific validators that would be able to handle "
                         f"sub-types")


class _ConfigWithArbitraryTypesNotAllowed(BaseModel.Config):
    arbitrary_types_allowed = False


def has_specific_type_validator(type_: Type[Any]) -> bool:
    """
    Determines if the type specified has one or more validators that are more specific than just the
    `arbitrary_type_validator` that is used when `arbitrary_types_allowed` of Config is set to :py:data:`True`.

    Args:
        type_: The type to analyze.

    Returns:
        :py:data:`True` if the type specified has a validator that is different from the `arbitrary_type_validator`,
        :py:data:`False` otherwise.
    """

    try:
        next(find_validators(type_, _ConfigWithArbitraryTypesNotAllowed))
        return True
    except Exception as e:
        if re.match("no validator found for <.*?>, see `arbitrary_types_allowed` in Config", str(e)):
            return False
        raise e


def check_validation_is_passed_on_to_sub_types(name: str, field: ModelField) -> None:
    if field.sub_fields is None:
        return
    if not has_specific_type_validator(field.type_):
        raise ArbitrarySubTypeError(name=name, field=field)
    for sub_field in field.sub_fields:
        check_validation_is_passed_on_to_sub_types(field.name, sub_field)


def check_sub_fields_level(field: ModelField) -> None:
    if field.sub_fields is None:
        return
    if field.sub_fields[0].sub_fields:
        raise ValueError(f"Generic types more than one level deep are currently not supported. "
                         f"Got {field.sub_fields[0].type_} and {field.sub_fields[0].sub_fields[0].type_}.")


def get_type_validator(expected_type: Type[T]) -> Callable[[Any], T]:
    """
    Creates a validation function that checks if the input argument is of the expected type.

    Args:
        expected_type: The type the resulting validator will enforce.

    Returns:
        A new function that can be used to validate if an input value is an instance of the type specified.
    """

    def validate_type(value: Any) -> T:
        if isinstance(value, expected_type):
            return value
        raise WrongTypeError(expected=expected_type, value=value)

    return validate_type


def get_subtype_validator(object_type: Type[T], subtype_provider: Callable[[T],
                                                                           Type]) -> Callable[[Any, ModelField], T]:
    """
    Creates a validation function that checks if the subtype of the input argument is of the expected type.

    Args:
        object_type: The type the resulting validator will enforce.
        subtype_provider: Callable to get the subtype of the provided value.

    Returns:
        A new function that can be used to validate if an input value is an instance of the type specified.
    """

    def validate_subtype(value: Any, field: ModelField) -> T:
        if field.sub_fields:
            expected_subtype = field.sub_fields[0].type_
            actual_subtype = subtype_provider(value)
            if expected_subtype != actual_subtype:
                if isinstance(actual_subtype, np.dtype):
                    actual_subtype = actual_subtype.type
                raise WrongSubTypeError(expected_type=object_type,
                                        expected_subtype=expected_subtype,
                                        actual_subtype=actual_subtype,
                                        value=value)
            check_sub_fields_level(field)

        return value

    return validate_subtype


def check_only_one_specified(first: Any, second: Any, message: str) -> None:
    first_present = first if isinstance(first, bool) else first is not None
    second_present = second if isinstance(second, bool) else second is not None
    if first_present and second_present:
        raise ValueError(message)


def get_subfield_schema(field: Optional[ModelField], subfield_index: int) -> Optional[Dict[str, Any]]:
    """
    Creates a schema of the sub-field of the model field specified.

    Args:
        field: The model field.
        subfield_index: The index of the sub-field of interest.

    Returns:
        The schema representing the sub-field of the model field if it is present, :py:data:`None` otherwise.
    """
    if field is None or field.sub_fields is None:
        return None
    subfield_schema = pydantic.schema_of(field.sub_fields[subfield_index].type_)
    subfield_schema.pop('title', None)
    return subfield_schema


def get_dimension(field: Optional[ModelField], subfield_index: int) -> Optional[PhysicalDimension]:
    """
    Gets the physical dimension associated to the model field specified.

    Args:
        field: The model field.
        subfield_index: The index of the sub-field of interest.

    Returns:
        The physical dimension associated to the model field if it is present, :py:data:`None` otherwise.
    """
    if field is None or field.sub_fields is None:
        return None
    dimension = field.sub_fields[subfield_index].type_
    if dimension == Any:
        return None
    if issubclass(dimension, PhysicalDimension):
        return dimension

    raise TypeError(f"Unsupported {dimension}, should be a {PhysicalDimension.__name__!r} or 'typing.Any'.")


def update_object_schema(field_schema: Dict[str, Any], **properties) -> None:
    """
    Updates the field schema with object properties, ignoring :py:data:`None` values.

    Updates the dictionary with a key ``type`` set to ``object`` and a key ``property``, the value of which is a
    dictionary containing all properties specified that are not :py:data:`None`.

    Args:
        field_schema: The field schema to update.
        **properties: The properties
    """
    field_schema |= {"type": "object", "properties": {k: v for (k, v) in properties.items() if v is not None}}


def validate(value: T,
             validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
             msg_template: Optional[str] = None) -> T:
    """
    Validates a given value based on the validator function(s) specified.

    Args:
        value: The value to validate.
        validators: The validator function(s).
        msg_template: The message to show in case the validation fails, may contain ``{value}`` to refer to the value.

    Returns:
        The given value in case the validation is successful.
    """
    msg_template = msg_template or "Validation failed for {value}"
    error = ValueError(msg_template.format(value=value))
    if isinstance(validators, bool):
        if validators:
            return value
        raise error

    for validator in validators if isinstance(validators, Iterable) else [validators]:
        try:
            satisfied = validator(value)
        except Exception as e:
            raise error from e

        if not satisfied:
            raise error

    return value


def validate_each(value: Iterable,
                  validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
                  msg_template: Optional[str] = None) -> None:
    for (i, element) in enumerate(value):
        validate(element, validators, f'While validating element {i}: {msg_template}')
