# Response to the instructor audit (Checkpoint 2)

Replies to [audits/02_instructor_audit.md](02_instructor_audit.md), one section per finding ID. Each finding is marked as fixed (with the commit), disputed (with the reason), or disclosed as a limitation (with where it is disclosed).

## A1 · Major · The paid pilot can't be reproduced or audited

_To be completed._

## A2 · Major · Freeze the primary test before the main run

_To be completed. Plan file: [ANALYSIS_PLAN.md](../ANALYSIS_PLAN.md)._

## A3 · Minor · Test the demand cues you found

**Status: fixed in the design and code. Results will come from the ablation cells of the main run.**

**What we changed**

1. **Plan.** [ANALYSIS_PLAN.md](../ANALYSIS_PLAN.md), Section 6, **S8**, adds a 2 × 2 ablation that switches each cue off. The plan is now v1.1, and the change is logged as PLAN-002 in `specs_tried.md`.

   | `cue_past_moves` | `cue_system_line` | Prompt change |
   |:-:|:-:|---|
   | 1 | 1 | None (the main-design prompt) |
   | 0 | 1 | Drops ", and that its past price moves say nothing about its future". The rest of the scenario is word-for-word the same. |
   | 1 | 0 | Overrides EDSL's default instruction ("You are answering questions as if you were a human. Do not break character.") with an empty string |
   | 0 | 0 | Both |

   The design follows your suggested fix. It uses the neutral control and one emotion, Embarrassment (description arm). Embarrassment is the emotion whose pilot sign flipped across prompt arms. The ablation runs on all 20 base scenarios, wording w1, with 3 repeats and both models. The three new cells add 1,440 observations, about $0.40.

2. **EDSL allows removing the system line.** In EDSL 1.0.9, `Agent(instruction="")` replaces the default instruction. The system prompt is then the persona text alone. We checked this in the rendered prompts, not only in the EDSL source.

3. **Collection.** `python code/poc_run.py --ablation` builds the four cells. The gain/loss check still asserts that paired texts differ only in the sign of the return. A new assertion checks that the clause is present exactly when `cue_past_moves = 1`. Option order is drawn once per base scenario, so it does not change across cue cells. The manifest records `design`, `persona_ids` and `cue_cells`.

4. **Analysis.** `cue_past_moves` and `cue_system_line` are now part of the analysis key in `build_dataset.py` and `poc_analyze.py`. Older runs default to 1/1, so the existing runs rebuild with the same numbers. The new script `code/cue_ablation.py` reports the following for each model and persona, and pooled across personas:
   - the disposition effect (DE) in each cell;
   - the effect of removing each cue (DE without the cue minus DE with it, averaged over the other cue);
   - the interaction between the two cues.

   Each estimate comes with a scenario-level bootstrap 95% interval. `run_all.py` runs the script for any run whose manifest says `design: cue_ablation`.

5. **Verification (free).** The synthetic dry run `poc_TEST_ablation_v0` is committed in `data/raw/` and `outputs/`. It has 48 rows, all valid, and 24 of 24 complete pairs. `tests/test_cue_ablation.py` adds 6 offline tests:
   - Standard prompts and their hashes are unchanged from `poc_TEST_v0`.
   - The no-past-moves text equals the original with only the clause removed.
   - The committed dry-run prompts contain the system line exactly when `cue_system_line = 1`, and the clause exactly when `cue_past_moves = 1`.
   - Older runs default to both cues on.
   - On a known fixture, the contrast arithmetic gives the expected values.

   The full suite passes, 13 of 13.

**Not ablated (disclosed).** The word "fictional" stays in every scenario, and the README's threats-to-validity section names it as a remaining cue. It keeps the models from bringing in knowledge of real tickers.

**Still to do.** The audit asks that "the results include it". Behavioral results need a paid run. The synthetic run only shows that the pipeline works. The ablation cells are part of the main run (S8). A small paid ablation on the 3 pilot scenarios costs about $0.03 and can be run first with `python code/poc_run.py --ablation`.

## A4 · Minor · File names and README status are out of date

_To be completed._
