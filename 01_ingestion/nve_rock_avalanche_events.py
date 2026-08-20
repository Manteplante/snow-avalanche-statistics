"""NVE rock avalanche events — rockfall and rockslide records (skredType
110-113: Skred fra fast fjell/Steinsprang/Steinskred/Fjellskred) from NVE's
national landslide/avalanche event database ("Skredhendelser").

See _nve.py for the shared fetch/pagination logic and column shape.
"""
from __future__ import annotations

import pandas as pd

from _nve import fetch_events

WHERE = "skredType>=110 AND skredType<=113"


def fetch() -> pd.DataFrame:
    return fetch_events(WHERE)
