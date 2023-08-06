"""campaign_metrics"""
import time
import os
from typing import Dict
import requests
import pandas as pd
from pandas import DataFrame as PandasDF

from iterable_etl.libs.network import get_data
from iterable_etl.libs.transform import csv_to_dataframe
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.cnst import urls, get_headers


def get_campaign_ids(api_url: str, headers: Dict[str, str]) -> list[int]:
    """Make a GET request to the Iterable API and return a list of campaign ids."""
    data = get_data(api_url, headers)
    campaign_ids = [
        campaign["id"]
        for campaign in data["campaigns"]
        if campaign["campaignState"] == "Running"
    ]
    return campaign_ids


def get_metrics_data(api_url: str, headers: Dict[str, str], campaign_id: int) -> bytes:
    """Make a GET request to the Iterable API and return the response content."""
    response = requests.get(api_url.format(campaign_id), headers=headers, timeout=10)
    response.raise_for_status()
    return response.content


@write_dataframe_to_csv("campaign_metrics")
@print_dataframe_head
def campaign_metrics_df() -> PandasDF:
    """campaign_metrics dataframe"""
    campaign_ids = get_campaign_ids(urls["campaigns"], get_headers())
    df_list = []
    for i, campaign_id in enumerate(campaign_ids):
        data = get_metrics_data(urls["metrics"], get_headers(), campaign_id)
        df = csv_to_dataframe(data)
        df_list.append(df)
        time.sleep(11)  # suboptimal
        if i == 5 and os.environ.get("APP_ENV") == "development":
            break
    combined_df = pd.concat(df_list)
    return combined_df
