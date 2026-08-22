"""Shared HTTP/HTML helpers for scraped sources.

Leading underscore means this file is not itself a source.
"""

from __future__ import annotations

import time

import requests
from bs4 import BeautifulSoup


def get_html(url: str, delay_seconds: float = 1.0, retries: int = 3) -> str:
    """GET a page, pausing first to be considerate to the server.

    Retries a few times on a transient connection failure or timeout — a
    network blip (seen in practice on GitHub Actions runners) shouldn't take
    down the whole pipeline run. A real HTTP error (404, 500, ...) is not
    retried, since retrying wouldn't fix it.
    """
    time.sleep(delay_seconds)
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if attempt == retries - 1:
                raise
            time.sleep(delay_seconds * (attempt + 1))


def soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")
