# Analysis plan: main study (frozen before collection)

**Team BIB · Inside Out Silicon Investors · FIN 331 · Project seed #13**
**Plan version:** 1.0 · **Written:** November 17, 2026 · **Responds to:** instructor audit finding A2 (and self-audit F11)

This file fixes the primary estimands, tests, multiple-comparison adjustment, failure rules and sign-flip rule **before** any main-study response is collected. Its commit date on `main` must come before `started_utc` in the main run's manifest (`data/raw/<main_run_id>/manifest.json`). Any later change is a deviation: it gets a new plan version, a dated entry in `specs_tried.md`, and the results it touches are labeled exploratory.

## 0. What we have already seen (pilot disclosure)

We wrote this plan **after** looking at the paid pilot `poc_paid_20261025T012651Z` (108 responses, 54 complete pairs, mid-career personas only, 3 scenarios, 1 wording, 1 repeat). In that pilot, the disposition effect (gain-sell minus loss-sell) was:

| | Gain sell | Loss sell | Effect |
|---|---:|---:|---:|
| Claude Haiku 5.5 (27 pairs) | 0.481 | 0.407 | +7.4 pp |
| GPT-5.6 Luna (27 pairs) | 0.556 | 0.778 | −22.2 pp |
| Pooled (54 pairs) | | | −7.4 pp |

Within Embarrassment, the character-name and description arms had opposite signs for both models. The emotion predictions in Section 3 are the ones in `Proposal.md` and `README.md`, written before the pilot; we have not changed them. The pilot is **not** pooled with the main study and is reported only as a pilot.

## 1. Design the plan applies to

| Factor | Levels |
|---|---|
| Models | `gpt-5.6-luna`, `claude-haiku-5-5`, settings as in `inputs/models_poc.csv` (CONFIG-001). Model comparisons are "model + configuration". |
| Emotional personas | 8 emotions × 3 backgrounds (novice, mid-career, retiree) = 24 |
| Prompt arms (emotional personas only) | character name, emotion description |
| Neutral controls | 3, one per background (background-matched, fixes self-audit F8). Neutral text is the same in both arms. |
| Base scenarios | 20 fictional companies, each with a gain and a loss version that differ only in the sign of the return |
| Wordings | 3 rewordings of each scenario (w1 is the baseline) |
| Repeats | 3 fresh calls per cell (cache hits are not repeats) |
| Outcomes | sell/hold (primary); 1–7 likelihood to sell (secondary) |

Collection volume: (24 × 2 + 3) persona prompts × 20 scenarios × 2 versions × 3 wordings × 3 repeats × 2 models = **36,720 observations**. At the pilot's cost per observation (≈ $0.0003) that is about $11. The dollar cap is written into the manifest before launch.

The pair unit is **persona × scenario × wording × repeat × model** (with arm folded into persona). Sell/hold option order is randomized with a saved seed *within* scenario, across repeats, and held fixed within each gain/loss pair (fixes self-audit F3).

## 2. Primary estimands

For a pair *i*, let *d<sub>i</sub>* = sell<sub>gain</sub> − sell<sub>loss</sub> ∈ {−1, 0, +1}. A cell's disposition effect (DE) is the mean of *d<sub>i</sub>* over its complete pairs, in percentage points. Weighting is equal at every level: across repeats, then wordings, then scenarios, then backgrounds and arms. So no factor gets more weight because it has more valid answers.

Separately for **each model** *m*:

- **P1 · Neutral baseline:** DE<sub>neutral,m</sub>, averaged over the 3 background-matched controls, 20 scenarios and 3 wordings. Question: do neutral LLM investors show a disposition effect? It is compared descriptively with Odean (1998), Table I: +5.0 pp.
- **P2 · Emotion shift:** Δ<sub>e,m</sub> = DE<sub>e,m</sub> − DE<sub>neutral,m</sub> for each of the 8 emotions. DE<sub>e,m</sub> averages equally over 3 backgrounds × 2 arms × 3 wordings. Each emotion persona is compared with the neutral control of **the same background**, then averaged.

That makes **2 P1 tests + 16 P2 tests**. We do not pool the two models into one primary estimate; the pilot suggests they may differ in sign.

## 3. Tests, intervals and multiple comparisons

**Unit of resampling.** Every persona and model sees the same 20 base scenarios, so scenarios are the shared source of dependence. Inference resamples or sign-flips at the **base-scenario level**: for each estimand, we first average *d* within scenario (over everything else in the estimand), giving 20 scenario-level values.

- **p-value:** two-sided paired **sign-flip randomization test** on the 20 scenario-level values. Under the null, the gain/loss labels are exchangeable within each scenario. Exact enumeration of all 2<sup>20</sup> sign patterns (≈ 1.05 million).
- **95% interval:** percentile **paired bootstrap over base scenarios**, B = 10,000, seed 331.
- **Adjustment:** **Holm** at family-wise α = 0.05, run **separately** within two families:
  - P1: 2 tests (one per model);
  - P2: 16 tests (8 emotions × 2 models).

  Both raw and Holm-adjusted p-values are reported.
