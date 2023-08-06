from __future__ import annotations
import itertools
from typing import Any, Sequence, overload

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandas._libs import lib
from pandas._typing import ArrayLike, Dtype, ScalarIndexer, SequenceIndexer, TakeIndexer
from pandas.api.extensions import ExtensionArray, ExtensionDtype
from pandas.core import algorithms


class VectorArray(ExtensionArray):
    def __init__(self, data: NDArray, copy: bool = False) -> None:
        super().__init__()
        try:
            data = np.array(data, copy=copy).tolist()

            # Raises ValueError for rigged arrays.
            self._data = np.array(data, copy=copy)

            # Raises ValueError if it's not 2D.
            _, self._dims = self._data.shape
        except ValueError as ve:
            raise ValueError(
                "VectorArray must be an array of vectors of the same dimension."
            ) from ve

    @overload
    def __getitem__(self, item: ScalarIndexer) -> Any:
        ...

    @overload
    def __getitem__(self, item: SequenceIndexer) -> VectorArray:
        ...

    def __getitem__(self, item: Any) -> Any:
        result = self._data[item]
        if lib.is_integer(item):
            return result
        else:
            return VectorArray(result)

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, VectorArray):
            return False

        data = self._data
        other_data = other._data

        if data.shape != other_data.shape:
            return False

        return np.all(data == other_data).item()

    @property
    def dtype(self) -> ExtensionDtype:
        # Avoid circular import
        # ExtensionDtype requires ExtensionArray in `construct_array_type`
        from .datatypes import VectorDType

        return VectorDType()

    @property
    def dims(self) -> int:
        return self._dims

    @classmethod
    def _from_sequence(
        cls, data: Sequence[Any], dtype: Dtype | None = None, copy: bool = False
    ):
        del dtype

        return VectorArray(np.array(data), copy=copy)

    @classmethod
    def _from_factorized(cls, values: NDArray, original: ExtensionArray):
        del original
        return VectorArray(values)

    @property
    def nbytes(self) -> int:
        return self._data.nbytes

    def isna(self) -> ArrayLike:
        return pd.isna(self._data)

    def copy(self) -> VectorArray:
        return VectorArray(self._data, copy=True)

    def take(
        self,
        indexer: TakeIndexer,
        *,
        allow_fill: bool = False,
        fill_value: Any | None = None,
    ) -> VectorArray:
        if fill_value is None:
            fill_value = self.dtype.na_value
        return VectorArray(
            algorithms.take(
                self._data,
                indices=indexer,
                allow_fill=allow_fill,
                fill_value=fill_value,
            )
        )

    @classmethod
    def _concat_same_type(cls, to_concat: Sequence[VectorArray]) -> VectorArray:
        return VectorArray(np.concatenate([va._data for va in to_concat]))

    @property
    def numpy(self):
        return self._data

    def _as_array1d(self):
        # Collect the second dimension into a list
        # because pandas would complain if it's more than 1D.
        array1d = np.full(shape=[len(self)], fill_value=None)
        list_data = self._data.tolist()
        for idx in range(len(self)):
            array1d[idx] = list_data[idx]
        return array1d

    def __array__(self):
        return self._as_array1d()
