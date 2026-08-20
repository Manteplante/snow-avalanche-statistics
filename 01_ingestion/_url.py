"""Target URL(s) for avalanche_reports.py, ice_reports.py and nve_avalanche_events.py.

Leading underscore means this file is not itself a source.
"""
from __future__ import annotations

# The human-facing page (https://www.varsom.no/snoskred/snoskredulykker/
# snoskredulykker-i-tabell/) builds its accident table client-side from this
# JSON resource (loaded via a <script> tag, onload="LagTabell()"). Fetching
# it directly returns the full dataset — no cookie dialog, no year-range
# inputs, no JS execution needed.
REPORTS_URL = "https://www.iskart.no/varsom/ulykker/json/snoskredulykker_jsonp.json"

# Same pattern as REPORTS_URL, for the ice-accident table at
# https://www.varsom.no/is/isulykker/isulykker-i-tabell/.
ICE_REPORTS_URL = "https://www.iskart.no/varsom/ulykker/json/isulykker_jsonp.json"

# NVE's national landslide/avalanche event database ("Skredhendelser"),
# licensed CC BY 3.0 (https://data.norge.no/nb/datasets/9a9d9575-59c7-48d5-
# 9f68-1d66bd8e76a7/skredhendelser). A plain ArcGIS REST Feature Service query
# endpoint — real JSON, no cookies, no JS. Layer 0 ("Skredtype") carries every
# slide type NVE tracks (rockslides, quick-clay slides, snow avalanches, ...);
# nve_avalanche_events.py filters server-side to snow avalanches only
# (skredType 130-139).
NVE_SKREDHENDELSER_URL = "https://gis3.nve.no/map/rest/services/Mapservices/SkredHendelser/MapServer/0/query"
