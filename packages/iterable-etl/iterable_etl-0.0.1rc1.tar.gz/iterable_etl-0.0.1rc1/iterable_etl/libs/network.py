"""network"""

from typing import Dict, Any
import requests

def get_data(api_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Make a GET request to the Iterable API and return the data."""
    response = requests.get(api_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data
