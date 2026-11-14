"""
Inside Out Silicon Investors: v0 dashboard skeleton.

Reads ONLY saved files (outputs/ and data/raw/). It never calls a model API.
Run locally:   streamlit run dashboard/app.py
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS, RAW_DIR, INPUTS = ROOT / "outputs", ROOT / "data" / "raw", ROOT / "inputs"

st.set_page_config(page_title="Inside Out Silicon Investors", page_icon="📈", layout="wide")


# ------------------------------------------------------------------ data loading
@st.cache_data
def load_runs():
    return json.loads((OUTPUTS / "runs.json").read_text())


@st.cache_data
def load_run(run_id: str):
    d = dict(
        responses=pd.read_csv(OUTPUTS / f"{run_id}_responses.csv"),
        rates=pd.read_csv(OUTPUTS / f"{run_id}_rates.csv"),
        summary=pd.read_csv(OUTPUTS / f"{run_id}_summary_table.csv"),
        cost=pd.read_csv(OUTPUTS / f"{run_id}_cost_projection.csv"),
        feasibility=(OUTPUTS / f"{run_id}_feasibility.md").read_text(),
        manifest=json.loads((OUTPUTS / f"{run_id}_manifest.json").read_text()),
    )
    prompts = RAW_DIR / run_id / "prompts.csv"
    d["prompts"] = pd.read_csv(prompts) if prompts.exists() else None
    return d


runs = load_runs()
run_ids = [r["run_id"] for r in runs["runs"]]
with st.sidebar:
    run_id = st.selectbox("Run", run_ids, index=run_ids.index(runs["primary_run"]))
data = load_run(run_id)
is_test = bool(data["manifest"]["is_test"])
resp = data["responses"]


def synthetic_banner():
    if is_test:
        st.warning("**Synthetic dry run.** EDSL's free test model gave every persona the same fixed "
                   "answer (hold, rating 4), so every effect is zero by construction. This run checks "
                   "the plumbing only; it is not behavioral evidence. The paid pilot's raw files will "
                   "replace it.", icon="⚠️")


# ------------------------------------------------------------------ pages
def intro():
    st.title("Inside Out Silicon Investors")
    st.subheader("Do LLM investor personas sell winners faster than losers, and does it depend on "
                 "the emotion they are told to feel?")
    synthetic_banner()
    st.markdown(
        "Human investors show the **disposition effect**: they sell stocks that have gone up more readily "
        "than stocks that have gone down (Odean, 1998: +5 pp). We give LLM 'investors' an emotion from "
        "*Inside Out* (Joy, Sadness, Fear, Embarrassment, ...) and ask them to sell or hold a fictional stock "
        "that is either up or down by the same amount, with everything else identical.\n\n"
        "_Placeholder: a short plain-language summary of the headline finding goes here once the paid "
        "pilot data is loaded._")
    pairs = resp.pivot_table(index=["persona_id", "scenario_id", "model_id", "repeat"],
                             columns="version", values="sell_valid", aggfunc="first")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Survey observations", len(resp))
    c2.metric("Models", resp["model_id"].nunique())
    c3.metric("Valid sell/hold answers", f"{resp['sell_valid'].mean():.0%}")
    c4.metric("Complete gain/loss pairs", int((pairs.get("gain", False) & pairs.get("loss", False)).sum()))
    st.caption(f"Run `{run_id}` · started {data['manifest']['started_utc'][:16]} UTC · "
               f"EDSL {data['manifest'].get('edsl_version', '?')}")


def methodology():
    st.title("Methodology")
    st.markdown("""
**Design.** Each persona sees a fictional company in two versions that differ *only* in the sign of the
return since purchase (for example +10% vs −10%). The text says future expected return and risk equal the
market's and that past moves say nothing about the future; taxes and costs are excluded. The pipeline
asserts that the two texts are identical apart from the sign.

**Questions.** (1) Sell or hold (option order randomized with seed 331, fixed within a pair);
(2) likelihood to sell, 1–7. Each question is a fresh call with no memory.

**Outcome.**
""")
    st.latex(r"\text{disposition effect} = \Pr(\text{sell}\mid\text{gain}) - \Pr(\text{sell}\mid\text{loss})")
    st.markdown("""
Computed per persona × model on **complete matched pairs only**. Invalid answers are never treated as "hold".

**Pipeline** (`python run_all.py` rebuilds everything from `data/raw/` with no API calls):

