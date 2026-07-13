"""Build the ETNF parquet catalog for the thebasemesh OpenUSD assets.

Essential Tuple Normal Form: one 1:1 relation keyed by a UUIDv5 `asset_uuid`, derived
from a stable natural key so a re-imported/rescaled duplicate resolves to the same id.
Keys are byte-compatible with the vsk-session-item-recommendation lake (same namespace
+ `asset:<natural_key>` rule), so this catalog can join that lake directly.

Usage: python build_etnf.py <models_dir> <download_urls.txt> <out.parquet>
"""

from __future__ import annotations

import re
import sys
import uuid
from pathlib import Path

import pandas as pd

# Fixed lake namespace (identical to vsk_recsys/data/etnf.py) so keys line up.
NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL,
    "https://github.com/V-Sekai-fire/vsk-session-item-recommendation-01",
)

SOURCE = "thebasemesh.com"
LICENSE = "CC0-1.0"


def asset_uuid(natural_key: str) -> str:
    return str(uuid.uuid5(NAMESPACE, f"asset:{natural_key}"))


def _name_from_url(url: str) -> str:
    m = re.search(r"dn=([^&]+)\.zip", url)
    return m.group(1) if m else ""


def build(models_dir: str, urls_file: str, out: str) -> pd.DataFrame:
    archive_by_name = {}
    for line in Path(urls_file).read_text().splitlines():
        name = _name_from_url(line.strip())
        if name:
            archive_by_name[name] = line.strip()

    rows = []
    for usd in sorted(Path(models_dir).glob("*.usda")):
        name = usd.stem
        natural_key = f"basemesh:{name}"
        rows.append(
            {
                "asset_uuid": asset_uuid(natural_key),
                "natural_key": natural_key,
                "name": name,
                "usd_file": f"models/{name}.usda",
                "source": SOURCE,
                "source_archive_url": archive_by_name.get(name, ""),
                "asset_page_url": f"https://www.thebasemesh.com/asset/{name.replace('_', '-')}",
                "up_axis": "Y",
                "forward_axis": "-Z",
                "handedness": "right",
                "meters_per_unit": 1.0,
                "license": LICENSE,
            }
        )

    frame = pd.DataFrame(rows)
    if frame["asset_uuid"].nunique() != len(frame):
        raise SystemExit("PK collision: asset_uuid not unique")
    frame.to_parquet(out, index=False)
    print(f"wrote {out}: {len(frame)} assets, PK-unique")
    print(frame[["asset_uuid", "natural_key", "up_axis", "handedness"]].head(3).to_string(index=False))
    return frame


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3])
