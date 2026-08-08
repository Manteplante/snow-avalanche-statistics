"""Snøskred — interactive map of avalanche accidents, reads the table
03_notebooks/01_clean_data.ipynb saved as 'snow_avalanche_data'.

Uses Kartverket's topographic WMTS tiles (verified live) rather than
OpenStreetMap for terrain context relevant to avalanche locations.
"""

import html

import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

from backend import storage

MONTH_ORDER = [
    "Januar", "Februar", "Mars", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Desember",
]
WEEKDAY_ORDER = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]

# Fields shown in a marker's popup, in the requested order.
POPUP_FIELDS = [
    ("Område", "område"),
    ("Kommune", "kommune"),
    ("Aktivitet", "aktivitet"),
    ("Utløser", "utløser"),
    ("Skredtatte", "skredtatte"),
    ("Døde", "døde"),
    ("Kun skadet", "kun skadet"),
    ("Skredutstyr", "skredutstyr"),
    ("Skredtype", "skredtype"),
    ("Svakt lag", "svakt lag"),
    ("Skredstørrelse", "skredstørrelse"),
    ("Eksposisjon", "eksposisjon"),
    ("Comment", "comment"),
]

# Verified with a live curl request (returned a real PNG terrain tile) —
# webmercator (EPSG:3857) matches Leaflet's default CRS with no plugins.
KARTVERKET_TOPO_TILES = "https://cache.kartverket.no/v1/wmts/1.0.0/topo/default/webmercator/{z}/{y}/{x}.png"
KARTVERKET_ATTR = '&copy; <a href="https://www.kartverket.no">Kartverket</a>'

st.header("🗺️ Snøskred")

df = storage.load("snow_avalanche_data")

if df.empty:
    st.info(f"No `snow_avalanche_data` table yet. Reading from `{storage.describe()}`.")
    st.stop()

# ── Sidebar slicers ────────────────────────────────────────────────────────
years = sorted(df["år"].dropna().unique())
months = sorted(df["måned"].dropna().unique(), key=MONTH_ORDER.index)
weekdays = sorted(df["dag"].dropna().unique(), key=WEEKDAY_ORDER.index)

chosen_years = st.sidebar.multiselect("År", years)
chosen_months = st.sidebar.multiselect("Måned", months)
chosen_weekdays = st.sidebar.multiselect("Dag", weekdays)

if chosen_years:
    df = df[df["år"].isin(chosen_years)]
if chosen_months:
    df = df[df["måned"].isin(chosen_months)]
if chosen_weekdays:
    df = df[df["dag"].isin(chosen_weekdays)]

df = df.dropna(subset=["latitude", "longitude"])

st.caption(f"Showing {len(df):,} accidents")

# ── Map ─────────────────────────────────────────────────────────────────────
def _field(row, column: str) -> str:
    value = row[column]
    return "–" if pd.isna(value) else html.escape(str(value))


norway = folium.Map(
    location=[65.0, 13.0],
    zoom_start=5,
    tiles=KARTVERKET_TOPO_TILES,
    attr=KARTVERKET_ATTR,
)
cluster = MarkerCluster().add_to(norway)

for _, row in df.iterrows():
    details = "".join(
        f"<b>{label}:</b> {_field(row, column)}<br>" for label, column in POPUP_FIELDS
    )
    popup_html = f"<b>{html.escape(str(row['sted']))}</b><br>{details}"

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        tooltip=str(row["sted"]),
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa"),
    ).add_to(cluster)

st_folium(norway, use_container_width=True, height=600, returned_objects=[])
