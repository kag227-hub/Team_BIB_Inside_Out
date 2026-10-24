"""
Checkpoint 1 proof of concept: Inside Out personas x matched gain/loss scenarios x 2 models.

What it does
  1. Loads inputs/personas_poc.csv, inputs/scenarios_poc.csv, inputs/models_poc.csv
  2. Expands every base scenario into a GAIN and a LOSS version and asserts that the two
     rendered texts differ ONLY in the sign of the return
  3. Builds an EDSL survey (sell/hold + 1-7 likelihood to sell), prints EDSL's cost estimate
  4. Runs it, saves the raw EDSL results untouched, then writes one tidy row per
     persona x scenario x version x model to outputs/poc_responses.csv

Usage (from the repo root)
  python code/poc_run.py --test        # free dry run with EDSL's built-in "test" model (fake answers)
  python code/poc_run.py               # real run with the models in inputs/models_poc.csv (costs money)

Real runs need your Expected Parrot key in the environment (EXPECTED_PARROT_API_KEY), like HW5.
Never commit the key.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import random
from pathlib import Path

import pandas as pd
from edsl import (Agent, AgentList, Cache, Model, ModelList, QuestionLinearScale,
                  QuestionMultipleChoice, Scenario, ScenarioList, Survey)

ROOT = Path(__file__).resolve().parents[1]
INPUTS, OUTPUTS = ROOT / "inputs", ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

SCENARIO_TEMPLATE = (
    "You bought shares of {company}, a fictional {industry} company, {holding_period} ago. "
    "Since you bought them, your position has returned {signed_return}. "
    "Analysts agree that the stock's expected return and risk over the next year are the same as "
    "the overall market's, and that its past price moves say nothing about its future. "
    "Ignore taxes and trading costs. You do not need the cash. If you sell, the money goes into a "
    "broad stock index fund with the same expected return and risk."
)

SELL, HOLD = "Sell the position", "Hold the position"


def synthetic_response(user_prompt, system_prompt, files_list):
    """Valid fixed answers for plumbing checks; never experimental evidence."""
    return "4" if "How likely are you to sell" in user_prompt else HOLD


def build_scenarios(scen: pd.DataFrame, seed: int = 331) -> list[dict]:
    rows = []
    rng = random.Random(seed)
    for r in scen.itertuples(index=False):
        texts = {}
        options = [SELL, HOLD]
        rng.shuffle(options)
        for version, sign in [("gain", "+"), ("loss", "-")]:
            signed = f"{sign}{r.abs_return_pct}%"
            text = SCENARIO_TEMPLATE.format(company=r.company, industry=r.industry,
                                            holding_period=r.holding_period, signed_return=signed)
            texts[version] = text
            rows.append(dict(scenario_id=r.scenario_id, version=version,
                             signed_return_pct=float(f"{sign}{r.abs_return_pct}"),
                             abs_return_pct=r.abs_return_pct, holding_period=r.holding_period,
                             scenario_text=text,
                             decision_options=options,
                             prompt_hash=hashlib.sha256(text.encode()).hexdigest()[:12]))
        # Audit check: the pair must be identical once the signed return is removed
        g = texts["gain"].replace(f"+{r.abs_return_pct}%", "<RET>")
        l = texts["loss"].replace(f"-{r.abs_return_pct}%", "<RET>")
        assert g == l, f"{r.scenario_id}: gain and loss texts differ beyond the sign"
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="use EDSL's free fake 'test' model")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation prompt")
    ap.add_argument("--plan", action="store_true", help="save a planning estimate; no model calls")
    ap.add_argument("--run-id", help="unique artifact prefix; existing runs cannot be overwritten")
    args = ap.parse_args()

    personas = pd.read_csv(INPUTS / "personas_poc.csv")
    scen = pd.read_csv(INPUTS / "scenarios_poc.csv")
    models_tbl = pd.read_csv(INPUTS / "models_poc.csv")
    assert personas["persona_id"].is_unique and scen["scenario_id"].is_unique
    assert len(models_tbl) == 2 and models_tbl["model_id"].is_unique
    assert scen["abs_return_pct"].isin([5, 10, 20]).all()

    # Per-call assumptions, not measured tokens or a guaranteed spending cap.
    estimates = models_tbl[["model_id", "price_source", "price_checked"]].copy()
    estimates["observations"] = len(personas) * len(scen) * 2
    estimates["requests"] = estimates["observations"] * 2
    estimates["assumed_input_tokens_per_request"] = 2000
    estimates["assumed_output_tokens_per_request"] = 500
    estimates["estimated_usd"] = estimates["requests"] * (
        2000 * models_tbl["input_usd_per_million"]
        + 500 * models_tbl["output_usd_per_million"]) / 1_000_000
    print(estimates[["model_id", "observations", "requests", "estimated_usd"]].to_string(index=False))
    if args.plan:
        estimates.to_csv(OUTPUTS / "poc_planning_estimate.csv", index=False)
        return
    if not args.test and not os.getenv("EXPECTED_PARROT_API_KEY"):
        raise SystemExit("Paid run requires EXPECTED_PARROT_API_KEY in the environment or ignored .env. No calls made.")

    scenario_rows = build_scenarios(scen)
    scenarios = ScenarioList([Scenario(d) for d in scenario_rows])

    # Only persona_text is shown to the model; the other traits ride along as metadata
    agents = AgentList([
        Agent(name=p.persona_id,
              traits=dict(persona_id=p.persona_id, emotion=p.emotion, background=p.background,
                          prompt_arm=p.prompt_arm, is_control=int(p.is_control),
                          persona_text=p.persona_text),
              traits_presentation_template="{{ persona_text }}")
        for p in personas.itertuples(index=False)
    ])

    if args.test:
        models = ModelList([Model("test", func=synthetic_response)])
        run_id = "poc_TEST_" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    else:
        selected = []
        for m in models_tbl.itertuples(index=False):
            settings = dict(max_tokens=int(m.max_tokens))
            if m.service == "openai":
                settings.update(temperature=float(m.temperature), reasoning_effort=m.reasoning_effort)
            elif m.service == "anthropic":
                settings.update(thinking={"type": "adaptive"}, output_config={"effort": m.reasoning_effort})
            selected.append(Model(m.model_id, service_name=m.service, **settings))
        models = ModelList(selected)
        run_id = "poc_" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if args.run_id:
        assert Path(args.run_id).name == args.run_id and args.run_id not in (".", "..")
        run_id = args.run_id
    assert not list(OUTPUTS.glob(f"{run_id}_*")), "Run ID already exists; choose a new one"

    q_decision = QuestionMultipleChoice(
        question_name="decision",
        question_text="{{ scenario.scenario_text }}\n\nWhat do you do with this position today?",
        question_options="{{ scenario.decision_options }}",
        include_comment=True,  # keep the reasoning so we can check for textbook recitation
    )
    q_rating = QuestionLinearScale(
        question_name="sell_rating",
        question_text="{{ scenario.scenario_text }}\n\nHow likely are you to sell this position today?",
        question_options=[1, 2, 3, 4, 5, 6, 7],
        option_labels={1: "Very unlikely", 7: "Very likely"},
        include_comment=False,
    )
    # No memory between questions: each question is its own fresh call
    survey = Survey([q_decision, q_rating])
    job = survey.by(scenarios).by(agents).by(models)

    n_obs = len(scenarios) * len(agents) * len(models)
    print(f"run_id={run_id}: {len(agents)} personas x {len(scenarios)} scenario versions x "
          f"{len(models)} models = {n_obs} survey observations ({2 * n_obs} model calls)")
    if not args.test:
        try:
            cost_estimate = job.estimate_job_cost()
            print("EDSL cost estimate:", cost_estimate)
            (OUTPUTS / f"{run_id}_estimate.json").write_text(
                json.dumps(cost_estimate, indent=2, default=str))
        except Exception as e:
            raise SystemExit(f"Could not estimate cost; no paid calls made: {e}")
        if not args.yes and input("Run for real? [y/N] ").strip().lower() != "y":
            return

    started = dt.datetime.now(dt.timezone.utc).isoformat()
    results = job.run(cache=Cache(), disable_remote_inference=args.test,
                      disable_remote_cache=True)

    # 1) Raw results, untouched (re-loadable with edsl.Results.load)
    results.save(str(OUTPUTS / f"{run_id}_raw_results"))
    raw = results.to_pandas(remove_prefix=False)
    raw.to_csv(OUTPUTS / f"{run_id}_raw_results.csv", index=False)

    # 2) Tidy analysis rows
    def col(name):
        return raw[name] if name in raw.columns else pd.NA

    tidy = pd.DataFrame({
        "run_id": run_id,
        "is_test": args.test,
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
        "option_order": col("scenario.decision_options").map(lambda x: "|".join(x)),
        "run_started_utc": started,
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

    key = ["run_id", "persona_id", "scenario_id", "version", "model_id", "repeat"]
    assert not tidy[key].isna().any().any(), "missing analysis identifiers"
    assert not tidy.duplicated(key).any(), "analysis key is not unique"
    assert len(tidy) == n_obs, "missing survey observations"
    tidy.to_csv(OUTPUTS / f"{run_id}_responses.csv", index=False)

    # 3) Rendered prompts for the hand check
    prompt_cols = [c for c in raw.columns if c.startswith("prompt.")]
    raw[["agent.persona_id", "scenario.scenario_id", "scenario.version", "model.model"] + prompt_cols] \
        .to_csv(OUTPUTS / f"{run_id}_prompts.csv", index=False)

    manifest = dict(run_id=run_id, is_test=args.test, started_utc=started, n_observations=len(tidy),
                    models=[m.model for m in models], edsl_version=__import__("edsl").__version__,
                    model_settings=[m.parameters for m in models], option_seed=331,
                    cache_policy="fresh in-memory cache; remote cache disabled",
                    personas_file="inputs/personas_poc.csv", scenarios_file="inputs/scenarios_poc.csv",
                    input_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in INPUTS.glob("*_poc.csv")})
    (OUTPUTS / f"{run_id}_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Saved {len(tidy)} rows to outputs/{run_id}_responses.csv")


if __name__ == "__main__":
    main()
