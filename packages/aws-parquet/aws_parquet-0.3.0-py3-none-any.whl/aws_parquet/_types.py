"""Type definitions for the aws_parquet package."""
import pandas as pd
from typing import (
    Any,
    Generator,
    Dict,
    TypeVar,
    Union,
)

PartitionLike = Dict[str, Any]
DataFrameOrIteratorT = TypeVar(
    "DataFrameOrIteratorT",
    bound=Union[pd.DataFrame, Generator[pd.DataFrame, None, None]],
)
