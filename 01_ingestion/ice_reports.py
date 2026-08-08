"""Ice accident reports — accident records scraped from varsom.no.

The accident table on varsom.no is built client-side from a JSON resource
(see _url.py); fetching that resource directly returns the full dataset in
one request, so this module never touches the human-facing page at all.
"""
from __future__ import annotations

import json
import re

import pandas as pd

from _http import get_html
from _url import ICE_REPORTS_URL


def _parse(raw: str) -> dict:
    """The response is `var IsulykkerJSON = {...};` — strip the JS wrapper."""
    body = re.search(r"\{.*\}", raw, re.S).group(0)
    return json.loads(body)


def _clean(value):
    """Empty string/list -> None, so missing data lands as null, not "":"""
    return None if value in (None, "", []) else value


def fetch() -> pd.DataFrame:
    data = _parse(get_html(ICE_REPORTS_URL))

    def to_int(value) -> int | None:
        cleaned = _clean(value)
        return int(cleaned) if cleaned is not None else None

    rows = [
        {
            "Dato": a["date"],
            "Døde": a["omkom_barn"] + a["omkom_voksen"],
            "Gjennom isen": to_int(a.get("deltagere")),
            "Vann/sted": _clean(a.get("vann")),
            "Latitude": a["bredde"],
            "Longitude": float(a["lengde"]),
            "Høyde": a["hoyde"],
            "Kommune": _clean(a.get("kommune")),
            "Fylke": a["fylke"],
            "Aktivitet": a["aktivitet"][0] if a["aktivitet"] else None,
            "Vanntype": _clean(a.get("vanntypetekst")),
            "Istype": _clean(a.get("istypetekst")),
            "Påvirket": _clean(a.get("regulerttekst")),
            "Comment": _clean(a.get("tekst")),
        }
        for a in data["Marker"]
    ]
    return pd.DataFrame(rows)
