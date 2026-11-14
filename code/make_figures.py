"""
Step 4 of the pipeline: saved rates -> headline table and figure (no API calls).

Usage (from the repo root)
  python code/make_figures.py poc_paid_20261025T012651Z

Reads   outputs/<run_id>_rates.csv           (written by code/poc_analyze.py)
Writes  outputs/<run_id>_summary_table.csv   emotion x prompt arm x model disposition effects
        outputs/<run_id>_summary_table.md    same table, for the README / audit
        outputs/<run_id>_disposition_by_persona.png
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"

# Odean (1998), Table I, entire-year sample: PGR 0.148 - PLR 0.098 (see README, "Human benchmark")
ODEAN_GAP_PP = 5.0

# Categorical slots 1-2 of the dataviz reference palette (validated, fixed order by model)
MODEL_COLORS = ["#2a78d6", "#eb6834"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def main(run_id: str) -> None:
    rates = pd.read_csv(OUTPUTS / f"{run_id}_rates.csv")
    manifest = json.loads((OUTPUTS / f"{run_id}_manifest.json").read_text())
    is_test = bool(manifest["is_test"])

    # ---- table ----------------------------------------------------------------------------
    summary = (rates[["model_id", "emotion", "prompt_arm", "persona_id", "n_gain", "n_loss",
                      "gain_sell_rate", "loss_sell_rate", "disposition_effect_pp"]]
               .sort_values(["model_id", "emotion", "prompt_arm"]))
    summary.to_csv(OUTPUTS / f"{run_id}_summary_table.csv", index=False)
    note = ("**SYNTHETIC DRY RUN: fixed hold/4 answers. Zeros are expected; not behavioral evidence.**\n\n"
            if is_test else "")
    (OUTPUTS / f"{run_id}_summary_table.md").write_text(
        f"# Disposition effect by persona and model: {run_id}\n\n{note}"
        "Disposition effect = gain sell rate - loss sell rate, in percentage points. "
        "Complete matched pairs only; at most 3 pairs per cell, so these are exploratory.\n\n"
        + summary.round(3).to_markdown(index=False) + "\n")

    # ---- figure: one horizontal bar per persona, one color per model ------------------------
    personas = (rates[["persona_id", "emotion", "prompt_arm"]].drop_duplicates()
                .sort_values(["emotion", "prompt_arm"]).persona_id.tolist())[::-1]
    models = sorted(rates["model_id"].unique())
    bar_h = 0.8 / max(len(models), 1)

    fig, ax = plt.subplots(figsize=(8, 0.55 * len(personas) + 1.6), dpi=150)
    for i, m in enumerate(models):
        sub = rates[rates.model_id == m].set_index("persona_id").reindex(personas)
        y = [k + (i - (len(models) - 1) / 2) * bar_h for k in range(len(personas))]
        # NaN (no complete pair) draws no bar; it is never plotted as a zero effect
        ax.barh(y, sub["disposition_effect_pp"], height=bar_h * 0.9,
                color=MODEL_COLORS[i % len(MODEL_COLORS)], label=m, zorder=3)
    ax.axvline(0, color=MUTED, lw=1, zorder=2)
    ax.axvline(ODEAN_GAP_PP, color=INK, lw=1, ls="--", zorder=2)
    ax.text(ODEAN_GAP_PP, len(personas) - 0.4, "  Odean (1998) humans: +5 pp",
            color=INK, fontsize=8, va="bottom")
    ax.set_yticks(range(len(personas)), personas, fontsize=8, color=INK)
    ax.set_xlim(-105, 105)
    ax.set_xlabel("Disposition effect (gain sell rate - loss sell rate, pp)", color=MUTED, fontsize=9)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8, length=0)
    title = "Do Inside Out personas sell winners more than losers?"
    if is_test:
        title += "\nSYNTHETIC DRY RUN - fixed answers, not evidence"
    ax.set_title(title, loc="left", fontsize=11, color=INK)
    ax.legend(title="Model", frameon=False, fontsize=8, title_fontsize=8, loc="lower right")
    fig.tight_layout()
    out = OUTPUTS / f"{run_id}_disposition_by_persona.png"
    fig.savefig(out)
    print(f"[make_figures] wrote {out.relative_to(ROOT)} and {run_id}_summary_table.csv/.md")


if __name__ == "__main__":
    main(sys.argv[1])
