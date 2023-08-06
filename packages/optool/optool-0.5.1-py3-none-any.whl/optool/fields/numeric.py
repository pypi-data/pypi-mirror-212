from __future__ import annotations

import itertools
import numbers
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Iterable, Optional, Type, TypeVar, Union

import numpy as np
import pydantic
from pydantic.fields import ModelField

from optool.fields.util import (WrongTypeError, check_only_one_specified, check_sub_fields_level, get_subtype_validator,
                                get_type_validator, update_object_schema)


class ShapeError(ValueError):

    def __init__(self, *, expected: tuple[int, ...], value: np.ndarray) -> None:
        super().__init__(f"expected the shape {expected}, but got a value with shape {value.shape}")


class DimensionsError(ValueError):

    def __init__(self, *, expected: int, value: np.ndarray) -> None:
        super().__init__(f"expected {expected} dimension(s), but got a value with {np.ndim(value)} dimension(s)")


class ArrayWriteableError(ValueError):

    def __init__(self, *, expected: bool, value: np.ndarray) -> None:
        super().__init__(f"expected writeable is {expected}, "
                         f"but got a value with writeable flag set to {value.flags.writeable}")


T = TypeVar("T", bound=np.generic)  # Allow storing everything in ndarray


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedNdArray(pydantic.BaseModel, Generic[T]):
    """
    Pydantic-compatible field type for :py:class:`numpy.ndarray` objects, which allows to specify the data-type.

    The approach is inspired by https://github.com/cheind/pydantic-numpy.

    See Also:
        `Pydantic documentation: Custom Data Types <https://docs.pydantic.dev/usage/types/#custom-data-types>`_ and
        class :py:class:`pydantic.types.ConstrainedInt` or similar of :py:mod:`pydantic`
    """

    strict: ClassVar[bool] = True
    strict_subtypes: ClassVar[bool] = True
    dimensions: ClassVar[Optional[int]] = None
    shape_spec: ClassVar[Optional[tuple[int, ...]]] = None
    writeable: ClassVar[bool] = True

    @classmethod
    def __get_validators__(cls):
        if cls.strict:
            yield get_type_validator(np.ndarray)
        if cls.strict_subtypes:
            yield get_subtype_validator(np.ndarray, lambda x: x.dtype)

        if not cls.strict:
            yield cls.validate_ndarray
        yield cls.validate_dimensions
        yield cls.validate_shape
        yield cls.validate_writeable

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any], field: Optional[ModelField]):
        update_object_schema(field_schema,
                             dimensions=cls.dimensions,
                             shape_spec=cls.shape_spec,
                             writeable=cls.writeable,
                             datatype=field.sub_fields[0].type_.__name__ if field and field.sub_fields else None)

    @classmethod
    def validate_ndarray(cls, val: Any, field: ModelField) -> np.ndarray:
        if not isinstance(val, Iterable):
            val = [val]  # otherwise, np.asarray returns something weird

        if field.sub_fields is not None:
            check_sub_fields_level(field)
            expected_subtype = field.sub_fields[0].type_
            array = np.asarray(val, dtype=expected_subtype)
        else:
            try:
                array = np.asarray(val)
            except Exception as e:
                raise WrongTypeError(expected=(np.ndarray, numbers.Number, Iterable), value=val) from e

        array.setflags(write=cls.writeable)
        return array

    @classmethod
    def validate_dimensions(cls, val: np.ndarray) -> np.ndarray:
        if cls.dimensions is None or cls.dimensions == val.ndim:
            return val
        raise DimensionsError(expected=cls.dimensions, value=val)

    @classmethod
    def validate_shape(cls, val: np.ndarray) -> np.ndarray:
        if cls.shape_spec is None:
            return val
        if all(cls._compare_dim(*dims) for dims in itertools.zip_longest(cls.shape_spec, val.shape)):
            return val
        raise ShapeError(expected=cls.shape_spec, value=val)

    @classmethod
    def validate_writeable(cls, val: np.ndarray) -> np.ndarray:
        if val.flags.writeable == cls.writeable:
            return val
        raise ArrayWriteableError(expected=cls.writeable, value=val)

    @classmethod
    def _compare_dim(cls, expected: Optional[int], actual: Optional[int]) -> bool:
        return actual == expected or expected == -1


def conndarray(*,
               strict: bool = False,
               dimensions: Optional[int] = None,
               shape: Optional[tuple[int, ...]] = None,
               writeable: bool = True) -> Type[np.ndarray]:
    """
    Creates a Pydantic-compatible field type for :py:class:`numpy.ndarray` objects, which allows specifying constraints
    on the accepted values.

    Args:
        strict: If :py:data:`True` only values of type :py:class:`numpy.ndarray` are accepted. (Default:
            :py:data:`False`)
        dimensions: The expected dimensions as in :py:func:`numpy.ndim`.
        shape: The shape expected. One shape dimension can be ``-1`` indicating that this dimension is arbitrary.
        writeable: Boolean flag indicating whether the :py:class:`numpy.ndarray` object is mutable or not.

    Returns:
        A new Pydantic-compatible field type.

    See Also:
        Method :py:func:`pydantic.conint` or similar of :py:mod:`pydantic`.
    """
    check_only_one_specified(dimensions, shape, "Cannot specify both dimensions and shape.")
    namespace = dict(strict=strict, dimensions=dimensions, shape_spec=shape, writeable=writeable)
    return type('ConstrainedNdArrayValue', (ConstrainedNdArray,), namespace)  # type: ignore


if TYPE_CHECKING:

    NdArrayLike = Union[np.ndarray[Any, np.dtype[T]], numbers.Number, Iterable]
    Array = Union[np.ndarray[Any, np.dtype[T]], numbers.Number, Iterable]
    ImmutableArray = Union[np.ndarray[Any, np.dtype[T]], numbers.Number, Iterable]

    StrictNdArray = np.ndarray[Any, np.dtype[T]]
    Row = np.ndarray[Any, np.dtype[T]]
    Column = np.ndarray[Any, np.dtype[T]]
    Matrix = np.ndarray[Any, np.dtype[T]]

else:

    class NdArrayLike(ConstrainedNdArray[T]):
        strict = False
        strict_subtypes = False

    class Array(ConstrainedNdArray[T]):
        """Pydantic-compatible field type for one-dimensional :py:class:`numpy.ndarray` objects."""
        strict = False
        strict_subtypes = False
        dimensions = 1

    class ImmutableArray(Array[T]):
        """
        Pydantic-compatible field type for one-dimensional :py:class:`numpy.ndarray` objects, where the flag
        ``writeable`` is set to :py:data:`False`.
        """
        strict = False
        strict_subtypes = False
        writeable = False

    class StrictNdArray(ConstrainedNdArray[T]):
        strict = True
        strict_subtypes = True

    class Row(ConstrainedNdArray[T]):
        """Pydantic-compatible field type for two-dimensional :py:class:`numpy.ndarray` objects representing row
        vectors."""
        strict = True
        strict_subtypes = False
        shape_spec = (1, -1)

    class Column(ConstrainedNdArray[T]):
        """Pydantic-compatible field type for two-dimensional :py:class:`numpy.ndarray` objects representing column
        vectors."""
        strict = True
        strict_subtypes = False
        shape_spec = (-1, 1)

    class Matrix(ConstrainedNdArray[T]):
        """Pydantic-compatible field type for two-dimensional :py:class:`numpy.ndarray` objects representing
        matrices."""
        strict = True
        strict_subtypes = False
        dimensions = 2
