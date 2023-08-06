from __future__ import annotations

from typing import Any, Dict, Sequence, Hashable
from numpy.typing import NDArray
from pandas import DataFrame
from pandas.api import extensions as pd_exts
from .arrays import VectorArray
from pandas._libs import lib
import faiss
from faiss import Index


@pd_exts.register_dataframe_accessor("fuse")
class FusionAccessor:
    def __init__(self, df: DataFrame) -> None:
        self._df = df

    def __call__(self, *columns: str) -> VectorArray:
        for col in columns:
            if col not in self._df.columns:
                raise ValueError(
                    f"Column {col} not found in the DataFrame! Found: {self._df.columns}"
                )

        series = [df[col] for col in columns]
        arrays = np.stack([self._join(*zipped) for zipped in zip(*series)])
        return VectorArray(arrays)

    @staticmethod
    def _join(*values: Any) -> NDArray:
        return np.concatenate([FusionAccessor._to_sequence(value) for value in values])

    @staticmethod
    def _to_sequence(item: Any):
        if lib.is_list_like(item):
            return item

        return [item]


@pd_exts.register_dataframe_accessor("search")
class SearchAccessor:
    def __init__(self, df: DataFrame) -> None:
        self._df = df
        self._indices: Dict[Hashable, Index] = {}

    def create_index(self, column: Hashable, factory: str = "Flat"):
        # HACK: Only allow VectorArray for now.
        col = VectorArray(df[column], copy=False)
        index = faiss.IndexFlatL2(col.dims)
        index.add(col.numpy)
        self._indices[column] = index

    def __call__(
        self, column: Hashable, query: Sequence[float] | NDArray, top_k: int
    ) -> DataFrame:
        if column not in self._indices:
            self.create_index(column)

        index = self._indices[column]
        col = self._df[column]

        search_query = np.array(query)

        if search_query.ndim == 1:
            search_query = search_query[np.newaxis, :]
        else:
            raise ValueError("Batched queries not supported yet.")

        # D, I are of the shape
        # batch, top_k
        D, I = index.search(search_query, k=top_k)

        D = np.array(D).squeeze()
        I = np.array(I).squeeze()

        return DataFrame({"distance": D, "indices": I, "data": col.iloc[I]})
