"""Public dashboard: reads the approved cell-level export only."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Inside Out Silicon Investors", page_icon="📈", layout="wide")
artifact = Path(__file__).resolve().parents[1] / "outputs" / "public_paid_pilot.json"
pilot = json.loads(artifact.read_text(encoding="utf-8"))
cells = pd.DataFrame(pilot["cells"])
n = cells["complete_pairs"].where(cells["complete_pairs"] > 0)
cells["gain_sell_pct"] = 100 * cells["gain_sells"] / n
cells["loss_sell_pct"] = 100 * cells["loss_sells"] / n
cells["gap_pp"] = 100 * (cells["gain_sells"] - cells["loss_sells"]) / n
labels = {"model_id": "Model", "emotion": "Emotion", "prompt_arm": "Prompt arm",
          "complete_pairs": "Matched pairs", "gain_sells": "Gain sells", "loss_sells": "Loss sells",
          "gain_sell_pct": "Gain sell rate (%)", "loss_sell_pct": "Loss sell rate (%)",
          "gap_pp": "Gain minus loss (pp)"}


def intro():
    st.title("Inside Out Silicon Investors")
    st.subheader("Do simulated investors sell winners more often than losers?")
    st.info("Exploratory results from the October paid model pilot.")
    a, b, c = st.columns(3)
    a.metric("Model responses", pilot["observations"])
    b.metric("Matched gain/loss pairs", int(cells["complete_pairs"].sum()))
    c.metric("Models", cells["model_id"].nunique())
    st.caption("October 24, 2026 (ET) · Three pairs per model, emotion, and prompt-arm cell.")
    st.write("With three pairs per cell, one changed answer moves a sell rate by about 33 percentage "
             "points. These results can guide the next experiment; they do not establish an effect.")


def methodology():
    st.title("Methodology")
    st.write("Nine investor personas evaluated three fictional scenarios in matched gain and loss "
             "versions. The experiment compared two models, character names versus emotion "
             "descriptions, and a separate neutral control.")
    st.write("Each sell rate is the number of sells divided by the number of pairs with valid "
             "gain and loss decisions. The gap is the gain sell rate minus the loss sell rate.")
    st.write("This public app reads aggregate counts. Response-level records are kept separate "
             "for course verification. Model choices are hypothetical; they are not brokerage trades.")


def results():
    st.title("Results")
    st.caption("Exploratory paid pilot. Positive gaps indicate more selling after gains.")
    view = cells[list(labels)].round(1).rename(columns=labels)
    st.dataframe(view, hide_index=True)


def explore():
    st.title("Explore by model, emotion, and prompt arm")
    view = cells.copy()
    selectors = st.columns(3)
    for container, column in zip(selectors, ("model_id", "emotion", "prompt_arm")):
        values = sorted(cells[column].unique())
        chosen = container.multiselect(labels[column], values, default=values)
        view = view[view[column].isin(chosen)]
    if view.empty:
        st.info("No cells match those filters.")
        return
    chart = view.assign(cell=view["model_id"] + " / " + view["emotion"] + " / " + view["prompt_arm"])
    st.bar_chart(chart.set_index("cell")[["gain_sell_pct", "loss_sell_pct"]].rename(columns=labels),
                 horizontal=True, stack=False, x_label="Sell rate (%)", y_label="Pilot cell")
    st.dataframe(view[list(labels)].round(1).rename(columns=labels), hide_index=True)


st.navigation([st.Page(intro, title="Intro", default=True),
               st.Page(methodology, title="Methodology"),
               st.Page(results, title="Results"),
               st.Page(explore, title="Explore")]).run()
