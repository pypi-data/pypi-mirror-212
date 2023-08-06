from numpy import generic
from pandas._typing import type_t
from pandas.api import extensions as pd_exts
from pandas.api.extensions import ExtensionDtype
from pandas.core.arrays import ExtensionArray
from pandas.core.dtypes.base import ExtensionDtype


@pd_exts.register_extension_dtype
class VectorDType(ExtensionDtype):
    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self):
        """Enables .astype("vector") method calls."""
        return "vector"

    @property
    def type(self):
        return generic

    @classmethod
    def construct_array_type(cls) -> type_t[ExtensionArray]:
        # Avoid circular import.
        # ExtensionArray requires ExtensionDtype in `dtype`
        from .arrays import VectorArray

        return VectorArray

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(str(self))
