"""NVE flood avalanche events — mass-carrying flood records (skredType 171:
Masseførende flom) from NVE's national landslide/avalanche event database
("Skredhendelser"). A small category — around 34 records.

See _nve.py for the shared fetch/pagination logic and column shape.
"""
from __future__ import annotations

import pandas as pd

from _nve import fetch_events

WHERE = "skredType=171"


def fetch() -> pd.DataFrame:
    return fetch_events(WHERE)
