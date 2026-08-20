"""NVE ice avalanche events — mountain ice fall and snow cornice collapse
records (skredType 150-151: Isnedfall/Skavlfall) from NVE's national
landslide/avalanche event database ("Skredhendelser").

Not to be confused with 01_ingestion/ice_reports.py, which is a different
source entirely — varsom.no's lake/sea ice accident reports (people/vehicles
falling through ice). This one is ice breaking off cliffs and glaciers, and
overhanging snow cornices collapsing — a mountain hazard, closer in kind to
the other nve_*_events.py sources than to ice_reports.py.

See _nve.py for the shared fetch/pagination logic and column shape.
"""
from __future__ import annotations

import pandas as pd

from _nve import fetch_events

WHERE = "skredType>=150 AND skredType<=151"


def fetch() -> pd.DataFrame:
    return fetch_events(WHERE)