| Step | File | Output |
|---|---|---|
| 1. Collect (paid, deliberate) | `code/poc_run.py` | `data/raw/<run_id>/` raw EDSL results, prompts, manifest |
| 2. Build dataset | `code/build_dataset.py` | `outputs/<run_id>_responses.csv` |
| 3. Analyze | `code/poc_analyze.py` | validity, pairs, rates, cost projection |
| 4. Figures/tables | `code/make_figures.py` | summary table + figure |
| 5. Dashboard | `dashboard/app.py` | this site |

**Benchmark.** Odean (1998), Table I: PGR 0.148 − PLR 0.098 = +5.0 pp. Our measure is an experimental
analogue, not a replication of the brokerage estimator.
""")
    st.subheader("Personas in this run")
    st.dataframe(pd.read_csv(INPUTS / "personas_poc.csv"), hide_index=True, use_container_width=True)
    st.subheader("Scenarios")
    st.dataframe(pd.read_csv(INPUTS / "scenarios_poc.csv"), hide_index=True, use_container_width=True)


def results():
    st.title("Results")
    synthetic_banner()
    st.image(str(OUTPUTS / f"{run_id}_disposition_by_persona.png"), use_container_width=True)
    st.caption("At most 3 matched pairs per bar: exploratory pilot magnitudes, no confidence intervals yet.")
    st.subheader("Disposition effect by persona and model")
    st.dataframe(data["summary"].round(3), hide_index=True, use_container_width=True)
    st.subheader("By emotion and prompt arm (averaged over scenarios)")
    s = data["summary"]
    st.dataframe(s.pivot_table(index=["emotion", "prompt_arm"], columns="model_id",
                               values="disposition_effect_pp").round(1), use_container_width=True)
    st.subheader("Cost and projection to the full design")
    st.dataframe(data["cost"], hide_index=True, use_container_width=True)
    with st.expander("Full feasibility report (validity, pairs, comment flags, hand check)"):
        st.markdown(data["feasibility"])


def explore():
    st.title("Explore the responses")
    synthetic_banner()
    c1, c2, c3, c4 = st.columns(4)
    models = c1.multiselect("Model", sorted(resp.model_id.unique()), default=sorted(resp.model_id.unique()))
    emotions = c2.multiselect("Emotion", sorted(resp.emotion.unique()), default=sorted(resp.emotion.unique()))
    arms = c3.multiselect("Prompt arm", sorted(resp.prompt_arm.unique()), default=sorted(resp.prompt_arm.unique()))
    versions = c4.multiselect("Version", ["gain", "loss"], default=["gain", "loss"])
    view = resp[resp.model_id.isin(models) & resp.emotion.isin(emotions)
                & resp.prompt_arm.isin(arms) & resp.version.isin(versions)]
    st.caption(f"{len(view)} of {len(resp)} rows")
    st.dataframe(view[["persona_id", "emotion", "prompt_arm", "scenario_id", "version", "signed_return_pct",
                       "model_id", "decision_raw", "sell", "sell_rating", "decision_comment"]],
                 hide_index=True, use_container_width=True)

    st.subheader("Side-by-side matched pair")
    c1, c2, c3 = st.columns(3)
    persona = c1.selectbox("Persona", sorted(resp.persona_id.unique()))
    scenario = c2.selectbox("Scenario", sorted(resp.scenario_id.unique()))
    model = c3.selectbox("Model ", sorted(resp.model_id.unique()))
    pair = resp[(resp.persona_id == persona) & (resp.scenario_id == scenario) & (resp.model_id == model)]
    cols = st.columns(2)
    for col, version in zip(cols, ["gain", "loss"]):
        row = pair[pair.version == version]
        with col:
            st.markdown(f"#### {version.title()}")
            if row.empty:
                st.info("No response saved for this version.")
                continue
            r = row.iloc[0]
            st.metric("Decision", str(r.decision_raw), f"sell rating {r.sell_rating_raw}", delta_color="off")
            st.markdown(f"**Model's comment:** {r.decision_comment if pd.notna(r.decision_comment) else '_none_'}")
            p = data["prompts"]
            if p is not None:
                pr = p[(p["agent.persona_id"] == persona) & (p["scenario.scenario_id"] == scenario)
                       & (p["scenario.version"] == version) & (p["model.model"] == model)]
                if len(pr):
                    with st.expander("Exact prompt sent to the model"):
                        st.text(pr.iloc[0]["prompt.decision_system_prompt"])
                        st.text(pr.iloc[0]["prompt.decision_user_prompt"])


pg = st.navigation([st.Page(intro, title="Intro", icon="🏠", default=True),
                    st.Page(methodology, title="Methodology", icon="🧪"),
                    st.Page(results, title="Results", icon="📊"),
                    st.Page(explore, title="Explore", icon="🔍")])
pg.run()
