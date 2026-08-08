"""Landing page — what the dashboard opens on."""

import streamlit as st

from backend import config
from backend import storage

st.title("❄️ Snøskred -og isulykker historisk data")

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
        'Image generated using the prompt "Create an animated picture of a blue sky, '
        'a mountain, and a snow avalanche," by OpenAI.'
    )

st.caption(
    "Data from [Varsom.no](https://www.varsom.no). Map tiles from "
    "[Kartverket](https://www.kartverket.no). Huge thanks to both — "
    "this dashboard would not exist without their open data."
)
