"""NVE data must never end up in the `records` table.

`nve_*_events.py` sources are ingested to 02_data/raw/ like any other source,
but they're collectively ~30x the row count of every other source combined,
and `records` feeds a table that gets uploaded to a live GCS bucket
(GCS_UPLOAD=true). backend/transform.py's build_tables() excludes any source
starting with "nve_" — this is a hard invariant, tested directly rather than
relying on the comment in that function staying accurate.
"""

import pandas as pd

from backend import storage
from backend.transform import build_tables


def test_build_tables_excludes_nve_sources():
    raw = pd.DataFrame({
        "value": [1, 2, 3, 4, 5],
        "source": [
            "avalanche_reports",
            "ice_reports",
            "nve_avalanche_events",
            "nve_rock_avalanche_events",
            "nve_underwater_avalanche_events",
        ],
    })

    records = build_tables(raw)["records"]

    assert not records["source"].str.startswith("nve_").any(), (
        f"records must never contain an nve_* source, got: {sorted(records['source'].unique())}"
    )
    assert set(records["source"]) == {"avalanche_reports", "ice_reports"}


def test_saved_records_table_has_no_nve_rows():
    """Same guarantee, checked against whatever `records` actually is right
    now (local 02_data/tables/ or the bucket) — skipped when there's no data.
    """
    records = storage.load("records")
    if records.empty or "source" not in records.columns:
        return

    nve_sources = sorted(
        source for source in records["source"].unique() if str(source).startswith("nve_")
    )
    assert not nve_sources, f"records contains nve_* rows: {nve_sources}"
