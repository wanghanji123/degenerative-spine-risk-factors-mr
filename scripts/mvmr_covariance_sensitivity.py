#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path


OUTCOMES = {
    "finn_b_M13_INTERVERTEB": "Intervertebral disc disorders",
    "finn_b_M13_SPINSTENOSIS": "Spinal stenosis",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def as_float(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {key}")
    return value


def conditional_f(
    rows: list[dict[str, str]],
    target_beta: str,
    other_beta: str,
    target_se: str,
    other_se: str,
    rho: float,
) -> tuple[float, float, float]:
    numerator = sum(as_float(row, other_beta) * as_float(row, target_beta) for row in rows)
    denominator = sum(as_float(row, other_beta) ** 2 for row in rows)
    delta = numerator / denominator
    q_value = 0.0
    min_variance = math.inf
    for row in rows:
        se_target = as_float(row, target_se)
        se_other = as_float(row, other_se)
        covariance = rho * se_target * se_other
        variance = se_target**2 + delta**2 * se_other**2 - 2.0 * delta * covariance
        if variance <= 0:
            raise ValueError(f"Non-positive residual variance at rho={rho}")
        residual = as_float(row, target_beta) - delta * as_float(row, other_beta)
        q_value += residual**2 / variance
        min_variance = min(min_variance, variance)
    return q_value / len(rows), delta, min_variance


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvmr-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--rho-grid",
        default="-0.9,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,0.9",
        help="Assumed constant correlation between SNP-BMI and SNP-smoking estimation errors.",
    )
    args = parser.parse_args()

    mvmr_dir = Path(args.mvmr_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    rho_grid = [float(value) for value in args.rho_grid.split(",")]
    results: list[dict[str, object]] = []
    input_manifest: list[dict[str, object]] = []

    for clean_id, label in OUTCOMES.items():
        path = mvmr_dir / "data_processed" / f"mvmr_matrix_{clean_id}.csv"
        all_rows = read_csv(path)
        rows = [row for row in all_rows if str(row.get("mvmr_keep", "")).lower() in {"true", "1"}]
        if not rows:
            raise RuntimeError(f"No retained MVMR rows in {path}")
        input_manifest.append(
            {
                "outcome": label,
                "input_path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "rows_total": len(all_rows),
                "rows_retained": len(rows),
            }
        )
        for rho in rho_grid:
            f_bmi, delta_bmi, min_var_bmi = conditional_f(
                rows, "beta_bmi", "beta_smoking_initiation", "se_bmi", "se_smoking_initiation", rho
            )
            f_smoking, delta_smoking, min_var_smoking = conditional_f(
                rows, "beta_smoking_initiation", "beta_bmi", "se_smoking_initiation", "se_bmi", rho
            )
            for exposure, f_value, delta, min_variance in (
                ("BMI", f_bmi, delta_bmi, min_var_bmi),
                ("Smoking initiation", f_smoking, delta_smoking, min_var_smoking),
            ):
                results.append(
                    {
                        "outcome": label,
                        "exposure": exposure,
                        "n_snps": len(rows),
                        "assumed_error_correlation_rho": rho,
                        "conditional_F": f_value,
                        "above_conventional_F10": f_value >= 10.0,
                        "projection_delta": delta,
                        "minimum_residual_variance": min_variance,
                        "covariance_model": "cov(beta_BMI,beta_smoking)=rho*se_BMI*se_smoking for every SNP",
                        "interpretation": (
                            "Stress-test only; rho is assumed, not estimated. "
                            "Public summary data do not identify the true SNP-exposure covariance."
                        ),
                    }
                )

    result_path = output_dir / "mvmr_conditional_F_covariance_sensitivity.csv"
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    manifest_path = output_dir / "mvmr_covariance_sensitivity_input_manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(input_manifest[0]))
        writer.writeheader()
        writer.writerows(input_manifest)

    grouped: dict[str, list[float]] = {}
    for row in results:
        key = f"{row['outcome']} | {row['exposure']}"
        grouped.setdefault(key, []).append(float(row["conditional_F"]))
    summary = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "rho_grid": rho_grid,
        "model": "Constant cross-exposure estimation-error correlation stress test",
        "scope": (
            "Assesses sensitivity of conditional F statistics to assumed SNP-exposure covariance. "
            "Does not estimate exact covariance or participant overlap."
        ),
        "ranges": {
            key: {
                "minimum_conditional_F": min(values),
                "maximum_conditional_F": max(values),
                "all_above_10": all(value >= 10.0 for value in values),
            }
            for key, values in grouped.items()
        },
        "result_sha256": sha256(result_path),
        "input_manifest_sha256": sha256(manifest_path),
    }
    (output_dir / "mvmr_covariance_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
