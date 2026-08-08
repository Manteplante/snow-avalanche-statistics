# Snøskred og Isulykker

[![ci](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

An interactive dashboard of avalanche and ice accidents in Norway — every
recorded snow-avalanche accident (2009–2026) and ice accident, mapped on
Kartverket terrain, filterable by year, month and weekday.

- **🗺️ Snøskred** — 1,184 avalanche accidents, mainland Norway
- **🗺️ Isulykke** — 905 ice accidents, mainland Norway

Svalbard and Jan Mayen accidents exist in the source data but are excluded
from both maps — Kartverket's terrain tiles don't cover them, only mainland
Norway (verified directly against the tile service).

## Data & map credits

**A huge thank you to [Varsom.no](https://www.varsom.no)** for maintaining
and publishing open, structured data on avalanche and ice accidents across
Norway — this project would not exist without it.

**And to [Kartverket](https://www.kartverket.no)** (the Norwegian Mapping
Authority) for the open topographic map tiles the two pages are built on.

## Getting started

```bash
make setup      # creates .venv, installs dependencies, registers the notebook kernel
make pipeline   # fetches live data from Varsom.no, builds the two cleaned tables
make app        # opens the dashboard
```

Needs [`uv`](https://docs.astral.sh/uv/) and `make`. `02_data/` is generated
by `make pipeline` and not committed — a fresh clone starts empty.

## What's in this project

| Piece | What it does |
|---|---|
| `01_ingestion/avalanche_reports.py` | Fetches avalanche accident data (the JSON Varsom.no's own table page runs on) |
| `01_ingestion/ice_reports.py` | Same, for ice accidents |
| `03_notebooks/01_clean_data.ipynb` | Shapes avalanche data into `snow_avalanche_data` (Norwegian columns, derived `år`/`måned`/`dag`, Svalbard excluded) |
| `03_notebooks/02_clean_ice_data.ipynb` | Same, for ice data → `ice_reports_clean` |
| `04_pages/01_snøskred.py`, `04_pages/02_isulykke.py` | The two interactive maps |

## Built on a template

This project started from
[Manteplante/streamlit-google-storage-template](https://github.com/Manteplante/streamlit-google-storage-template) —
that's where the pipeline mechanics live: how `01_ingestion/`, `backend/transform.py`
and `04_pages/` fit together, Google Cloud Storage deployment, caching, and
everything else about the underlying Streamlit scaffolding. This README stays
focused on the project itself; see the template for the how-it-works deep dive.

Working in this repo with a coding agent? `AGENTS.md` documents this
project's own conventions.

## License

MIT.
