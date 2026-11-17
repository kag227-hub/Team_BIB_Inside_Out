"""
Rebuild every output from the committed raw data. No API calls, no spending.

    python run_all.py

For each run folder in data/raw/ that contains raw_results.csv:
  1. delete that run's old files in outputs/          (rebuild from scratch)
  2. code/build_dataset.py  raw EDSL results -> outputs/<run_id>_responses.csv
  3. code/poc_analyze.py    validity, matched pairs, sell rates, cost -> *_feasibility.md, *_rates.csv
  4. code/make_figures.py   headline table + figure -> *_summary_table.*, *_disposition_by_persona.png
  5. code/cue_ablation.py   (cue-ablation runs only, audit A3) DE with/without each cue -> *_cue_ablation.*
Then writes outputs/runs.json, which the dashboard reads to know which runs exist.

Collecting NEW responses is a separate, deliberate step that costs money:
    python code/poc_run.py --run-id <new_id>       (paid; asks for confirmation)
    python code/poc_run.py --test --run-id <id>    (free synthetic plumbing check)
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR, OUTPUTS = ROOT / "data" / "raw", ROOT / "outputs"


def step(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL if args[0].endswith("poc_analyze.py") else None)


def main() -> None:
    runs = sorted(d.name for d in RAW_DIR.iterdir() if (d / "raw_results.csv").exists())
    if not runs:
        raise SystemExit("No raw runs found in data/raw/. See README, 'Data'.")
    OUTPUTS.mkdir(exist_ok=True)

    summary = []
    for run_id in runs:
        for old in OUTPUTS.glob(f"{run_id}_*"):
            old.unlink()
        step("code/build_dataset.py", run_id)
        step("code/poc_analyze.py", f"outputs/{run_id}_responses.csv")
        print(f"[poc_analyze] wrote outputs/{run_id}_feasibility.md, _rates.csv, _cost_projection.csv")
        step("code/make_figures.py", run_id)
        manifest = json.loads((RAW_DIR / run_id / "manifest.json").read_text())
        if manifest.get("design") == "cue_ablation":
            step("code/cue_ablation.py", run_id)
        summary.append(dict(run_id=run_id, is_test=bool(manifest["is_test"]),
                            started_utc=manifest["started_utc"], models=manifest["models"],
                            n_observations=manifest["n_observations"]))

    # The dashboard shows a real (paid) run by default; synthetic runs only if nothing else exists.
    real = [r for r in summary if not r["is_test"]]
    primary = (real or summary)[-1]["run_id"]
    (OUTPUTS / "runs.json").write_text(json.dumps(dict(primary_run=primary, runs=summary), indent=2))
    print(f"\nDone. {len(runs)} run(s) rebuilt. Dashboard default run: {primary}")
    if not real:
        print("WARNING: only synthetic runs are in data/raw/. Add the paid pilot's raw files "
              "(see README) to get behavioral results.")


if __name__ == "__main__":
    main()
