"""Jordskred — interactive map of NVE's earth-avalanche-event registry, reads
the table 03_notebooks/04_clean_nve_earth_avalanche_events.ipynb saved as
'nve_earth_avalanche_events_clean'.

Soil, clay and debris slides (skredType 140-144, including quick-clay slides)
from NVE's national landslide/avalanche event database — a hazard registry,
not curated accident reports. NVE data is never part of `records` (see
backend/transform.py and 05_tests/test_records_excludes_nve.py) — this page's
table comes from the notebook cleaning the raw NVE file directly.

Same design as 01_snøskred_nve.py: Kartverket topographic WMTS tiles, and
FastMarkerCluster (client-side marker generation) rather than one Python
Marker object per row, which doesn't scale to tens of thousands of points.
"""

import json

import folium
import streamlit as st
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium

from backend import storage

MONTH_ORDER = [
    "Januar", "Februar", "Mars", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Desember",
]
WEEKDAY_ORDER = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]

# Fields shown in a marker's popup, in the requested order.
POPUP_FIELDS = [
    ("Skredtype", "skredtype"),
    ("Døde", "døde"),
    ("Berørte", "berørte"),
    ("Bygninger skadet", "bygninger skadet"),
    ("Vei skadet", "vei skadet"),
    ("Jernbane skadet", "jernbane skadet"),
    ("Evakuering", "evakuering"),
    ("Redningsaksjon", "redningsaksjon"),
    ("Ansvarlig institusjon", "ansvarlig institusjon"),
    ("Kilde", "kilde"),
    ("Comment", "comment"),
]

# Verified with a live curl request (returned a real PNG terrain tile) —
# webmercator (EPSG:3857) matches Leaflet's default CRS with no plugins.
KARTVERKET_TOPO_TILES = "https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png"
KARTVERKET_ATTR = '&copy; <a href="https://www.kartverket.no">Kartverket</a>'

st.header("🗺️ Jordskred")
st.caption("📡 Data: [NVE](https://www.nve.no/om-nve/aapne-data-og-api-fra-nve/) — Skredhendelser")
st.caption("ℹ️ Fordi Kartverket-kartet ikke dekker Svalbard, vises ikke hendelser derfra i denne visningen.")

df = storage.load("nve_earth_avalanche_events_clean")

if df.empty:
    st.info(f"No `nve_earth_avalanche_events_clean` table yet. Reading from `{storage.describe()}`.")
    st.stop()

# ── Sidebar slicers ────────────────────────────────────────────────────────
years = sorted(df["year"].dropna().astype(int).unique())
months = sorted(df["month"].dropna().unique(), key=MONTH_ORDER.index)
weekdays = sorted(df["day"].dropna().unique(), key=WEEKDAY_ORDER.index)

chosen_years = st.sidebar.multiselect("År", years)
chosen_months = st.sidebar.multiselect("Måned", months)
chosen_weekdays = st.sidebar.multiselect("Dag", weekdays)

if chosen_years:
    df = df[df["year"].isin(chosen_years)]
if chosen_months:
    df = df[df["month"].isin(chosen_months)]
if chosen_weekdays:
    df = df[df["day"].isin(chosen_weekdays)]

df = df.dropna(subset=["latitude", "longitude"])

st.caption(f"Showing {len(df):,} events")

# ── Map ─────────────────────────────────────────────────────────────────────
# FastMarkerCluster sends `data` (a plain array) to the browser once, and a JS
# `callback` builds each marker there — instead of one Python Marker/Popup
# object per row, which doesn't scale to tens of thousands of points.
FIELD_COLUMNS = [column for _, column in POPUP_FIELDS]
STED_INDEX = 2 + len(FIELD_COLUMNS)  # data columns are [lat, lon, *FIELD_COLUMNS, sted]

data_columns = df[["latitude", "longitude", *FIELD_COLUMNS, "sted"]].astype(object)
data = data_columns.where(data_columns.notna(), None).values.tolist()

# Same marker_color/icon_color/icon/prefix keys folium.Icon(...) itself sends
# to L.AwesomeMarkers.icon() on the other two Snøskred/Isulykke pages —
# verified against the installed folium package's source rather than assumed.
CALLBACK = """
function (row) {
    function esc(v) {
        if (v === null || v === undefined) { return null; }
        return String(v)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }
    function show(v) {
        var e = esc(v);
        return (e === null || e === '') ? '–' : e;
    }
    var labels = __LABELS__;
    var details = '';
    for (var i = 0; i < labels.length; i++) {
        details += '<b>' + labels[i] + ':</b> ' + show(row[2 + i]) + '<br>';
    }
    var sted = row[__STED_INDEX__] ? esc(row[__STED_INDEX__]) : 'Ukjent sted';
    var html = '<b>' + sted + '</b><br>' + details;

    var icon = L.AwesomeMarkers.icon({
        marker_color: 'red',
        icon_color: 'white',
        icon: 'exclamation-triangle',
        prefix: 'fa'
    });
    var marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.setIcon(icon);
    marker.bindTooltip(sted);
    marker.bindPopup(html, {maxWidth: 300});
    return marker;
}
""".replace("__LABELS__", json.dumps([label for label, _ in POPUP_FIELDS])).replace(
    "__STED_INDEX__", str(STED_INDEX)
)

norway = folium.Map(
    location=[65.0, 13.0],
    zoom_start=5,
    tiles=KARTVERKET_TOPO_TILES,
    attr=KARTVERKET_ATTR,
)
FastMarkerCluster(data=data, callback=CALLBACK).add_to(norway)

st_folium(norway, use_container_width=True, height=600, returned_objects=[])
