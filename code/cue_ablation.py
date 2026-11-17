"""
Demand-cue ablation (instructor audit A3, self-audit F6): disposition effect with and without
each cue. No API calls.

Usage (from the repo root)
  python code/cue_ablation.py poc_ablation_<timestamp>

Reads   outputs/<run_id>_responses.csv   (written by code/build_dataset.py)
Writes  outputs/<run_id>_cue_ablation.csv   one row per model x persona x estimate
        outputs/<run_id>_cue_ablation.md    same, for the README / audit response

Cues (see code/poc_run.py):
  cue_past_moves   scenario says past price moves "say nothing about its future" (1) or not (0)
  cue_system_line  EDSL's "Do not break character" instruction is present (1) or removed (0)

Estimates, separately for each model and persona (and pooled over the personas):
  DE[cell]              gain sell rate - loss sell rate in that cue cell, pp (complete pairs only)
  remove_past_moves     mean over cue_system_line levels of DE[past=0] - DE[past=1]
  remove_system_line    mean over cue_past_moves levels of DE[sys=0]  - DE[sys=1]
  interaction           (DE[0,0] - DE[1,0]) - (DE[0,1] - DE[1,1])
A positive "remove_*" estimate means the disposition effect is larger without that cue.

Inference follows ANALYSIS_PLAN.md: the contrast is first averaged within each base scenario,
then a percentile bootstrap over base scenarios (B = 10,000, seed 331) gives a 95% interval.
Labeled exploratory (ANALYSIS_PLAN.md, S8).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
CUES = ["cue_past_moves", "cue_system_line"]
CELLS = [(1, 1), (0, 1), (1, 0), (0, 0)]
B, SEED = 10_000, 331

# weights on the four cells (past, sys) for each estimate
WEIGHTS = {
    "DE_both_cues": {(1, 1): 1},
    "DE_no_past_moves": {(0, 1): 1},
    "DE_no_system_line": {(1, 0): 1},
    "DE_no_cues": {(0, 0): 1},
    "remove_past_moves": {(0, 1): .5, (0, 0): .5, (1, 1): -.5, (1, 0): -.5},
    "remove_system_line": {(1, 0): .5, (0, 0): .5, (1, 1): -.5, (0, 1): -.5},
    "interaction": {(0, 0): 1, (1, 0): -1, (0, 1): -1, (1, 1): 1},
}


def pair_diffs(df: pd.DataFrame) -> pd.DataFrame:
    """One row per complete gain/loss pair with d = sell_gain - sell_loss (in {-1, 0, 1})."""
    ids = ["model_id", "persona_id", "scenario_id", "repeat"] + CUES
    valid = df[df["sell_valid"].astype(bool)]
    wide = valid.pivot(index=ids, columns="version", values="sell").reindex(columns=["gain", "loss"])
    wide = wide.dropna()
    wide["d"] = wide["gain"] - wide["loss"]
    return wide.reset_index()


def scenario_contrast(d: pd.DataFrame, weights: dict) -> pd.Series:
    """Contrast per base scenario: weighted sum of cell means of d. NaN if a needed cell is empty."""
    cell = d.groupby(["scenario_id"] + CUES)["d"].mean().unstack(CUES)
    total = pd.Series(0.0, index=cell.index)
    for c, w in weights.items():
        col = cell[c] if c in cell.columns else pd.Series(np.nan, index=cell.index)
        total = total + w * col
    return total


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    if len(values) < 2:
        return np.nan, np.nan
    draws = rng.choice(values, size=(B, len(values)), replace=True).mean(axis=1)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return lo, hi


def summarize(d: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    groups = [(m, p, g) for (m, p), g in d.groupby(["model_id", "persona_id"])]
    groups += [(m, "pooled (equal weight per persona)", g) for m, g in d.groupby("model_id")]
    for model, persona, g in groups:
        if persona.startswith("pooled"):
            # equal weight per persona: average each persona's scenario-level contrast
            per = {}
            for est, w in WEIGHTS.items():
                s = pd.concat([scenario_contrast(gp, w) for _, gp in g.groupby("persona_id")], axis=1)
                per[est] = s.mean(axis=1, skipna=False)
        else:
            per = {est: scenario_contrast(g, w) for est, w in WEIGHTS.items()}
        for est, s in per.items():
            vals = s.dropna().to_numpy()
            lo, hi = bootstrap_ci(vals, rng)
            rows.append(dict(model_id=model, persona_id=persona, estimate=est,
                             value_pp=100 * vals.mean() if len(vals) else np.nan,
                             ci95_lo_pp=100 * lo, ci95_hi_pp=100 * hi,
                             n_scenarios=len(vals),
                             n_pairs=int(sum(len(g[(g.cue_past_moves == c[0]) & (g.cue_system_line == c[1])])
                                             for c in WEIGHTS[est]))))
    return pd.DataFrame(rows)


def main(run_id: str) -> None:
    df = pd.read_csv(OUTPUTS / f"{run_id}_responses.csv")
    cells = set(map(tuple, df[CUES].drop_duplicates().to_numpy()))
    assert cells == set(CELLS), f"{run_id} is not a full 2 x 2 cue ablation: {sorted(cells)}"
    is_test = bool(df["is_test"].iloc[0])
    table = summarize(pair_diffs(df))
    table.to_csv(OUTPUTS / f"{run_id}_cue_ablation.csv", index=False)

    note = ("**SYNTHETIC DRY RUN: fixed hold/4 answers. Zeros are expected; not behavioral evidence.**\n\n"
            if is_test else "")
    (OUTPUTS / f"{run_id}_cue_ablation.md").write_text(
        f"# Demand-cue ablation: {run_id}\n\n{note}"
        "Audit A3. DE = gain sell rate - loss sell rate (pp), complete matched pairs only. "
        "`remove_X` = DE without cue X minus DE with it, averaged over the other cue. "
        "95% interval: percentile bootstrap over base scenarios (B = 10,000, seed 331). "
        "Exploratory (ANALYSIS_PLAN.md, S8); with few base scenarios the intervals are coarse.\n\n"
        + table.round(1).to_markdown(index=False) + "\n")
    print(f"[cue_ablation] wrote outputs/{run_id}_cue_ablation.csv/.md")


if __name__ == "__main__":
    main(sys.argv[1])
