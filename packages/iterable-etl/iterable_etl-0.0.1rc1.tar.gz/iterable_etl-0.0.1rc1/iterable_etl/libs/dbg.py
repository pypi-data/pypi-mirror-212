"""dbg"""

import os
from typing import Any, Callable, TypeVar

import pandas as pd

T = TypeVar('T')

def print_dataframe_head(func: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args: Any, **kwargs: Any) -> T:
        result = func(*args, **kwargs)
        if os.environ.get("APP_ENV") == "development":
            if isinstance(result, pd.DataFrame):
                print(func.__name__)
                print(result.head(10))
                print("")
            else:
                print("Returned object is not a DataFrame.")
        return result
    return wrapper

def write_dataframe_to_csv(file_name:str):
    def _write_dataframe_to_csv(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            result = func(*args, **kwargs)
            if os.environ.get("SAMPLE_OUTPUT") == "True":
                if isinstance(result, pd.DataFrame):
                    directory = "sample_output"
                    os.makedirs(directory, exist_ok=True)
                    csv_filename = f"{file_name}.csv"
                    csv_path = os.path.join(directory, csv_filename)
                    result.to_csv(csv_path, index=False)
                    print(f"DataFrame saved to: {csv_path}")
                else:
                    print("Returned object is not a DataFrame.")
            return result
        return wrapper
    return _write_dataframe_to_csv
