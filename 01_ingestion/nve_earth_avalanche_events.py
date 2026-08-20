"""NVE earth avalanche events — soil, clay and debris slide records
(skredType 140-144: Løsmasseskred/Kvikkleireskred/Flomskred/Leirskred/
Jordskred, including quick-clay slides) from NVE's national landslide/
avalanche event database ("Skredhendelser").

See _nve.py for the shared fetch/pagination logic and column shape.
"""
from __future__ import annotations

import pandas as pd

from _nve import fetch_events

WHERE = "skredType>=140 AND skredType<=144"


def fetch() -> pd.DataFrame:
    return fetch_events(WHERE)
