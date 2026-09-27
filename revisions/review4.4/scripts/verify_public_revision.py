"""Portable aggregate-only checks. Does not reproduce SNP-level MR fits."""
from pathlib import Path
import csv, hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, condition):
    checks.append({"check": name, "pass": bool(condition)})

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

manifest = rows(ROOT / "MANIFEST.csv")
for record in manifest:
    path = (ROOT / record["path"]).resolve()
    assert path.is_relative_to(ROOT.resolve()), "Unsafe manifest path"
    check("SHA256 " + record["path"], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"])

m = rows(ROOT / "analysis/MVMR_repaired_results.csv")
check("four exploratory MVMR rows", len(m) == 4)
for r in m:
    label = r["exposure"] + " " + r["outcome_id"]
    check("429 SNPs " + label, int(r["n_snps"]) == 429)
    check("OR exponentiation " + label, math.isclose(math.exp(float(r["beta"])), float(r["OR"]), rel_tol=1e-10))
    check("CI covers estimate " + label, float(r["CI_lower"]) < float(r["OR"]) < float(r["CI_upper"]))
    if r["exposure"] == "Smoking initiation":
        check("weak smoking conditional F " + label, float(r["conditional_F_gencov0"]) < 10)
g = rows(ROOT / "analysis/MVMR_repaired_covariance_grid.csv")
check("76 covariance scenarios", len(g) == 76)
check("smoking remains weak across grid", all(float(r["conditional_F"]) < 10 for r in g if r["exposure"] == "Smoking initiation"))
s3 = rows(next((ROOT / "supplementary").glob("Supplementary_Table_S3_*.csv")))
check("unverified pain OR absent", all(r["id.outcome"] != "ukb-b-8463" for r in s3))
primary = [r for r in s3 if r["method"] == "Inverse variance weighted" and r["exposure_run"] in ["BMI", "Smoking initiation"] and r["id.outcome"] in ["finn-b-M13_INTERVERTEB", "finn-b-M13_SPINSTENOSIS"]]
check("four primary IVW rows", len(primary) == 4)
check("four primary tests below 0.0125", all(float(r["pval"]) < .0125 for r in primary))
result = {"checks": len(checks), "passed": sum(r["pass"] for r in checks), "failed": [r["check"] for r in checks if not r["pass"]], "scope": "Aggregate identity and consistency only. No raw-data fit, author approval, or validation of causal assumptions."}
print(json.dumps(result, indent=2))
raise SystemExit(bool(result["failed"]))
