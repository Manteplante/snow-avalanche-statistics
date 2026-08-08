"""Landing page — what the dashboard opens on."""

import streamlit as st

from backend import config

st.title("❄️ Snøskred -og isulykker historisk data")

frontpage = config.ROOT / "assets" / "frontpage.png"
if frontpage.exists():
    st.image(str(frontpage))
    st.caption(
        'Image generated using the prompt "Create an animated picture of a blue sky, '
        'a mountain, and a snow avalanche," by OpenAI.'
    )
    st.caption(
        "Data from [Varsom.no](https://www.varsom.no). Map tiles from "
        "[Kartverket](https://www.kartverket.no). Huge thanks to both — "
        "this dashboard would not exist without their open data."
    )
