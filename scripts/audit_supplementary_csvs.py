#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def table_sort_key(path: Path) -> tuple[int, int, str]:
    match = re.search(r"_S(\d+)(B?)_", path.name)
    if not match:
        return (10_000, 0, path.name)
    return (int(match.group(1)), 1 if match.group(2) else 0, path.name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit supplementary CSV structure and regenerate SHA-256 manifests."
    )
    parser.add_argument(
        "--supp-dir",
        type=Path,
        default=REPOSITORY_ROOT / "supplementary",
        help="Directory containing Supplementary_Table_*.csv files.",
    )
    args = parser.parse_args()
    supp = args.supp_dir.resolve()
    if not supp.is_dir():
        raise SystemExit(f"Supplementary directory not found: {supp}")

    rows: list[dict[str, object]] = []
    for path in sorted(supp.glob("Supplementary_Table_*.csv"), key=table_sort_key):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            raw_rows = list(csv.reader(handle))
        header_width = len(raw_rows[0]) if raw_rows else 0
        consistent = bool(raw_rows) and all(
            len(row) == header_width for row in raw_rows[1:]
        )
        match = re.search(r"_S(\d+B?)_", path.name)
        rows.append(
            {
                "file": path.name,
                "table_id": f"S{match.group(1)}" if match else "",
                "data_rows": max(0, len(raw_rows) - 1),
                "columns": header_width,
                "consistent_columns": str(consistent),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    if not rows:
        raise SystemExit(f"No Supplementary_Table_*.csv files found in {supp}")

    fields = [
        "file",
        "table_id",
        "data_rows",
        "columns",
        "consistent_columns",
        "size_bytes",
        "sha256",
    ]
    for name in [
        "supplementary_manifest.csv",
        "00_supplementary_csv_integrity_audit.csv",
    ]:
        with (supp / name).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    if not all(row["consistent_columns"] == "True" for row in rows):
        raise SystemExit("At least one supplementary CSV has inconsistent columns.")
    print(
        f"Audited {len(rows)} supplementary CSV files; "
        "all column counts are consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
