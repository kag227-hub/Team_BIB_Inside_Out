# Self-audit 01 — Checkpoint 2 (v0)

**Team BIB · Inside Out Silicon Investors · audited November 14, 2026**

> **Draft for the team to edit.** The findings below come from a skeptical review of the repository at the
> Checkpoint 2 branch. Before submitting, (1) re-run the course's exact *Skeptical review* prompt
> (Quick Reference → *Starter prompts for coding agents* → #5) and merge anything new into Section 1, and
> (2) fill in the 10-point checklist in Section 3 using the wording in `00_PROJECT_SEEDS`.

## 1. What the review flagged, and which findings are real

| # | Finding | Real? | Evidence |
|---|---|---|---|
| F1 | **The paid pilot's raw responses are not in the repo.** Every number in `STATUS_checkpoint1.md` (108 obs, $0.0307, the Embarrassment sign flip) can't be recomputed from committed files. | **Real — most serious** | `STATUS_checkpoint1.md`: "raw artifacts are saved in Colab and on Expected Parrot, but transfer into this PR … pending". No `poc_paid_*` files anywhere in the repo. |
| F2 | **v0 outputs and dashboard run on the synthetic test model**, so every effect is 0 by construction. | **Real** (direct consequence of F1) | `data/raw/poc_TEST_v0/` is the only run; the model answers "hold / 4" to everything. Labeled as synthetic in every output and on every dashboard page. |
| F3 | **Option order is confounded with scenario and return size.** The seed-331 shuffle is drawn once per scenario, so s01 (5%) always shows *Sell* first and s02 (10%) and s03 (20%) always show *Hold* first. A magnitude effect cannot be separated from an option-order effect. | **Real** | `outputs/poc_TEST_v0_responses.csv`, `option_order` by `scenario_id`. |
| F4 | **Return magnitude is also collinear with company, industry and holding period** (one scenario per magnitude). | **Real** (pilot design limit) | `inputs/scenarios_poc.csv`: 3 rows, one per magnitude. |
| F5 | **Tiny cells: 3 matched pairs per persona × model.** A single flipped answer moves the effect by 33 pp, and no uncertainty intervals are reported yet, although the README promises a paired bootstrap. | **Real** | `outputs/*_rates.csv`: `n_gain = n_loss = 3`. |
| F6 | **Demand cues in the prompt.** EDSL prepends "You are answering questions as if you were a human. Do not break character."; the scenario text says "past price moves say nothing about its future" and calls the company "fictional". These may push answers toward textbook rationality, or toward role-play stereotypes. | **Real** (direction unknown) | `data/raw/poc_TEST_v0/prompts.csv`, `prompt.decision_system_prompt` / `_user_prompt`. |
| F7 | **LLM leakage of the disposition-effect literature.** Two Claude neutral-control comments used theory language in the paid pilot. The regex flag catches only a few keywords. | **Real**, partly mitigated | `STATUS_checkpoint1.md`; `code/poc_analyze.py` section 3. Hand review of ≥10 comments per model is still pending. |
| F8 | **The neutral control is not background-matched.** Emotional personas are all "42-year-old mid-career"; the control is a generic investor. An emotion-vs-control gap mixes emotion with background. | **Real** | `inputs/personas_poc.csv`. |
| F9 | **The two models are configured differently** (GPT: temperature 1.0 and low reasoning effort; Claude: adaptive thinking and low effort, no temperature). Model differences include setting differences. | **Real**, disclosed | `inputs/models_poc.csv`, `code/poc_run.py`. |
| F10 | **Decision and rating come from separate, memoryless calls**, so a persona can choose "Sell" and rate selling 2/7. Consistency is not checked. | **Real** | `code/poc_run.py` (two-question survey, no memory). |
| F11 | **Specification search / p-hacking risk.** 8 emotions × 2 arms × 2 models × wordings creates many comparisons, and primary tests are not frozen yet. | **Real** (open) | README "Researcher discretion"; `specs_tried.md` exists but there is no frozen pre-registration. |
| F12 | **No one-command rebuild; raw files mixed with derived outputs; README listed implemented files as "planned".** | Real — **fixed in this PR** | See Section 2. |
| F13 | `.gitignore` excluded `outputs/poc_TEST_*`, which would hide v0 outputs from the dashboard. | Real — **fixed in this PR** | `.gitignore`. |
| F14 | `requirements.txt` lacked `matplotlib`, which the figure step needs. | Real — **fixed in this PR** | `requirements.txt`. |
| F15 | Look-ahead bias, survivorship bias, merge errors. | **Not applicable / low** | Fictional firms and no time series, so no look-ahead or survivorship. No dataset merges: persona traits travel inside each EDSL agent, and keys are asserted unique. |

## 2. Fixed in this PR vs. still open

### Fixed

- **One-command, offline pipeline** (`python run_all.py`): it deletes each run's old outputs, then rebuilds raw → dataset → analysis → table + figure for every run in `data/raw/`. It makes no API calls.
- **Raw and derived files separated.** `code/poc_run.py` now writes untouched raw EDSL results, prompts and the manifest to `data/raw/<run_id>/`. Everything in `outputs/` is regenerated.
- **Single source of truth for parsing.** `code/build_dataset.py` holds the raw → tidy logic and the collector imports it. The offline rebuild matched the collector's own output exactly (`assert_frame_equal`) on the v0 run.
- **New tests** (`tests/test_build_dataset.py`): invalid or refused answers never become "hold"; duplicate keys are rejected; the committed raw run rebuilds with the expected row count. All 7 tests pass.
- **Headline figure and table** in `outputs/`, with the Odean +5 pp benchmark marked. Missing pairs draw no bar instead of a zero bar.
- **Dashboard skeleton** (`dashboard/app.py`): Intro, Methodology, Results and Explore pages, reading only saved files. Synthetic runs carry a warning banner on every page.
- F12, F13 and F14 above.

### Still open, with plan

| Finding | Plan | Owner / when |
|---|---|---|
| F1, F2 | Export the paid run from Colab / Expected Parrot into `data/raw/poc_paid_20261025T012651Z/` (`raw_results.csv`, `raw_results.ep`, `prompts.csv`, `manifest.json`), check for keys, commit, run `python run_all.py`. The dashboard switches to it automatically. | _team_ · before the instructor reviews the PR |
| Dashboard live | Deploy `dashboard/app.py` on Streamlit Community Cloud and put the URL at the top of the README. | _team_ · this week |
| F3, F4 | Main study: randomize option order *within* scenario across personas or repeats (still fixed within a gain/loss pair), and use several companies per magnitude (the README's 20 base scenarios). | Before freezing the main design |
| F5 | Add a paired bootstrap over base scenarios for persona-level intervals; cluster by persona for pooled estimates (README "Outcomes and analysis"). | Next analysis PR |
| F6 | Test one arm with EDSL's default instruction removed or replaced; log it in `specs_tried.md`. Keep the "past moves say nothing" sentence (it defines the rational benchmark), but report the issue. | Pilot 2 |
| F7 | Hand-read ≥10 comments per model; expand the flag list; report the flagged share by cell. | Before freezing |
| F8 | Add background-matched neutral controls (one per background). | Main design |
| F9 | Keep settings as chosen (disclosed), and report model comparisons as "model + configuration". | Ongoing |
| F10 | Report the decision/rating agreement rate; consider a single structured question as a robustness arm. | Next analysis PR |
| F11 | Freeze the primary hypotheses (emotion-level gaps vs. neutral, per model), the multiple-comparison adjustment and the failure rules in a timestamped file before the main run. | Before the main run |

## 3. Ten-point checklist (`00_PROJECT_SEEDS`)

> **TODO (team):** copy the ten item names from the top of `00_PROJECT_SEEDS` into the first column. The
> notes column suggests relevant evidence from this audit.

| # | Checklist item (from `00_PROJECT_SEEDS`) | Status (OK / problem / not yet) | Note |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

Evidence to draw on when filling it in:

- **One-command reproducibility:** OK (`run_all.py`).
- **Raw data committed:** problem (F1).
- **Secrets out of git:** OK (`.env` ignored, key read from the environment).
- **Unique keys / merge checks:** OK (asserted in `build_dataset.py` and `poc_analyze.py`).
- **Look-ahead / survivorship:** N/A, fictional firms.
- **LLM leakage:** problem, partly mitigated (F6, F7).
- **Specification log:** OK (`specs_tried.md`).
- **Pre-registration / p-hacking:** not yet (F11).
- **Uncertainty reported:** not yet (F5).
- **Dashboard live:** not yet.
- **Hand check:** OK on synthetic data; paid run pending (F1).
