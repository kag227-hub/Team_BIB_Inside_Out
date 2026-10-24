# Team BIB: “Inside Out” Silicon Investors

**FIN 331 final project · Project seed #13 · Python + EDSL**

Do LLM investor personas show the **disposition effect**—a greater tendency to sell investments with gains than investments with losses—and does that tendency depend on emotion or model?

We study investors inspired by the emotions in *Inside Out*: **Joy, Sadness, Anger, Fear, Disgust, Anxiety, Envy, and Embarrassment**. Each emotion is crossed with three backgrounds: novice investor, mid-career saver, and retiree. A neutral, no-emotion investor provides a reference.

**Status:** experimental design and pipeline plan. This README does not report experimental results. Model choices, exact prompts, budget, and analysis specifications must be frozen and timestamped before the main run. If any pilot responses have already been examined, disclose them and label subsequent predictions accordingly.

**Checkpoint 1 update (October 24, 2026):** pilot collection and analysis scripts are implemented and have passed a synthetic dry run. GPT-5.6 Luna and Claude Haiku 5.5 are selected for the paid pilot; credentials and live availability still need verification. See [POC_README.md](POC_README.md), [MODEL_SELECTION.md](MODEL_SELECTION.md), and [STATUS_checkpoint1.md](STATUS_checkpoint1.md). The larger study described below remains planned.

## Why this question matters

A fintech designing investor nudges could use evidence about how simulated emotions affect sell/hold decisions. Researchers could use it to assess whether LLM “silicon subjects” reproduce a documented human pattern. Agreement with a human benchmark would not, by itself, establish that LLMs behave like real investors.

## Personas and predictions

The primary design contains **24 emotional personas + 1 neutral control = 25 personas**. The neutral control has a fixed, generic investor background; it is not three additional personas. Background-matched neutral controls and a rational-economist control are optional extensions and increase the budget.

These are proposed predictions to register before running, not findings:

| Emotion | Predicted behavior |
|---|---|
| Joy | Pride in gains leads to selling winners quickly. |
| Sadness | Regret leads to holding losers. |
| Anger | Holds losers to “make it back.” |
| Fear | Sells winners early; may also sell losers to reduce exposure. |
| Disgust | Sells losers quickly. |
| Anxiety | Sells winners early; may also sell losers to reduce uncertainty. |
| Envy | Holds or chases winners; the binary task tests the holding prediction only. |
| Embarrassment | Holds losers to avoid admitting a mistake. |

The outcome includes both gain-side and loss-side sell rates: some predictions concern one side without uniquely predicting the sign of the overall disposition effect. Report misses and ambiguous predictions.

**Prompt arms:**

1. **Character-name arm:** names the Inside Out emotion character and supplies a fixed investor background.
2. **Emotion-description arm:** describes the same emotional tendency without the character or film name.

Keep the background and all financial facts identical across arms. Match emotional content as closely as possible and save the exact texts. This comparison tests sensitivity to character cues, although wording differences prevent a perfectly isolated test of psychology.

## Experimental design

- Generate **20 base scenarios** using fictional companies with no real ticker, news, or identifiable historical event.
- Each scenario has a **gain and loss version**, differing only in the sign of the return since purchase: for example, +10% versus −10%.
- Include absolute return magnitudes of **5%, 10%, and 20%** and vary holding periods. Save the exact allocation of the 20 scenarios before running; 20 is not assumed to be a balanced full factorial.
- State that the distribution of future returns, including expected return and risk, is identical across the paired versions and independent of the past move.
- Hold position size, portfolio context, liquidity needs, taxes, and transaction costs fixed across each pair. Explicitly exclude taxes and trading costs in the baseline.
- Ask for **sell or hold** and a **1–7 likelihood-to-sell rating**, where 1 means very unlikely and 7 means very likely.
- Randomize sell/hold display order using a saved seed; keep that order identical within a gain/loss pair. Save the mapping from displayed option to sell/hold.
- Give each decision fresh conversation context so one scenario does not reveal another.
- Use **two models**, preserving provider, exact model identifier/version where available, generation settings, run date, and any provider-reported version metadata.
- Prepare **three rewordings** of each scenario as a robustness arm. Within each wording, gain/loss prompts must remain identical except for the return sign.
- Repeat each design cell several times, distinguishing fresh calls from cached responses.

