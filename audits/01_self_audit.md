# Self-audit 01 — Checkpoint 2 (v0)

**Team BIB · Inside Out Silicon Investors · audited November 14, 2026 · updated after PR #8 (paid-pilot summary counts)**

> **How this review was done.** On November 15, 2026 we ran the course's *Skeptical review* prompt
> (Quick Reference → *Starter prompts for coding agents* → #5) on `main`, word for word: *"Review this repo
> like a skeptical finance professor. Look for look-ahead bias and leakage, merges without `validate`, unit
> and frequency mismatches, hard-coded paths or keys, and steps that don't reproduce from `run_all.py`. List
> issues ranked by severity; don't fix anything yet."* It ranked F1 (paid results not reproducible) and F6/F7
> (LLM leakage, demand cues) as the most severe, and flagged F16–F20 as new. It found no merges without
> `validate` and no look-ahead bias (F15). The ten-point checklist in Section 3 uses the course checklist items as
> filled in by Ayushi (from [PR #5](https://github.com/kag227-hub/Team_BIB_Inside_Out/pull/5)), with the
> evidence updated for this pipeline.

## 1. What the review flagged, and which findings are real

| # | Finding | Real? | Evidence |
|---|---|---|---|
| F1 | **The paid pilot's raw responses are still not in the repo.** Only cell-level summary counts are committed (`outputs/public_paid_pilot.json`, added in PR #8: sells and complete pairs for each model × emotion × prompt arm). `run_all.py` cannot rebuild the real results, and an auditor cannot re-check parsing, the prompts, the model comments or costs. | **Real — most serious; partly fixed** | `outputs/public_paid_pilot.json` (18 cells, 108 responses, 54 pairs); `code/export_public_pilot.py` needs a local paid responses file that is not committed. No `data/raw/poc_paid_*` folder. |
| F2 | **The real results and the reproducible pipeline are split.** The dashboard now shows the paid pilot's sell rates, but everything `run_all.py` rebuilds (the dataset, table and figure in `outputs/`) is still the synthetic run, where every effect is 0 by construction. The dashboard also no longer shows individual responses or exact prompts. | **Real** (consequence of F1) | `dashboard/app.py` reads only `outputs/public_paid_pilot.json`; `outputs/poc_TEST_v0_*` come from `data/raw/poc_TEST_v0/`. |
| F3 | **Option order is confounded with scenario and return size.** The seed-331 shuffle is drawn once per scenario, so s01 (5%) always shows *Sell* first and s02 (10%) and s03 (20%) always show *Hold* first. A magnitude effect cannot be separated from an option-order effect. | **Real** | `outputs/poc_TEST_v0_responses.csv`, `option_order` by `scenario_id`. |
| F4 | **Return magnitude is also collinear with company, industry and holding period** (one scenario per magnitude). | **Real** (pilot design limit) | `inputs/scenarios_poc.csv`: 3 rows, one per magnitude. |
| F5 | **Tiny cells: 3 matched pairs per persona × model.** A single flipped answer moves the effect by 33 pp, and no uncertainty intervals are reported yet, although the README promises a paired bootstrap. | **Real** | `outputs/*_rates.csv`: `n_gain = n_loss = 3`. |
| F6 | **Demand cues in the prompt.** EDSL prepends "You are answering questions as if you were a human. Do not break character."; the scenario text says "past price moves say nothing about its future" and calls the company "fictional". These may push answers toward textbook rationality, or toward role-play stereotypes. | **Real** (direction unknown) | `data/raw/poc_TEST_v0/prompts.csv`, `prompt.decision_system_prompt` / `_user_prompt`. |
| F7 | **LLM leakage of the disposition-effect literature.** Two Claude neutral-control comments used theory language in the paid pilot. The regex flag catches only a few keywords. | **Real**, partly mitigated | `STATUS_checkpoint1.md`; `code/poc_analyze.py` section 3. Hand review of ≥10 comments per model is still pending. |
| F8 | **The neutral control is not background-matched.** Emotional personas are all "42-year-old mid-career"; the control is a generic investor. An emotion-vs-control gap mixes emotion with background. | **Real** | `inputs/personas_poc.csv`. |
| F9 | **The two models are configured differently** (GPT: temperature 1.0 and low reasoning effort; Claude: adaptive thinking and low effort, no temperature). Model differences include setting differences. | **Real**, disclosed | `inputs/models_poc.csv`, `code/poc_run.py`. |
| F10 | **Decision and rating come from separate, memoryless calls**, so a persona can choose "Sell" and rate selling 2/7. Consistency is not checked. | **Real** | `code/poc_run.py` (two-question survey, no memory). |
| F11 | **Specification search / p-hacking risk.** 8 emotions × 2 arms × 2 models × wordings creates many comparisons, and primary tests are not frozen yet. | **Real** (open) | README "Researcher discretion"; `specs_tried.md` exists but there is no frozen pre-registration. |
| F12 | **No one-command rebuild; raw files mixed with derived outputs; README listed implemented files as "planned".** | Real — **fixed (PR #6)** | See Section 2. |
| F13 | `.gitignore` excluded `outputs/poc_TEST_*`, which would hide v0 outputs from the dashboard. | Real — **fixed (PR #6)** | `.gitignore`. |
| F14 | `requirements.txt` lacked `matplotlib`, which the figure step needs. | Real — **fixed (PR #6)** | `requirements.txt`. |
| F15 | Look-ahead bias, survivorship bias, merge errors. | **Not applicable / low** | Fictional firms and no time series, so no look-ahead or survivorship. No dataset merges: persona traits travel inside each EDSL agent, and keys are asserted unique. |
| F16 | **Past returns cover different time spans (unit / frequency mismatch).** The 5%, 10% and 20% returns are cumulative over 8, 14 and 24 months, so annualized they are almost the same (7.6%, 8.5%, 9.5% a year), while the future is described over one year. The "return size" factor is really a time-span difference; we can't tell whether models react to the total gain or the yearly gain. | **Real** | `inputs/scenarios_poc.csv` (`holding_period`, `abs_return_pct`). |
| F17 | **`run_all.py` and the README describe the dashboard wrongly.** `run_all.py` says it rebuilds "every output" and writes `runs.json` "which the dashboard reads", but since PR #8 the dashboard reads only `outputs/public_paid_pilot.json`, which `run_all.py` never touches. | **Real** | `run_all.py` docstring and final print; `dashboard/app.py` line 9. |
| F18 | **Leftover files in `outputs/` that `run_all.py` doesn't produce.** `checkpoint1_validation.json` refers to a run (`poc_TEST_validated`) that no longer exists; `checkpoint1_dry_run_feasibility.md` and `poc_planning_estimate.csv` are also not rebuilt. | **Real**, low | `outputs/`. |
| F19 | **Mixed units in one table.** `outputs/*_summary_table.csv` shows sell rates as fractions (0–1) next to the gap in percentage points; the dashboard shows percentages. Labels are correct but easy to misread. | **Real**, low | `code/make_figures.py`, `code/poc_analyze.py`. |
| F20 | **Key hygiene is missing two course-recommended files.** No hard-coded keys or absolute paths were found (code, data, and the zipped raw-results archive), but `.gitignore` does not list `.streamlit/secrets.toml` and there is no `.env.example`. | **Real**, low | `.gitignore`; Quick Reference starter prompt #2. |

## 2. Fixed vs. still open

### Fixed

- **One-command, offline pipeline** (`python run_all.py`): it deletes each run's old outputs, then rebuilds raw → dataset → analysis → table + figure for every run in `data/raw/`. It makes no API calls.
- **Raw and derived files separated.** `code/poc_run.py` now writes untouched raw EDSL results, prompts and the manifest to `data/raw/<run_id>/`. Everything in `outputs/` is regenerated.
- **Single source of truth for parsing.** `code/build_dataset.py` holds the raw → tidy logic and the collector imports it. The offline rebuild matched the collector's own output exactly (`assert_frame_equal`) on the v0 run.
- **New tests** (`tests/test_build_dataset.py`): invalid or refused answers never become "hold"; duplicate keys are rejected; the committed raw run rebuilds with the expected row count. All 7 tests pass.
- **Headline figure and table** in `outputs/`, with the Odean +5 pp benchmark marked. Missing pairs draw no bar instead of a zero bar.
- **Dashboard skeleton** (`dashboard/app.py`): Intro, Methodology, Results and Explore pages, reading only saved files.
- **Real paid-pilot results on the dashboard** (PR #8): matched-pair counts, gain and loss sell rates and their gap for each model × emotion × prompt arm, with filters. The counts reproduce the figures reported in `STATUS_checkpoint1.md` (see checklist item 8).
- F12, F13 and F14 above.
- - **Dashboard live** at https://teambibinsideout-tkgtmunmsq9qkk3gjgrgdd.streamlit.app/

### Still open, with plan

| Finding | Plan | Owner / when |
|---|---|---|
| F1, F2 | Commit the paid run's raw files to `data/raw/poc_paid_20261025T012651Z/` (`raw_results.csv`, `raw_results.ep`, `prompts.csv`, `manifest.json`) after checking them for credentials, then run `python run_all.py`. This rebuilds the real dataset, table and figure, and lets the dashboard show individual responses again. If the team decides to keep them private, state the reason here and in the README. | _team_ · before the instructor reviews the PR |
| F3, F4 | Main study: randomize option order *within* scenario across personas or repeats (still fixed within a gain/loss pair), and use several companies per magnitude (the README's 20 base scenarios). | Before freezing the main design |
| F5 | Add a paired bootstrap over base scenarios for persona-level intervals; cluster by persona for pooled estimates (README "Outcomes and analysis"). | Next analysis PR |
| F6 | Test one arm with EDSL's default instruction removed or replaced; log it in `specs_tried.md`. Keep the "past moves say nothing" sentence (it defines the rational benchmark), but report the issue. | Pilot 2 |
| F7 | Hand-read ≥10 comments per model; expand the flag list; report the flagged share by cell. | Before freezing |
| F8 | Add background-matched neutral controls (one per background). | Main design |
| F9 | Keep settings as chosen (disclosed), and report model comparisons as "model + configuration". | Ongoing |
| F10 | Report the decision/rating agreement rate; consider a single structured question as a robustness arm. | Next analysis PR |
| F11 | Freeze the primary hypotheses (emotion-level gaps vs. neutral, per model), the multiple-comparison adjustment and the failure rules in a timestamped file before the main run. | Before the main run |
| F16 | In the main design, hold the holding period fixed when varying return size (or vary both on a grid), and state past returns on the same horizon as the one-year outlook. | Before freezing the main design |
| F17 | Fix the `run_all.py` docstring and final message, and the README "How to run" note, so they say the dashboard reads the paid-pilot summary file, which `run_all.py` does not rebuild. | Next PR |
| F18 | Move the Checkpoint 1 files out of `outputs/` (for example to `archive/checkpoint1/`) so `outputs/` holds only what `run_all.py` makes. | Next PR |
| F19 | Report all rates in percent in the saved tables to match the dashboard. | Next analysis PR |
| F20 | Add `.streamlit/secrets.toml` to `.gitignore` and add an `.env.example` showing `EXPECTED_PARROT_API_KEY=` with no value. | Next PR |

## 3. Ten-point checklist (`00_PROJECT_SEEDS`)

| Course checklist | Status | Evidence / follow-up |
|---|---|---|
| 1. Reproduces | OK | `python run_all.py` deletes and regenerates every v0 output from `data/raw/` offline, with no API keys or model calls. 7 tests pass (`python -m unittest discover -s tests`). |
| 2. Input provenance | OK for v0; **problem** for the paid pilot | The v0 run's raw EDSL results, rendered prompts and manifest (with SHA-256 hashes of the input tables) are committed in `data/raw/poc_TEST_v0/`. For the paid pilot only cell-level summary counts are committed (`outputs/public_paid_pilot.json`); the raw responses are not (F1). |
| 3. Unit and keys | OK | One row = run × persona × scenario × gain/loss version × model × repeat. Key uniqueness, missing identifiers and the row count against the manifest are asserted in `code/build_dataset.py`; `code/poc_analyze.py` re-checks keys and reports incomplete pairs. |
| 4. Look-ahead | OK | Fictional companies, with no market history, realized future prices or historically selected sample (F15). |
| 5. LLM leakage | **problem** | Learned disposition-effect concepts, *Inside Out* character cues and EDSL's "Do not break character" instruction can cue the expected behavior (F6, F7). Plan: hand-read comments, run prompt-sensitivity checks, compare arms with the neutral control. |
| 6. No p-hacking | **problem** | Pilot specifications are logged in `specs_tried.md`, but primary tests, the multiple-comparison adjustment and failure rules are not yet frozen in a dated file (F11). |
| 7. Magnitudes | OK | Both component sell rates, the percentage-point gap and the number of matched pairs are reported for every cell: for the paid pilot on the dashboard, and for the synthetic run in `outputs/*_summary_table.csv`. There are no confidence intervals yet (F5), and with 3 pairs per cell one changed answer moves a rate by about 33 pp. |
| 8. Hand checks | OK for consistency; **not yet** at the response level | The paid-pilot counts in `outputs/public_paid_pilot.json` were recomputed by hand and match `STATUS_checkpoint1.md`: 108 responses, 54 complete pairs, and the Embarrassment gaps of −66.7 pp (name) vs +33.3 pp (description) for GPT-5.6 Luna and −33.3 pp vs +66.7 pp for Claude Haiku 5.5. Both come from the same pilot analysis, so this checks consistency, not parsing. A response-level hand check needs the raw files (F1). On synthetic data, `code/poc_analyze.py` prints a matched pair to verify and the tests check invalid-answer handling. |
| 9. Threats to validity | OK | See Sections 1–2 of this audit and the README's "Threats to validity" (leakage, framing, option order, sample size, benchmark mismatch). |
| 10. Team understanding | not yet | Each teammate should rerun v0 and be able to explain the join keys, invalid-answer handling and the paired gain-minus-loss estimator. |
