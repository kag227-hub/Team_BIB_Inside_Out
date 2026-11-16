# Instructor audit: Team BIB ("Inside Out" Silicon Investors), Checkpoint 2

**Repo:** kag227-hub/Team_BIB_Inside_Out · **Audited commit:** `2deff39` (2026-11-14 20:46, `main`) · **Seed:** 13 (LLM personas and the disposition effect), with your edits: *Inside Out* emotions × investor backgrounds, character-name vs. emotion-description arms

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

## Summary

The design is careful:
- matched gain/loss pairs with identical future-return statements;
- invalid answers never coded as "hold";
- a neutral control;
- a dated human benchmark (Odean 1998, Table I);
- a self-audit that already names the hardest problems.

The committed synthetic run reproduces byte for byte, and all 7 tests pass. But the **paid pilot**, the only behavioral data and the one the public dashboard shows, can't be reproduced or audited from the repo, because its raw responses aren't committed (A1). Its numbers already show the two things this seed's audit list warns about: the models disagree in sign, and wording flips signs. So freezing the primary test before the main run is the priority (A2).

| Check | Result |
|---|---|
| Reruns from scratch | ✅ for the synthetic run (`run_all.py` exit 0; 7/7 tests). ❌ for the paid pilot (A1) |
| Inputs have provenance | ✅ synthetic run (manifest with input hashes). ❌ paid pilot raw files (your F1) |
| Keys unique, merges validated | ✅ asserted in `build_dataset.py` |
| No look-ahead / survivorship | n/a (fictional firms) |
| LLM leakage handled | ⚠️ demand cues identified (your F6), not yet tested (A3). The LLM step was audited from cached outputs only |
| `specs_tried.md` complete | ⚠️ pilot logged; primary tests and adjustment not frozen (A2) |
| Magnitudes discussed | ✅ component rates and pp gaps, with Odean's +5.0 pp benchmark |
| Hand checks | ✅ counts in the export recomputed (also by the auditor). Response level not possible (A1) |
| Threats to validity | ✅ README and self-audit |
| Every number traces to `outputs/` | ⚠️ the dashboard reads `outputs/public_paid_pilot.json`, which no committed code or data regenerates |

## What holds up

- **Synthetic run reproduces.** `run_all.py` deletes and rebuilds `outputs/poc_TEST_v0_*` and `runs.json`. All seven files are byte-identical to the committed ones. `python -m unittest discover -s tests`: 7 OK.
- **The paid-pilot export is internally consistent.** In `outputs/public_paid_pilot.json`, the 18 cells sum to 54 complete pairs and 108 observations. Your self-audit's Embarrassment gaps follow from the counts: GPT-5.6 Luna −66.7 pp (name) vs. +33.3 pp (description); Claude Haiku 5.5 −33.3 pp vs. +66.7 pp.
- **Seed 13, "reciting the textbook":** personas are never told the hypothesis or the term "disposition effect", and you name EDSL's injected "Do not break character" line as a cue.
- **Seed 13, cost log:** `outputs/poc_TEST_v0_cost_projection.csv` and `poc_planning_estimate.csv`.

## Findings

### A1 · Major · The paid pilot can't be reproduced or audited

**Evidence:**
- `data/raw/` contains only `poc_TEST_v0` (synthetic); `run_all.py` prints "WARNING: only synthetic runs are in data/raw/".
- The dashboard (`dashboard/app.py:9-10`) reads `outputs/public_paid_pilot.json` (run `poc_paid_20261025T012651Z`). No committed code or data produces that file: `code/export_public_pilot.py` needs `outputs/poc_paid_20261025T012651Z_responses.csv`, which is not committed (README "Data"; your self-audit F1).
- In the audit environment, regenerating it is impossible, and there are no API keys for a live rerun, by design.

**Why it matters:** Every behavioral number you show comes from data nobody else can check. Parsing errors, invalid-answer handling or a wrong pairing in the paid run would be invisible. LLM steps are audited from the team's committed cached outputs, and for this run there are none.

**Fix:** Commit the paid run's raw EDSL results, rendered prompts and manifest under `data/raw/poc_paid_20261025T012651Z/`, as you did for the synthetic run. Model outputs from a course experiment are normally fine to share. If there's a specific term preventing it, cite it in the README and give Prof. Bowen access instead. Then `run_all.py` rebuilds the export.

**How to show it's fixed:** On a fresh clone, `python run_all.py` regenerates `outputs/public_paid_pilot.json` identically.

### A2 · Major · Freeze the primary test before the main run: the pilot already shows sign disagreement

**Evidence:** From the export, pooled over the 27 complete pairs per model, gain-sell minus loss-sell is:
- Claude Haiku 5.5: **+7.4 pp** (0.481 − 0.407);
- GPT-5.6 Luna: **−22.2 pp** (0.556 − 0.778);
- pooled over 54 pairs: −7.4 pp.

Within Embarrassment, the character-name and description arms have opposite signs for both models. Your self-audit (F11, checklist item 6) says the primary tests, the multiple-comparison adjustment and the failure rules aren't yet frozen in a dated file.

**Why it matters:** "Prompt sensitivity (does rewording flip the result?)" is the first item on this seed's audit list. With 8 emotions × 3 backgrounds × 2 arms × 2 models × 3 wordings, you'll be able to find a significant cell somewhere. The pilot shows the answer depends on model and wording, which is exactly when an unfrozen analysis plan becomes a specification search.

**Fix:** Before collecting the main study, commit a dated `ANALYSIS_PLAN.md` (or a `specs_tried.md` section) naming:
- the primary estimand: e.g. the neutral-control disposition effect per model, and emotion minus neutral per model, averaged over backgrounds and wordings;
- the paired test and interval (your paired bootstrap over base scenarios);
- the multiple-comparison adjustment (e.g. Holm across the 8 emotions × 2 models);
- what counts as a "sign flip" across wordings, and how it will be reported.

**How to show it's fixed:** The plan file's commit date precedes the main-run manifest's `started_utc`.

### A3 · Minor · Test the demand cues you found

**Evidence:**
- Your F6: EDSL prepends "You are answering questions as if you were a human. Do not break character."
- The scenarios say "past price moves say nothing about its future" and call the company "fictional" (`data/raw/poc_TEST_v0/prompts.csv`).

**Why it matters:** "Whether the model is just reciting the textbook answer" is on the seed's list. A line telling the model that past moves don't matter pushes toward the rational answer (no disposition effect), while role-play cues may push toward a stereotyped one.

**Fix:** Add one ablation arm in the main design, with the neutral control and one emotion: (a) no "past moves say nothing" sentence, (b) EDSL's system line removed or overridden, if EDSL allows. Report the disposition effect with and without each cue.

**How to show it's fixed:** The plan file lists the ablation, and the results include it.

### A4 · Minor · File names and README status are out of date

**Evidence:**
- The proposal is `Proposal.md` (not `PROPOSAL.md`), and the status memo is split across `status.md` and `STATUS_checkpoint1.md`.
- `README.md:11` says "This README does not report experimental results", but the dashboard linked at `README.md:3` reports the paid pilot.
- `README.md:13` still says model credentials "need verification", while the paid run happened on 2026-10-24.

**Fix:** Rename to `PROPOSAL.md` and a single `STATUS.md`. Update the README status lines to describe the paid pilot and point to where its data lives.

## How to respond

This audit is `audits/02_instructor_audit.md` in your repo. Fix what you can, then add `audits/03_audit_response.md`, replying to each finding ID: fixed (the commit), disputed (why), or disclosed as a limitation (where).

**Deadline: Saturday, November 21, 2026.**