Do not tell experimental personas the hypotheses, the term “disposition effect,” or Odean’s findings. An optional rational-economist control should receive a decision rule based on future payoffs, not the expected experimental answer.

## Outcomes and analysis

For each persona, model, prompt arm, and wording:

```text
gain_sell_rate = valid sell decisions in gain cases / valid gain decisions
loss_sell_rate = valid sell decisions in loss cases / valid loss decisions
disposition_effect = gain_sell_rate - loss_sell_rate
rating_gap = mean sell rating in gain cases - mean sell rating in loss cases
```

A positive disposition effect means a greater tendency to sell winners; a negative effect means a greater tendency to sell losers. Report both component rates, sample sizes, missingness, effect sizes in percentage points, and uncertainty. The rating gap is a secondary outcome.

Use matched gain/loss pairs as the primary comparison. Define the complete-pair rule before collection; flag incomplete pairs and report failures by treatment rather than silently dropping them. Invalid or refused responses must never become “hold.” Save retries as separate attempts and choose the analyzed attempt using a pre-specified rule.

Calculate estimates **separately for each model**. For emotion summaries, weight the three backgrounds equally; retain persona-level estimates. Compare every wording with the baseline and report sign flips, including zero or uncertain estimates.

For pooled comparisons across personas, cluster standard errors by persona and preserve pairing across scenarios, repeats, and arms. A single-persona estimate cannot have standard errors clustered by persona: use a paired bootstrap over base scenarios for its interval. Emotion-specific summaries have only three persona clusters, so label their uncertainty exploratory and disclose the small-cluster limitation. Repeated calls are not additional human subjects. Pre-specify primary comparisons and a multiple-comparison adjustment before examining results.

### Human benchmark

Odean (1998), **Table I, entire-year sample**, reports a proportion of gains realized (PGR) of **0.148** and a proportion of losses realized (PLR) of **0.098**. Under our gain-minus-loss convention, the published rounded values imply **+0.050, or 5.0 percentage points**. The paper displays its difference using the reverse sign convention.

Source: Terrance Odean, *Are Investors Reluctant to Realize Their Losses?*, Journal of Finance 53(5), 1775–1798, [publisher article and Table I](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00072). Benchmark checked October 15, 2026.

Odean uses realized and paper opportunities in brokerage records; we use prompted hypothetical decisions. Our sell-rate gap is an experimental analogue, not an exact replication of the brokerage estimator. Compare magnitudes with that qualification.

## Planned EDSL pipeline

**The files below are proposed deliverables, not files already implemented.** Pin the EDSL version and verify its survey, cache, and model interfaces during implementation.

| Planned file | Purpose |
|---|---|
| `inputs/personas.csv` | Persona ID, emotion, background, control flag, and text for each prompt arm. |
| `inputs/scenarios.csv` | Base scenario ID, magnitude, holding period, fixed financial assumptions, and wording templates. |
| `inputs/models.csv` | Provider, exact model ID, settings, and dated price sources. |
| `code/build_design.py` | Expand personas × scenarios × gain/loss × models × arms × wordings × repeats; save seeded option order and prompt hashes. |
| `code/run_survey.py` | Build EDSL agents/scenarios and a sell/hold plus rating survey; save rendered prompts, raw responses, usage, and failures. |
| `code/analyze.py` | Validate keys/pairs, normalize answers, compute component rates and gaps, and produce intervals and hand-check tables from saved data. |
| `run_all.py` | Rebuild analysis outputs from committed raw responses without paid API calls by default. |
| `app.py` | Read saved outputs and show estimates plus response-level drill-down. |
| `specs_tried.md` | Append-only record of every tested persona, wording, model, specification, pilot, and deviation, including null results. |
| `cost_log.csv` | Estimated and actual tokens/spend, call counts, cache hits, retries, pricing source/date, and run ID. |

Conceptual execution order:

```text
load and validate persona, scenario, and model tables
freeze manifest, hypotheses, specification IDs, seeds, and budget
expand and save design; assert unique keys and sign-only pairing
estimate survey-level API requests and token costs
run a labeled pilot; log any changes before freezing the main design
collect through EDSL with explicit cache/repeat policy
save raw artifacts before parsing or analysis
validate and join tables with merge cardinality checks
compute matched sell-rate gaps and rating gaps separately per model
export estimates, uncertainty, failure summaries, and hand checks
render dashboard using saved files only
```

### Dataset contract

