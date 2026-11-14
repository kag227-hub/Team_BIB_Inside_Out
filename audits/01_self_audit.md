# Checkpoint 2 self-audit

November 14, 2026 · Team BIB

Review basis: applied the FIN331 Quick Reference’s “Skeptical review” prompt (#5) to the Checkpoint 1 baseline, then assessed what the v0 changes fix. This audit covers the committed synthetic fixture.

| Severity | Finding | Assessment and response |
|---|---|---|
| High | The paid pilot could not be independently recomputed from the repository; main contained a memo but not the paid raw inputs. | Real. The single-command offline pipeline is now reproducible on a labeled synthetic fixture. Recovering the paid responses, documenting normalization, and reproducing the paid memo remain open. |
| High | Learned finance concepts, movie knowledge, or EDSL’s role instruction can cue the expected behavior despite fictional stocks. | Real and open. Compare arms and a neutral control, audit actual prompts and comments, freeze rules before the main run, and report sensitivity rather than selecting favorable results. |
| Medium | Incomplete join keys, missing rows, or malformed answers could silently change the denominator. | Fixed in v0. Unique keyed joins and exact design coverage are enforced; unequal signed returns fail the build. Malformed fields become missing, not holds, and decisions use complete matched pairs. |
| Medium | Three pairs per cell and holding period varying with return magnitude make stable inference or separation of scenario factors impossible in v0. | Real and open. Show counts; no confidence intervals or inference in v0. Expand and balance scenarios and freeze uncertainty procedures before main collection. |
| Medium | There was no single offline rebuild or dashboard. | Fixed for local use. The HTML reads generated outputs; public deployment still requires Pages settings and verification. |
| Low | Historical look-ahead and index survivorship could bias a real-securities study. | Not material here: fictional stocks, no market history or index universe, and no realized future prices used as inputs. Reassess if the design incorporates real securities. |

| Course checklist | Status | Evidence / follow-up |
|---|---|---|
| 1. Reproduces | OK | python run_all.py regenerates all v0 data and the result table offline. |
| 2. Input provenance | OK | The four checked-in inputs are documented and hashed. Paid evidence remains a separately disclosed gap. |
| 3. Unit and keys | OK | One row per model, persona, scenario, and version for one run; uniqueness and exact coverage are enforced before keyed joins. |
| 4. Look-ahead | OK | No realized future market data or historically selected sample. |
| 5. LLM leakage | problem | Learned concepts and character cues remain plausible. Inspect raw responses and run prompt sensitivity checks. |
| 6. No p-hacking | problem | Pilot specs are logged; full-study outcomes, comparisons, and rules still require a dated freeze. |
| 7. Magnitudes | OK | Report both component rates, percentage-point gaps, and decision denominators; fixture effects have no behavioral meaning. |
| 8. Hand checks | OK | Fixture counts and the rate difference are checked independently in the regression tests. Repeat on real data after import. |
| 9. Threats to validity | OK | See this audit and the project README for leakage, framing, sample size, and benchmark limits. |
| 10. Team understanding | not yet | Each teammate should rerun v0 and explain join keys, invalid-answer handling, and the paired estimator. |
