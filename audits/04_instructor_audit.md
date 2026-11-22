# Instructor audit: Team BIB ("Inside Out" Silicon Investors), Checkpoint 3

**Repo:** kag227-hub/Team_BIB_Inside_Out · **Audited commit:** `2ebf2f4` (2026-11-17, `main`, merge of PR #14) · **Seed:** 13, silicon investors: do LLM personas have the disposition effect? (with your `PROPOSAL.md` edits) · **CP2 audit:** `audits/02_instructor_audit.md` (commit `2deff39`)

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

## Summary

The CP2 fixes are excellent.
- The paid pilot's raw answers are committed, and `run_all.py` rebuilds the public export byte for byte on a fresh copy.
- My own pairing of the raw EDSL results reproduces all 18 dashboard cells.
- `ANALYSIS_PLAN.md` freezes the estimands, the paired bootstrap, Holm families and a sign-flip rule before any main-study collection.
- The demand-cue ablation is designed, coded and tested.

But the main study hasn't been collected. The only real data is still the 108-observation October pilot (B1). Your own plan prices the full design at about $11, so this is the one thing to do before Dec 1.

## Follow-up on your Checkpoint 2 audit

Response file: `audits/03_audit_response.md` found (on `main`). Statuses for A1, A2 and A4 come from the repo.

| CP2 finding | Status | Evidence |
|---|---|---|
| A1 · Paid pilot can't be reproduced | fixed | `data/raw/poc_paid_20261025T012651Z/` (raw_results.csv, prompts.csv, manifest.json with source and committed SHA-256). On a fresh copy, `python run_all.py` (exit 0, 8.7 s) regenerates `outputs/public_paid_pilot.json`, and `cmp` says it's identical to the committed file. `tests/test_paid_export.py` passes |
| A2 · Freeze the primary test before the main run | fixed | `ANALYSIS_PLAN.md` v1.0 (`058e549`, 2026-11-17) and v1.1 (`e8db10e`, 13:29 −0500): primary estimands, a paired bootstrap over base scenarios (B = 10,000, seed 331), Holm within two families, and a sign-flip rule (`ANALYSIS_PLAN.md:54-81`). No main-run manifest exists yet, so the plan necessarily predates it |
| A3 · Test the demand cues | disclosed | Designed (S8, a 2 × 2 ablation), coded (`code/cue_ablation.py`, `poc_run.py --ablation`) and tested on synthetic data (`poc_TEST_ablation_v0`, regenerated identically). Behavioral results await the paid run, as your response says ("Still to do") |
| A4 · File names and README status | fixed | `PROPOSAL.md` and a single `STATUS.md` exist at the root. README "Current status" and "Paid pilot, October 24, 2026" describe the pilot and its data |

**3 of 4 fixed, 0 still open (1 disclosed).**

## Checkpoint 3 checks

| Check | Result |
|---|---|
| Reruns from scratch (full sample) | ⚠️ ✅ every committed run rebuilds (3 runs; 29 of 31 output files identical, and the 2 PNGs differ in bytes). But no main-study run exists (B1) |
| Inputs have provenance | ✅ manifests with model IDs, EDSL version, option seed, source and SHA-256 |
| Keys unique, merges validated | ✅ asserted in `build_dataset.py`. My own pivot finds 54 complete gain/loss pairs, with no duplicates |
| No look-ahead / survivorship | n/a (fictional firms) |
| LLM leakage handled | ⚠️ cue ablation designed (A3), not yet run on paid data. The LLM step was audited from the committed answers (no API keys here) |
| `specs_tried.md` complete | ✅ PLAN-001/002 logged |
| Magnitudes discussed | ✅ pp gaps vs Odean's benchmark (pilot only) |
| Hand checks | ✅ 14 tests, including paid-export and prompt-hash checks |
| Threats to validity | ✅ README, including the remaining "fictional" cue |
| Every number traces to `outputs/` | ✅ the dashboard reads only `outputs/public_paid_pilot.json` |
| Dashboard matches `outputs/` | ✅ "108" observations, "54" pairs |

Steps not rerun by design: `code/poc_run.py` (paid EDSL calls; this environment has no API keys by design). The LLM step was audited from your committed raw answers. These are not counted against you.

## Getting ready for Dec 1

Presentations run only from URLs, with a hard cutoff at 9 minutes (10:45 section) or 10 minutes (12:10 section). Put your URL(s) in column G of the Team Projects sheet.

| Check | Result |
|---|---|
| Dashboard launches from a clean clone | ✅ `streamlit run dashboard/app.py --server.headless true --server.port 8612` (team venv) on a clean export of `2ebf2f4`: `/_stcore/health` returned `ok` after 3 s, with no exceptions on the page or in the log. `dashboard/requirements.txt` pins streamlit 1.67.0 and pandas 3.0.6 |
| Dashboard shows the v1 numbers from `outputs/` | ⚠️ it shows the pilot ("Exploratory results from the October paid model pilot"). There is no v1 yet (B1) |
| README links the live URL(s) | ✅ `README.md:3` links the `…streamlit.app` dashboard (the live site itself wasn't checked) |

**Core story for 9–10 minutes:** the disposition effect in neutral personas, per model (P1), then emotion minus neutral (P2) with Holm-adjusted intervals, then the sign-flip rule across wordings. The cue ablation is the slide that answers "is the model just reciting the textbook?"

## What holds up

- **Byte-for-byte reproduction** of the public export from committed raw answers, and 14/14 tests passing.
- **Independent check of the LLM step from the cache.** All 108 rows are validated, 54 per model (`gpt-5.6-luna`, `claude-haiku-5-5`), and 54 gain and 54 loss versions. My own gain/loss pairing (persona × scenario) reproduces every one of the 18 cells in `public_paid_pilot.json` (complete pairs, gain sells, loss sells). Pooled per model, gain-sell minus loss-sell is +7.41 pp (Claude Haiku 5.5) and −22.22 pp (GPT-5.6 Luna), as at CP2. Summed per-call costs give $0.031, which matches the manifest's `job_cost_usd` of $0.0307.
- **A real pre-registration.** It fixes the estimands, tests, families, failure rules and sign-flip rule before collection, with a deviation procedure.
- **Seed 13 items:** prompt sensitivity (3 wordings, 2 arms, a sign-flip rule); textbook recitation (the cue ablation); and a cost log (per-call costs in the raw file; projection in `*_cost_projection.csv`).

## New findings

### B1 · Blocking · The main study hasn't been collected

**Evidence:** `data/raw/` holds only `poc_paid_20261025T012651Z` (108 observations, 9 personas, 3 scenarios), plus two synthetic test runs. `ANALYSIS_PLAN.md:34`: the main study is 36,720 observations, "about $11", with a dollar cap in the manifest. README "Current status": "The paid pilot is complete."

**Why it matters:** Checkpoint 3 was v1 on the full sample. With 3 pairs per cell, the pilot can't answer the question, as your README says.

**Fix:** Run `python code/poc_run.py --run-id <main_id>` with the frozen plan and the ablation cells. Commit the raw answers as you did for the pilot, and rerun `run_all.py`.

**How to show it's fixed:** `data/raw/<main_id>/manifest.json` with `started_utc` after the `ANALYSIS_PLAN.md` commit, and outputs for P1/P2 with Holm-adjusted intervals. I will rebuild from the committed raw answers and recompute P1 from them.

## How to respond

This audit is `audits/04_instructor_audit.md` in your repo. Fix what you can, then add `audits/05_audit_response.md`, replying to each **B** finding (no CP2 findings are still open): fixed (the commit), disputed (why), or disclosed as a limitation (where).

There's no separate deadline for this response. Keep working through these until your final deliverables are due: the final repo is audited again then.
