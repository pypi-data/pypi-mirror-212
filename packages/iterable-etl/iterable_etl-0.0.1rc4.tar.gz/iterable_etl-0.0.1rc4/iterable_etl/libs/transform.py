"""transform"""

from typing import Dict, Any
import io

import pandas as pd
from pandas import DataFrame as PandasDF


def json_to_dataframe(data: Dict[str, Any]) -> PandasDF:
    """Convert the JSON data to a Pandas DataFrame."""
    df = pd.json_normalize(data)
    return df


def csv_to_dataframe(data: str) -> PandasDF:
    """Convert the CSV data to a Pandas DataFrame."""
    df = pd.read_csv(io.StringIO(data.decode("utf-8")), index_col=0)
    return df