- **Direction:** the tests are two-sided. We report each emotion's result against the prediction below as a hit (significant in the predicted direction), a miss (significant in the opposite direction) or not detected.

| Emotion | Prediction (Proposal) | Predicted sign of Δ (vs. neutral) |
|---|---|---|
| Joy | Sells winners quickly | + |
| Sadness | Holds losers | + |
| Anger | Holds losers to "make it back" | + |
| Embarrassment | Holds losers to avoid admitting a mistake | + |
| Disgust | Sells losers quickly | − |
| Envy | Holds winners (binary task tests holding only) | − |
| Fear | Sells winners early; may also sell losers | ambiguous |
| Anxiety | Sells winners early; may also sell losers | ambiguous |

The 3 persona clusters per emotion and background are treated as fixed design cells, not as a sample of personas. Emotion-level intervals describe uncertainty over scenarios only, and we will say so.

## 4. Sign-flip rule (wording and arm robustness)

For every primary estimand, we also compute the estimate and its 95% bootstrap interval **separately for each wording** (w1, w2, w3) and, for P2, **for each arm**. Each estimand is labeled as follows:

- **Robust sign:** all three wording estimates have the same sign as the pooled estimate.
- **Unstable sign:** the point estimates differ in sign across wordings, but no wording's interval excludes zero in the opposite direction.
- **Sign flip:** at least one wording has an interval entirely above zero and another has an interval entirely below zero.

**Claim rule:** we describe an effect's direction in the text only if it is Holm-significant **and** has a robust sign across wordings. Otherwise we report it as wording-dependent. The full table of per-wording and per-arm estimates is published for every estimand, including nulls. An arm disagreement (as in the pilot's Embarrassment cell) is reported as a result in its own right (S1 below). It does not by itself block a claim about the pooled emotion shift, but it is stated next to it.

## 5. Validity, missing data and failure rules

1. **Valid decision:** the answer maps exactly to the displayed *Sell* or *Hold* option. Refusals, blanks, off-scale or ambiguous answers are **invalid** and never coded as hold (tested in `tests/test_build_dataset.py`).
2. **Retries:** only transport failures (no model response: timeout, rate limit, server error) are retried, at most 2 times. A response that arrives but is invalid is **not** retried; it is kept as invalid. Every attempt is saved with an `attempt_id`, and the analyzed attempt is the first one that returned a response.
3. **Cache:** remote cache off, fresh local cache per run. A cache hit is not a repeat. Any cache hits are reported and dropped from the analysis.
4. **Complete pairs:** the primary analysis uses pairs where both the gain and loss decisions are valid. Incomplete pairs are counted and reported for each model × emotion × arm, never silently dropped.
5. **Cell warning:** a model × emotion cell is flagged when its invalid share exceeds **10%**, or when the gain and loss invalid shares differ by more than **5 pp**. For flagged cells we also report worst-case bounds: invalid gain answers treated as all sell and invalid loss answers as all hold (upper bound), and the reverse (lower bound).
6. **Model failure:** if a model has fewer than **80%** valid decisions overall, its primary results are reported as "not interpretable" and its tests are left out of the Holm families. This is recorded in `specs_tried.md`.
7. **Budget stop:** if the dollar cap is reached mid-run, we analyze only fully completed scenario blocks (all personas and versions for a scenario) and report the shortfall.
8. **One run:** one frozen main-run manifest. Reruns are never pooled as extra observations. A rerun after a failure gets a new `run_id`, and the reason is logged.
9. **Recitation check:** comments that cite theory (regex in `code/poc_analyze.py`, plus hand-reading at least 10 per model) are reported by cell. They are **not** excluded from the primary analysis. A secondary analysis drops them (S5).

## 6. Secondary and exploratory analyses (labeled as such)

These have no family-wise control. Where several are tested together we report Benjamini–Hochberg q-values, and every estimate is labeled **exploratory**.

- **S1 · Arm contrast:** character name minus description, for each emotion × model (16 estimates).
- **S2 · Rating gap:** mean sell rating in gain minus in loss, for the same P1 and P2 contrasts.
- **S3 · Background:** emotion shifts estimated separately for each background.
- **S4 · Magnitude:** DE by absolute return (5 / 10 / 20%).
- **S5 · Without recitation:** P1 and P2 re-estimated after dropping flagged comments.
- **S6 · Model contrast:** DE<sub>neutral</sub> for Luna minus for Haiku.
- **S7 · Decision–rating agreement:** share of Sell decisions with a rating ≥ 5 and of Hold decisions with a rating ≤ 3 (self-audit F10).

## 7. Deviations

Any change after this file is merged (new models, prompts, scenarios, tests, thresholds or exclusions) gets:
- a new plan version at the top of this file;
- a dated `specs_tried.md` row explaining why;
- an "exploratory" label on every result it affects.

The original version stays in the git history.
