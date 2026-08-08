"""Avalanche reports — accident records scraped from varsom.no.

The accident table on varsom.no is built client-side from a JSON resource
(see _url.py); fetching that resource directly returns the full dataset in
one request, so this module never touches the human-facing page at all.
"""
from __future__ import annotations

import json
import re

import pandas as pd

from _http import get_html
from _url import REPORTS_URL


def _parse(raw: str) -> dict:
    """The response is a JS object literal (`var SnoskredulykkerJSON = {...};`),
    not strict JSON — two keys inside `rapport` entries are unquoted."""
    body = re.search(r"\{.*\}", raw, re.S).group(0)
    body = re.sub(r"([{,]\s*)(url|tekst)(\s*:)", r'\1"\2"\3', body)
    return json.loads(body)


def fetch() -> pd.DataFrame:
    data = _parse(get_html(REPORTS_URL))

    def lookup(table: str, code) -> str | None:
        """Translate a raw code into the display text varsom.no's own JS shows."""
        if code in (None, "", []):
            return None
        for entry in data[table]:
            if entry["navn"] == str(code):
                return entry["tabell"] or None
        return str(code)

    rows = [
        {
            "Dato": a["date"],
            "Døde": a["dode"],
            "Kun skadet": a["skadet"],
            "Skredtatte": a["skredtatte"],
            "Sted": a["sted"],
            "Latitude": a["breddegrad"],
            "Longitude": a["lengdegrad"],
            "Kommune": a["kommune"],
            "Område": lookup("omraader", a["omraade"]),
            "Aktivitet": lookup("aktiviteter", a["aktivitet"]),
            "Utløser": lookup("utlosningstyper", a["utlost"]),
            "Bakkeaktivitet": lookup("bakkeaktiviteter", a["bakkeaktivitet"]),
            "Skredutstyr": lookup("skredutstyr", a["skredutstyr"]),
            "Skredtype": lookup("skredtype", a["skredtype"]),
            "Svakt lag": lookup("svaktlag", a["svaktlag"]),
            "Skredstørrelse": lookup("skredstorrelse", a["skredstorrelse"]),
            "Eksposisjon": lookup("eksposisjoner", a["eksposisjon"]),
            "Comment": a["beskrivelse"],
        }
        for a in data["ulykker"]
    ]
    return pd.DataFrame(rows)
