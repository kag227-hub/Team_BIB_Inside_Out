"""
Step 2 of the pipeline: raw EDSL results -> tidy analysis dataset (no API calls).

One output row = one persona's answers to one scenario version (gain or loss) from one model
and repeat. Invalid or refused answers stay as NaN with a validity flag; they never become "hold".

Usage (from the repo root)
  python code/build_dataset.py poc_paid_20261025T012651Z

Reads   data/raw/<run_id>/raw_results.csv and data/raw/<run_id>/manifest.json
Writes  outputs/<run_id>_responses.csv and outputs/<run_id>_manifest.json
"""

import ast
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR, OUTPUTS = ROOT / "data" / "raw", ROOT / "outputs"

SELL, HOLD = "Sell the position", "Hold the position"
KEY = ["run_id", "persona_id", "scenario_id", "version", "model_id", "repeat"]


def _options(x):
    """decision_options is a list in memory but a string like "['Sell..', 'Hold..']" in CSV."""
    if isinstance(x, str):
        x = ast.literal_eval(x)
    return "|".join(x)


def tidy_from_raw(raw: pd.DataFrame, run_id: str, is_test: bool, started_utc: str) -> pd.DataFrame:
    def col(name):
        return raw[name] if name in raw.columns else pd.NA

    tidy = pd.DataFrame({
        "run_id": run_id,
        "is_test": is_test,
        "persona_id": col("agent.persona_id"),
        "emotion": col("agent.emotion"),
        "background": col("agent.background"),
        "prompt_arm": col("agent.prompt_arm"),
        "is_control": col("agent.is_control"),
        "scenario_id": col("scenario.scenario_id"),
        "version": col("scenario.version"),
        "signed_return_pct": col("scenario.signed_return_pct"),
        "abs_return_pct": col("scenario.abs_return_pct"),
        "prompt_hash": col("scenario.prompt_hash"),
        "model_id": col("model.model"),
        "repeat": 0,
        "decision_raw": col("answer.decision"),
        "decision_comment": col("comment.decision_comment"),
        "sell_rating_raw": col("answer.sell_rating"),
        "option_order": col("scenario.decision_options").map(_options),
        "run_started_utc": started_utc,
    })
    tidy["sell"] = tidy["decision_raw"].map({SELL: 1, HOLD: 0})  # anything else -> NaN, never "hold"
    tidy["sell_valid"] = tidy["sell"].notna()
    rating = pd.to_numeric(tidy["sell_rating_raw"], errors="coerce")
    tidy["sell_rating"] = rating.where(rating.between(1, 7) & rating.mod(1).eq(0))
    tidy["rating_valid"] = tidy["sell_rating"].notna()

    # usage / cost / cache columns: names vary by EDSL version, so keep whatever exists
    for c in raw.columns:
        if any(k in c for k in ("cost", "tokens", "cache_used", "cache_keys")) and "comment" not in c:
            tidy[c.replace(".", "__")] = raw[c].values

    assert not tidy[KEY].isna().any().any(), "missing analysis identifiers"
    assert not tidy.duplicated(KEY).any(), "analysis key is not unique"
    assert set(tidy["version"]) <= {"gain", "loss"}, "unexpected scenario version"
    return tidy


def build(run_id: str) -> Path:
    run_dir = RAW_DIR / run_id
    raw = pd.read_csv(run_dir / "raw_results.csv")
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["run_id"] == run_id, "manifest belongs to a different run"
    tidy = tidy_from_raw(raw, run_id, bool(manifest["is_test"]), manifest["started_utc"])
    assert len(tidy) == manifest["n_observations"], "row count does not match the manifest"

    OUTPUTS.mkdir(exist_ok=True)
    out = OUTPUTS / f"{run_id}_responses.csv"
    tidy.to_csv(out, index=False)
    shutil.copy(run_dir / "manifest.json", OUTPUTS / f"{run_id}_manifest.json")
    print(f"[build_dataset] {run_id}: {len(raw)} raw rows -> {len(tidy)} tidy rows -> {out.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    build(sys.argv[1])
