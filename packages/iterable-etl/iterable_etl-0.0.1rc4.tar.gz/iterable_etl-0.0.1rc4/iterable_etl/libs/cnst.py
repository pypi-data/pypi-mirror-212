"""constants"""

import os
from typing import Dict

urls = {
    "lists": "https://api.iterable.com/api/lists",
    "campaigns": "https://api.iterable.com/api/campaigns",
    "metrics": "https://api.iterable.com/api/campaigns/metrics?campaignId={}&startDateTime=2021-06-01&endDateTime=2023-06-07",
}


def get_headers() -> Dict[str, str]:
    """header config for Iterable API"""
    headers = {
        "Api-Key": os.environ.get("ITERABLE_KEY"),
        "Content-Type": "application/json",
    }
    return headers
