"""
Checkpoint 1 proof of concept: Inside Out personas x matched gain/loss scenarios x 2 models.

What it does
  1. Loads inputs/personas_poc.csv, inputs/scenarios_poc.csv, inputs/models_poc.csv
  2. Expands every base scenario into a GAIN and a LOSS version and asserts that the two
     rendered texts differ ONLY in the sign of the return
  3. Builds an EDSL survey (sell/hold + 1-7 likelihood to sell), prints EDSL's cost estimate
  4. Runs it and saves the raw EDSL results untouched to data/raw/<run_id>/
     (raw_results.ep/.csv, prompts.csv, manifest.json). Everything downstream is rebuilt
     offline from those files by run_all.py.

Usage (from the repo root)
  python code/poc_run.py --test        # free dry run with EDSL's built-in "test" model (fake answers)
  python code/poc_run.py               # real run with the models in inputs/models_poc.csv (costs money)
  python code/poc_run.py --ablation --test   # free dry run of the demand-cue ablation (audit A3)
  python code/poc_run.py --ablation          # paid cue ablation: 2 personas x 4 cue cells

Cue ablation (instructor audit A3, self-audit F6). Two demand cues are switched on/off in a 2 x 2:
  cue_past_moves   1 = scenario says "...and that its past price moves say nothing about its future"
                   0 = that clause is removed (the rest of the scenario is unchanged)
  cue_system_line  1 = EDSL's default agent instruction ("You are answering questions as if you were
                       a human. Do not break character.") is prepended to the persona
                   0 = the instruction is overridden with an empty string, so the system prompt is
                       the persona text alone
Normal runs use cue_past_moves = cue_system_line = 1 only, so their prompts are unchanged.

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
from build_dataset import HOLD, SELL, tidy_from_raw
from edsl import (Agent, AgentList, Cache, Model, ModelList, QuestionLinearScale,
                  QuestionMultipleChoice, Scenario, ScenarioList, Survey)

ROOT = Path(__file__).resolve().parents[1]
INPUTS, OUTPUTS, RAW_DIR = ROOT / "inputs", ROOT / "outputs", ROOT / "data" / "raw"
OUTPUTS.mkdir(exist_ok=True)

PAST_MOVES_CLAUSE = ", and that its past price moves say nothing about its future"
SCENARIO_TEMPLATE = (
    "You bought shares of {company}, a fictional {industry} company, {holding_period} ago. "
    "Since you bought them, your position has returned {signed_return}. "
    "Analysts agree that the stock's expected return and risk over the next year are the same as "
    "the overall market's{past_moves_clause}. "
    "Ignore taxes and trading costs. You do not need the cash. If you sell, the money goes into a "
    "broad stock index fund with the same expected return and risk."
)
NO_SYSTEM_LINE = ""  # overrides EDSL's default agent instruction (see docstring)

# Cue ablation design (audit A3): the neutral control and one emotion, all four cue cells.
# Embarrassment is the emotion whose pilot sign flipped across prompt arms; the description arm
# is used so the film name is not a third role-play cue.
ABLATION_PERSONAS = ["neutral_generic", "embarrassment_mid_desc"]
CUE_CELLS = [(1, 1), (0, 1), (1, 0), (0, 0)]  # (cue_past_moves, cue_system_line)


def synthetic_response(user_prompt, system_prompt, files_list):
    """Valid fixed answers for plumbing checks; never experimental evidence."""
    return "4" if "How likely are you to sell" in user_prompt else HOLD


def build_scenarios(scen: pd.DataFrame, seed: int = 331, past_moves_levels=(1,)) -> list[dict]:
    """Gain/loss versions of each base scenario, for each requested cue_past_moves level.

    The option order is drawn once per base scenario (same RNG sequence as before the ablation
    existed), so it is identical across gain/loss AND across cue levels: the cue is the only
    thing that changes between cue cells.
    """
    rows = []
    rng = random.Random(seed)
    for r in scen.itertuples(index=False):
        options = [SELL, HOLD]
        rng.shuffle(options)
        for cue in past_moves_levels:
            texts = {}
            for version, sign in [("gain", "+"), ("loss", "-")]:
                signed = f"{sign}{r.abs_return_pct}%"
                text = SCENARIO_TEMPLATE.format(
                    company=r.company, industry=r.industry, holding_period=r.holding_period,
                    signed_return=signed, past_moves_clause=PAST_MOVES_CLAUSE if cue else "")
                texts[version] = text
                rows.append(dict(scenario_id=r.scenario_id, version=version,
                                 signed_return_pct=float(f"{sign}{r.abs_return_pct}"),
                                 abs_return_pct=r.abs_return_pct, holding_period=r.holding_period,
                                 cue_past_moves=int(cue),
                                 scenario_text=text,
                                 decision_options=options,
                                 prompt_hash=hashlib.sha256(text.encode()).hexdigest()[:12]))
            # Audit check: the pair must be identical once the signed return is removed
            g = texts["gain"].replace(f"+{r.abs_return_pct}%", "<RET>")
            l = texts["loss"].replace(f"-{r.abs_return_pct}%", "<RET>")
            assert g == l, f"{r.scenario_id}: gain and loss texts differ beyond the sign"
            assert (PAST_MOVES_CLAUSE in g) == bool(cue), f"{r.scenario_id}: cue_past_moves not applied"
    return rows


def build_agents(personas: pd.DataFrame, system_line_levels=(1,)) -> AgentList:
    """One EDSL agent per persona and cue_system_line level. Only persona_text is shown."""
    agents = []
    for p in personas.itertuples(index=False):
        for cue in system_line_levels:
            extra = {} if cue else dict(instruction=NO_SYSTEM_LINE)
            agents.append(Agent(
                name=p.persona_id if cue else f"{p.persona_id}__no_system_line",
                traits=dict(persona_id=p.persona_id, emotion=p.emotion, background=p.background,
                            prompt_arm=p.prompt_arm, is_control=int(p.is_control),
                            cue_system_line=int(cue), persona_text=p.persona_text),
                traits_presentation_template="{{ persona_text }}", **extra))
    return AgentList(agents)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="use EDSL's free fake 'test' model")
    ap.add_argument("--yes", action="store_true", help="skip the cost confirmation prompt")
    ap.add_argument("--plan", action="store_true", help="save a planning estimate; no model calls")
    ap.add_argument("--run-id", help="unique artifact prefix; existing runs cannot be overwritten")
    ap.add_argument("--ablation", action="store_true",
                    help="demand-cue ablation (audit A3): ABLATION_PERSONAS x all four cue cells")
    args = ap.parse_args()

    personas = pd.read_csv(INPUTS / "personas_poc.csv")
    if args.ablation:
        assert set(ABLATION_PERSONAS) <= set(personas.persona_id), "ablation persona missing"
        personas = personas[personas.persona_id.isin(ABLATION_PERSONAS)].reset_index(drop=True)
        cue_levels = [1, 0]
    else:
        cue_levels = [1]
    n_cue_cells = len(cue_levels) ** 2
    scen = pd.read_csv(INPUTS / "scenarios_poc.csv")
    models_tbl = pd.read_csv(INPUTS / "models_poc.csv")
    assert personas["persona_id"].is_unique and scen["scenario_id"].is_unique
    assert len(models_tbl) == 2 and models_tbl["model_id"].is_unique
    assert scen["abs_return_pct"].isin([5, 10, 20]).all()

    # Per-call assumptions, not measured tokens or a guaranteed spending cap.
    estimates = models_tbl[["model_id", "price_source", "price_checked"]].copy()
    estimates["observations"] = len(personas) * len(scen) * 2 * n_cue_cells
    estimates["requests"] = estimates["observations"] * 2
    estimates["assumed_input_tokens_per_request"] = 2000
    estimates["assumed_output_tokens_per_request"] = 500
    estimates["estimated_usd"] = estimates["requests"] * (
        2000 * models_tbl["input_usd_per_million"]
        + 500 * models_tbl["output_usd_per_million"]) / 1_000_000
    print(estimates[["model_id", "observations", "requests", "estimated_usd"]].to_string(index=False))
    if args.plan:
        name = "poc_ablation_planning_estimate.csv" if args.ablation else "poc_planning_estimate.csv"
        estimates.to_csv(OUTPUTS / name, index=False)
        return
    if not args.test and not os.getenv("EXPECTED_PARROT_API_KEY"):
        raise SystemExit("Paid run requires EXPECTED_PARROT_API_KEY in the environment or ignored .env. No calls made.")

    scenario_rows = build_scenarios(scen, past_moves_levels=cue_levels)
    scenarios = ScenarioList([Scenario(d) for d in scenario_rows])

    # Only persona_text is shown to the model; the other traits ride along as metadata
    agents = build_agents(personas, system_line_levels=cue_levels)

    if args.test:
        models = ModelList([Model("test", func=synthetic_response)])
        run_id = ("poc_TEST_ablation_" if args.ablation else "poc_TEST_") + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
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
        run_id = ("poc_ablation_" if args.ablation else "poc_") + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    if args.run_id:
        assert Path(args.run_id).name == args.run_id and args.run_id not in (".", "..")
        run_id = args.run_id
    run_dir = RAW_DIR / run_id
    assert not run_dir.exists() and not list(OUTPUTS.glob(f"{run_id}_*")), \
        "Run ID already exists; choose a new one"
    run_dir.mkdir(parents=True)

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
    print(f"run_id={run_id}: {len(agents)} persona agents x {len(scenarios)} scenario versions x "
          f"{len(models)} models = {n_obs} survey observations ({2 * n_obs} model calls)")
    if not args.test:
        try:
            cost_estimate = job.estimate_job_cost()
            print("EDSL cost estimate:", cost_estimate)
            (run_dir / "estimate.json").write_text(
                json.dumps(cost_estimate, indent=2, default=str))
        except Exception as e:
            raise SystemExit(f"Could not estimate cost; no paid calls made: {e}")
        if not args.yes and input("Run for real? [y/N] ").strip().lower() != "y":
            return

    started = dt.datetime.now(dt.timezone.utc).isoformat()
    results = job.run(cache=Cache(), disable_remote_inference=args.test,
                      disable_remote_cache=True)

    # 1) Raw results, untouched (re-loadable with edsl.Results.load)
    results.save(str(run_dir / "raw_results"))
    raw = results.to_pandas(remove_prefix=False)
    raw.to_csv(run_dir / "raw_results.csv", index=False)

    # 2) Tidy analysis rows (same function the offline rebuild uses: code/build_dataset.py)
    tidy = tidy_from_raw(raw, run_id, args.test, started)
    assert len(tidy) == n_obs, "missing survey observations"

    # 3) Rendered prompts for the hand check
    prompt_cols = [c for c in raw.columns if c.startswith("prompt.")]
    raw[["agent.persona_id", "agent.cue_system_line", "scenario.scenario_id", "scenario.version",
         "scenario.cue_past_moves", "model.model"] + prompt_cols] \
        .to_csv(run_dir / "prompts.csv", index=False)

    manifest = dict(run_id=run_id, is_test=args.test, started_utc=started, n_observations=len(tidy),
                    models=[m.model for m in models], edsl_version=__import__("edsl").__version__,
                    model_settings=[m.parameters for m in models], option_seed=331,
                    cache_policy="fresh in-memory cache; remote cache disabled",
                    personas_file="inputs/personas_poc.csv", scenarios_file="inputs/scenarios_poc.csv",
                    design="cue_ablation" if args.ablation else "pilot",
                    persona_ids=personas.persona_id.tolist(),
                    cue_cells=[dict(cue_past_moves=a, cue_system_line=b)
                               for a, b in CUE_CELLS if a in cue_levels and b in cue_levels],
                    input_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in INPUTS.glob("*_poc.csv")})
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Saved raw artifacts to data/raw/{run_id}/. Rebuild outputs with: python run_all.py")


if __name__ == "__main__":
    main()
