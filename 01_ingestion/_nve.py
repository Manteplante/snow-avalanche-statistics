"""Shared fetch logic for NVE Skredhendelser sources (nve_*_events.py).

One ArcGIS REST Feature Service (see NVE_SKREDHENDELSER_URL in _url.py) covers
every slide type NVE tracks — rockslides, quick-clay slides, ice/cornice fall,
snow avalanches, and more, distinguished by the numeric `skredType` field.
Each nve_*_events.py source is a thin wrapper: it just supplies the `where`
clause for its slide-type range and gets the same columns back.

Leading underscore means this file is not itself a source.
"""
from __future__ import annotations

import json
from urllib.parse import urlencode

import pandas as pd

from _http import get_html
from _url import NVE_SKREDHENDELSER_URL

PAGE_SIZE = 1000

FIELDS = [
    "skredNavn", "stedsnavn",
    "skredTidspunkt_aar", "skredTidspunkt_mnd", "skredTidspunkt_dag",
    "Value", "totAntPersOmkommet", "persBerort", "bygnSkadet", "vegSkadet",
    "baneSkadet", "evakuering", "redningsaksjon", "ansvarligInstitusjon",
    "registrertAv", "beskrivelse",
]


def _page(where: str, offset: int) -> list[dict]:
    params = {
        "where": where,
        "outFields": ",".join(FIELDS),
        "outSR": "4326",  # WGS84 lat/lon, not the service's native UTM
        "resultOffset": offset,
        "resultRecordCount": PAGE_SIZE,
        "f": "json",
    }
    url = f"{NVE_SKREDHENDELSER_URL}?{urlencode(params)}"
    return json.loads(get_html(url)).get("features", [])


def _date(a: dict) -> str | None:
    year, month, day = a["skredTidspunkt_aar"], a["skredTidspunkt_mnd"], a["skredTidspunkt_dag"]
    return f"{year:04d}-{month:02d}-{day:02d}" if year and month and day else None


def fetch_events(where: str) -> pd.DataFrame:
    """Every NVE Skredhendelser event matching `where` (a skredType filter)."""
    rows: list[dict] = []
    offset = 0
    while True:
        features = _page(where, offset)
        for feature in features:
            a = feature["attributes"]
            g = feature.get("geometry") or {}
            rows.append({
                "Dato": _date(a),
                "Sted": a["skredNavn"] or a["stedsnavn"],
                "Latitude": g.get("y"),
                "Longitude": g.get("x"),
                "Skredtype": a["Value"],
                "Døde": a["totAntPersOmkommet"],
                "Berørte": a["persBerort"],
                "Bygninger skadet": a["bygnSkadet"],
                "Vei skadet": a["vegSkadet"],
                "Jernbane skadet": a["baneSkadet"],
                "Evakuering": a["evakuering"],
                "Redningsaksjon": a["redningsaksjon"],
                "Ansvarlig institusjon": a["ansvarligInstitusjon"],
                "Kilde": a["registrertAv"],
                "Comment": a["beskrivelse"],
            })
        if len(features) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    return pd.DataFrame(rows)
