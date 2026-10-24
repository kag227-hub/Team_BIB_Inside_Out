"""
Checkpoint 1 proof of concept: feasibility report from saved responses (no API calls).

Usage (from the repo root)
  python code/poc_analyze.py outputs/poc_2026-10-23_responses.csv

Writes, next to the input file:
  *_feasibility.md       parse rates, pair completeness, refusals/recitation flags, cost projection
  *_rates.csv            gain/loss sell rates and disposition effect by model x persona (PoC only: tiny n)
  *_cost_projection.csv  actual cost per observation scaled to the README's design sizes
"""

import sys
import json
from pathlib import Path

import pandas as pd

path = Path(sys.argv[1])
stem = path.name.replace("_responses.csv", "")
df = pd.read_csv(path)
out = path.parent
manifest_path = out / f"{stem}_manifest.json"
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
is_test = bool(manifest.get("is_test", stem.startswith("poc_TEST_")))

key = ["run_id", "persona_id", "scenario_id", "version", "model_id", "repeat"]
assert not df.duplicated(key).any(), "duplicate analysis keys"
assert not df[key].isna().any().any(), "missing analysis keys"
assert df["run_id"].nunique() == 1, "analyze one run at a time"
assert set(df["version"]) <= {"gain", "loss"}

lines = [f"# PoC feasibility report: {stem}", ""]
if is_test:
    lines += ["**SYNTHETIC DRY RUN: validates plumbing only. No behavioral evidence or paid spending.**", ""]

# 1. Parse / validity rates
valid = (df.groupby(["model_id", "prompt_arm"])
           .agg(n=("sell", "size"), sell_valid=("sell_valid", "mean"), rating_valid=("rating_valid", "mean"))
           .round(3))
lines += ["## 1. Valid answers (share of rows)", "", valid.to_markdown(), ""]

# 2. Pair completeness: both gain and loss valid for the same persona x scenario x model
pair_key = ["persona_id", "scenario_id", "model_id", "repeat"]
pairs = df.pivot_table(index=pair_key, columns="version", values="sell_valid", aggfunc="first")
if manifest:
    root = Path(__file__).resolve().parents[1]
    personas = pd.read_csv(root / manifest["personas_file"])
    scenarios = pd.read_csv(root / manifest["scenarios_file"])
    expected = pd.MultiIndex.from_product(
        [personas.persona_id, scenarios.scenario_id, manifest["models"], [0]], names=pair_key)
    pairs = pairs.reindex(expected)
pairs = pairs.reindex(columns=["gain", "loss"]).fillna(False).astype(bool)
complete = pairs["gain"] & pairs["loss"]
lines += ["## 2. Matched pairs", "",
          f"- Pairs expected: {len(pairs)}",
          f"- Complete pairs (both answers valid): {int(complete.sum())}",
          f"- Incomplete pairs: {int((~complete).sum())} (kept and reported, never dropped silently)", ""]

# 3. Character breaks / textbook recitation in the free-text comments
flags = {
    "mentions_theory": r"disposition effect|loss aversion|sunk cost|odean|prospect theory|behavioral finance",
    "breaks_character": r"as an ai|language model|i cannot|i can't provide|not financial advice",
}
for name, pat in flags.items():
    df[name] = df["decision_comment"].fillna("").str.contains(pat, case=False, regex=True)
flag_tbl = df.groupby(["model_id", "prompt_arm"])[list(flags)].mean().round(3)
lines += ["## 3. Comment flags (share of rows)", "", flag_tbl.to_markdown(), "",
          "Read 10 comments per model by hand too; regex flags miss things.", ""]

# 4. Sell rates and disposition effect (gain sell rate - loss sell rate). Tiny n: pipeline check only.
v = df[df["sell_valid"] & pd.MultiIndex.from_frame(df[pair_key]).isin(complete[complete].index)]
rates = (v.groupby(["model_id", "persona_id", "emotion", "prompt_arm", "version"])["sell"]
          .agg(["mean", "size"]).unstack("version"))
rates.columns = [f"{stat}_{ver}" for stat, ver in rates.columns]
rates = rates.rename(columns={"mean_gain": "gain_sell_rate", "mean_loss": "loss_sell_rate",
                              "size_gain": "n_gain", "size_loss": "n_loss"})
if {"gain_sell_rate", "loss_sell_rate"} <= set(rates.columns):
    rates["disposition_effect_pp"] = 100 * (rates["gain_sell_rate"] - rates["loss_sell_rate"])
rates.round(3).to_csv(out / f"{stem}_rates.csv")
lines += ["## 4. Sell rates (complete pairs only; at most 3 pairs per cell; exploratory)", "",
          rates.round(3).to_markdown() if len(rates) else "_No valid answers._", ""]

# 5. Cost: actual spend per survey observation, scaled to the README design sizes
cost_cols = [c for c in df.columns if c.endswith("_cost") and c.startswith("raw_model_response")]
tok_cols = [c for c in df.columns if c.endswith(("_input_tokens", "_output_tokens"))]
df["obs_cost_usd"] = df[cost_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
cached = [c for c in df.columns if c.startswith("cache_used")]
if is_test:
    # Fake model token prices are not invoices and must not drive projections.
    df["obs_cost_usd"] = 0.0
else:
    # EDSL may attach nominal response cost even when a cached answer was reused.
    for cost_col in cost_cols:
        question = cost_col.removeprefix("raw_model_response__").removesuffix("_cost")
        cache_col = f"cache_used__{question}_cache_used"
        if cache_col in df:
            df.loc[df[cache_col].eq(True), cost_col] = 0.0
    df["obs_cost_usd"] = df[cost_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
proj = []
for m, g in df.groupby("model_id"):
    uncached = ~g[cached].any(axis=1) if cached else pd.Series(True, index=g.index)
    per_obs = g.loc[uncached, "obs_cost_usd"].mean() if not is_test else float("nan")
    row = dict(model_id=m, observations=len(g), total_cost_usd=round(g["obs_cost_usd"].sum(min_count=1), 6),
               cost_per_obs_usd=per_obs,
               share_cached=round(g[cached].mean().mean(), 3) if cached else None)
    for t in tok_cols:
        row["mean_" + t.split("__")[-1]] = round(pd.to_numeric(g[t], errors="coerce").mean(), 1)
    # README design sizes are totals across BOTH models, so each model gets half
    for label, n_total in [("mvp_2000", 2000), ("arms_repeats_12000", 12000), ("full_36000", 36000)]:
        row[f"proj_{label}_usd"] = round(per_obs * n_total / 2, 2) if pd.notna(per_obs) else None
    proj.append(row)
proj = pd.DataFrame(proj)
proj.to_csv(out / f"{stem}_cost_projection.csv", index=False)
lines += ["## 5. Cost (actual) and projection to the full design", "", proj.to_markdown(index=False), "",
          "Synthetic runs have $0 spend and no cost extrapolation. Real-run projections use fully uncached observations only. "
          "Missing cost metadata remains unknown; provider/Expected Parrot billing must be reconciled separately.", ""]

# 6. Hand check: one matched pair, laid out for a teammate to verify against the prompts file
hc = df.sort_values(key).head(2)[["persona_id", "scenario_id", "version", "model_id",
                                  "decision_raw", "sell", "sell_rating_raw", "sell_rating", "obs_cost_usd"]]
lines += ["## 6. Hand-check pair (verify against *_prompts.csv and the raw results)", "",
          hc.to_markdown(index=False), ""]

(out / f"{stem}_feasibility.md").write_text("\n".join(lines))
print("\n".join(lines))
