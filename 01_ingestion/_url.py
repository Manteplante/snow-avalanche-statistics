"""Target URL(s) for avalanche_reports.py.

Leading underscore means this file is not itself a source.
"""
from __future__ import annotations

# The human-facing page (https://www.varsom.no/snoskred/snoskredulykker/
# snoskredulykker-i-tabell/) builds its accident table client-side from this
# JSON resource (loaded via a <script> tag, onload="LagTabell()"). Fetching
# it directly returns the full dataset — no cookie dialog, no year-range
# inputs, no JS execution needed.
REPORTS_URL = "https://www.iskart.no/varsom/ulykker/json/snoskredulykker_jsonp.json"
