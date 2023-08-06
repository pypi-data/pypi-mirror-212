from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, TypeVar

import pydantic
from pydantic import ValidationError
from pydantic.fields import ModelField

from optool.fields.util import (WrongTypeError, check_validation_is_passed_on_to_sub_types, get_dimension,
                                get_subfield_schema, get_subtype_validator, get_type_validator, update_object_schema)
from optool.uom import UNITS, PhysicalDimension, Quantity, Unit


class DimensionalityError(ValueError):

    def __init__(self, *, expected: Optional[str], value: Quantity) -> None:
        super().__init__(f"expected the dimensionality {expected}, "
                         f"but got a value with dimensionality {value.dimensionality}")


class UnsupportedMagnitudeConversion(ValueError):

    def __init__(self, *, value: Any) -> None:
        super().__init__(f"the value of {type(value)} cannot be converted automatically")


class UnitParseError(ValueError):

    def __init__(self, *, unit: str) -> None:
        super().__init__(f"cannot parse the unit {unit}")


D = TypeVar("D", bound=PhysicalDimension)


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedUnit(pydantic.BaseModel, Generic[D]):
    """
    Pydantic-compatible field type for :py:class:`pint.Unit` objects, which allows to specify the desired
    dimensionality.

    See Also:
        `Pydantic documentation: Custom Data Types <https://docs.pydantic.dev/usage/types/#custom-data-types>`_ and
        class :py:class:`pydantic.types.ConstrainedInt` or similar of :py:mod:`pydantic`
    """
    strict: ClassVar[bool] = True

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(Unit) if cls.strict else cls.validate_unit
        yield cls.validate_dimensionality

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        dimension = get_dimension(field, 0)
        update_object_schema(field_schema, dimensionality=dimension.dimensionality if dimension else None)

    @classmethod
    def validate_unit(cls, value: Any, field: ModelField) -> Unit:
        if isinstance(value, Unit):
            return value

        if isinstance(value, str):
            try:
                return UNITS.parse_units(value)
            except Exception as e:
                raise UnitParseError(unit=value) from e

        raise WrongTypeError(expected=(Unit, str), value=value)

    @classmethod
    def validate_dimensionality(cls, val: Unit, field: ModelField) -> Unit:
        dimension = get_dimension(field, 0)
        if dimension is None or val.dimensionality == UNITS.get_dimensionality(dimension.dimensionality):
            return val
        raise DimensionalityError(expected=dimension.dimensionality, value=val)


T = TypeVar("T")  # Allow storing everything as magnitude in Quantity


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedQuantity(pydantic.BaseModel, Generic[D, T]):
    """
    Pydantic-compatible field type for :py:class:`optool.uom.Quantity` objects, which allows to specify the desired
    dimensionality.

    See Also:
        Class :py:class:`pydantic.types.ConstrainedInt` or similar of :py:mod:`pydantic`.
    """

    strict: ClassVar[bool] = True
    strict_subtypes: ClassVar[bool] = True

    @classmethod
    def __get_validators__(cls):
        if cls.strict:
            yield get_type_validator(Quantity)
        if cls.strict_subtypes:
            yield get_subtype_validator(Quantity, lambda x: type(x.m))

        if not cls.strict:
            yield cls.validate_quantity
        yield cls.validate_dimensionality
        yield cls.validate_magnitude

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        dimension = get_dimension(field, 0)
        update_object_schema(field_schema,
                             dimensionality=dimension.dimensionality if dimension else None,
                             datatype=get_subfield_schema(field, 1))

    @classmethod
    def validate_quantity(cls, val: Any, field: ModelField) -> Quantity:
        try:
            return Quantity(val)
        except Exception as e:
            raise WrongTypeError(expected=(Quantity, str, Number), value=val) from e

    @classmethod
    def validate_dimensionality(cls, val: Quantity, field: ModelField) -> Quantity:
        dimension = get_dimension(field, 0)
        if dimension is None or val.dimensionality == UNITS.get_dimensionality(dimension.dimensionality):
            return val
        raise DimensionalityError(expected=dimension.dimensionality, value=val)

    @classmethod
    def validate_magnitude(cls, val: Quantity, field: ModelField) -> Quantity:
        if not field.sub_fields:
            return val

        magnitude_field = field.sub_fields[1]
        check_validation_is_passed_on_to_sub_types(field.name, magnitude_field)
        valid_value, error = magnitude_field.validate(val.m, {}, loc='magnitude')
        if error:
            raise ValidationError([error], cls)

        return Quantity(valid_value, val.u)


if TYPE_CHECKING:
    UnitLike = Unit
    StrictUnit = Unit

    QuantityLike = Quantity
    StrictQuantity = Quantity

else:

    class UnitLike(ConstrainedUnit[D], Unit):
        strict = False

    class StrictUnit(ConstrainedUnit[D], Unit):
        strict = True

    class QuantityLike(ConstrainedQuantity[D, T], Quantity):
        strict = False
        strict_subtypes = False

    class StrictQuantity(ConstrainedQuantity[D, T], Quantity):
        strict = True
        strict_subtypes = False
