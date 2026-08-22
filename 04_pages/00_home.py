"""Landing page — what the dashboard opens on."""

import streamlit as st

from backend import config
from backend import storage

st.title("❄️🪨🌊 Snøskred og andre skredtyper")

# Try storage first (bucket in a deployed app, or 02_data/tables/ locally
# once the pipeline has uploaded it there) — fall back to the local asset
# directly, so the banner shows up even before the first `make pipeline` run.
frontpage = storage.load_figure("frontpage")
if frontpage is None:
    local = config.ROOT / "assets" / "frontpage.png"
    if local.exists():
        frontpage = local.read_bytes()

if frontpage is not None:
    st.image(frontpage)
    st.caption(
        'Photo: Markus Malmin/Røde Kors. Thank you for letting us use the photo!'
    )

st.caption(
    "Data from [Varsom.no](https://www.varsom.no) and "
    "[NVE](https://www.nve.no/om-nve/aapne-data-og-api-fra-nve/). Map tiles "
    "from [Kartverket](https://www.kartverket.no). Huge thanks to all "
    "three — this dashboard would not exist without their open data."
)
st.caption(
    "This dashboard only shows what these sources publish — nothing is "
    "independently verified, added to, or corrected beyond what's fetched "
    "directly from them."
)
