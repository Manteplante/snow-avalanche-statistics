"""NVE avalanche events — snow-avalanche records from NVE's national
landslide/avalanche event database ("Skredhendelser").

This is a broader, different dataset than avalanche_reports.py: it's a hazard
*registry* (every observed/reported avalanche event, most with no casualties,
dating back to the 1950s) rather than varsom.no's curated *accident* reports.
Kept as its own source rather than merged into avalanche_reports.py.

See _nve.py for the shared fetch/pagination logic and column shape — every
nve_*_events.py source is just a skredType filter over the same endpoint.
"""
from __future__ import annotations

import pandas as pd

from _nve import fetch_events

# Snow avalanches only (130 Snøskred-uspesifisert .. 139 Tørt flakskred). The
# service also tracks rockslides, quick-clay slides, ice fall, etc. under
# other skredType ranges — see the nve_*_events.py sibling sources.
WHERE = "skredType>=130 AND skredType<=139"


def fetch() -> pd.DataFrame:
    return fetch_events(WHERE)