One analyzed row is **one persona’s survey response to one scenario version, model, repeat, prompt arm, and wording**. The two survey answers belong to that row even if EDSL requires two underlying requests.

The unique analysis key is:

```text
run_id × persona_id × scenario_id × version × model_id
       × repeat × prompt_arm × wording_id
```

Require `version` to be gain/loss, normalized `sell` to be 0/1 for valid decisions, and `sell_rating` to be an integer from 1 to 7. Keep validity flags for each answer. Preserve emotional/background traits, signed return, option order, specification ID, prompt hash, raw-response reference, UTC timestamp, provider request ID if available, usage, and cache status.

Keep raw attempts separately with an additional `attempt_id`. Never overwrite failed attempts. Retain a single frozen main-run manifest; do not pool successive reruns as extra observations.

## Scale and cost

| Scope | Survey observations |
|---|---:|
| 2 models × 25 personas × 20 scenarios × 2 versions, one arm/wording/repeat | 2,000 |
| Same design with 3 repeats | 6,000 |
| Both prompt arms with 3 repeats, one wording | 12,000 |
| Both prompt arms, 3 wordings, and 3 repeats | 36,000 |

These are **survey observations, not guaranteed API-call counts**. A two-question EDSL survey may issue two requests per observation, before retries; a structured combined response may use one. Verify the chosen implementation before pricing.

Estimate costs separately per model:

```text
estimated_cost =
    estimated_input_tokens / 1,000,000 × input_price_per_million
  + estimated_output_tokens / 1,000,000 × output_price_per_million
```

Include repeated persona/system text, question overhead, any second-question context, provider-billed reasoning tokens where relevant, retries, and caching assumptions. Record price URLs and access dates. Choose models, set a dollar cap, and record the estimate before launching paid collection. Reconcile actual usage and spend afterward; label unavailable billing fields rather than inventing them.

## Dashboard and reproducibility

The dashboard will show an **emotion × model grid** of disposition effects and confidence intervals, with filters for background, wording, and prompt arm. Each cell opens the underlying prompts and raw responses. Show the neutral-control estimate as a reference line within each model and arm, plus sample sizes and failure rates. Keep optional rational-control results distinct.

Before the final submission:

- Pin Python/dependency versions and document exact setup and offline rerun commands once implemented.
- Commit prompt templates, design tables, manifests, provenance, run dates, and raw responses sufficient for analysis without new API calls.
- Assert uniqueness using the full key; check expected cell counts and incomplete pairs.
- Compare rendered paired prompts and assert that only the signed return changes.
- Use `validate=` for dataframe merges and check unmatched rows.
- Keep every attempted specification in `specs_tried.md`; disclose pilots and exploratory changes.
- Independently hand-check at least one design pair, parsed response, token-cost calculation, and effect estimate.
- Generate every reported number and figure from files in `outputs/`.
- Keep credentials in environment variables or ignored local secrets, never in Git.
- Have every teammate explain the design, parsing, estimators, uncertainty, and limitations.

## Threats to validity

- **Caricature and demand effects:** named fictional characters may produce stereotypes or familiar scripts. Description and neutral arms help assess sensitivity.
- **Training leakage:** models may know the disposition-effect literature even when companies are fictional. Hiding the hypotheses reduces explicit cues but cannot remove prior knowledge.
- **Prompt sensitivity:** wording, question sequence, and option order may change the answer. Save them and report robustness results, including sign reversals.
- **Limited external validity:** hypothetical LLM choices lack real money, consequences, and human emotional experience.
- **Benchmark mismatch:** brokerage realization opportunities differ from our balanced experimental decisions; a similar gap does not establish human equivalence.
- **Dependence and small samples:** repeated outputs, shared prompts, and only three backgrounds per emotion limit inference; deterministic decoding or cached repeats may add no information.
- **Model drift:** provider updates can change responses despite the same model alias. Record available version metadata and preserve raw outputs.
- **Missingness and parsing:** refusals, malformed answers, and unequal failures can bias comparisons. Report them by cell and apply the frozen handling rule.
- **Researcher discretion:** many emotions, models, wordings, and outcomes create opportunities to select favorable results. Freeze primary tests and log every attempted specification.
- **Ambiguous rational choice:** equal expected returns alone do not make holding and selling economically equivalent. Fix future risk, alternatives, taxes, costs, and liquidity assumptions, and state the rational-control decision rule explicitly.
