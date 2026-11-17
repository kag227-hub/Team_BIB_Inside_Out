# Team BIB: “Inside Out” Silicon Investors

[Open the public dashboard](https://teambibinsideout-tkgtmunmsq9qkk3gjgrgdd.streamlit.app/)

Updated November 17, 2026.

Read the [proposal](PROPOSAL.md) and [project status](STATUS.md) for the research motivation, completed pilot, and remaining work.

**FIN 331 final project · Project seed #13 · Python + EDSL**

Do LLM investor personas show the **disposition effect**—a greater tendency to sell investments with gains than investments with losses—and does that tendency depend on emotion or model?

The planned full study covers investors inspired by the emotions in *Inside Out*: **Joy, Sadness, Anger, Fear, Disgust, Anxiety, Envy, and Embarrassment**. Each emotion is crossed with three backgrounds: novice investor, mid-career saver, and retiree. A neutral, no-emotion investor provides a reference.

**Current status.** The paid pilot is complete. It collected 108 survey observations across two models and nine personas, producing 54 complete gain/loss pairs. The public Streamlit dashboard displays its aggregate results. The offline pipeline rebuilds both paid and synthetic runs from committed raw files. The larger eight-emotion, three-background study is planned.

**Paid pilot, October 24, 2026 (ET).** GPT-5.6 Luna and Claude Haiku 5.5 evaluated Joy, Sadness, Fear, and Embarrassment in character-name and emotion-description prompts, plus a neutral control. Each persona evaluated three fictional scenarios in gain and loss versions. The recorded job charge was $0.0307. The run ID is `poc_paid_20261025T012651Z` because collection occurred on October 25 in UTC. See [Checkpoint 1](STATUS.md), [pilot instructions](POC_README.md), and [model selection](MODEL_SELECTION.md).

The pilot has three matched pairs per model and persona cell. For Embarrassment, the gain-minus-loss gap changes from −66.7 to +33.3 percentage points across prompt arms for GPT-5.6 Luna, and from −33.3 to +66.7 for Claude Haiku 5.5. With so few pairs, these estimates are exploratory. Confidence intervals, additional wording checks, and the expanded study remain to be completed.

## How to run (Checkpoint 2 · v0)

```bash
python -m pip install -r requirements.txt
python run_all.py                     # rebuilds derived files for raw runs present locally
python -m unittest discover -s tests   # offline checks
streamlit run dashboard/app.py        # displays the saved public paid-pilot aggregates
```

| Step | File | Reads → writes |
|---|---|---|
| 1. Collect (paid, deliberate; not run by `run_all.py`) | `code/poc_run.py` | `inputs/*_poc.csv` → `data/raw/<run_id>/` (raw EDSL results, prompts, manifest) |
| 2. Build dataset | `code/build_dataset.py` | `data/raw/<run_id>/raw_results.csv` → `outputs/<run_id>_responses.csv` |
| 3. Analyze | `code/poc_analyze.py` | → `*_feasibility.md`, `*_rates.csv`, `*_cost_projection.csv` |
| 4. Table + figure | `code/make_figures.py` | → `*_summary_table.csv/.md`, `*_disposition_by_persona.png` |
| 4b. Cue ablation (audit A3; ablation runs only) | `code/cue_ablation.py` | → `*_cue_ablation.csv/.md`: disposition effect with and without each demand cue |
| 5. Dashboard | `dashboard/app.py` | `outputs/public_paid_pilot.json` (paid pilot aggregates only) |

**Data and offline reproducibility.** The repository includes the paid run's saved EDSL Results CSV, rendered prompts, and manifest in `data/raw/poc_paid_20261025T012651Z/`. It contains 108 survey observations and 54 complete gain/loss pairs. `python run_all.py` rebuilds the paid dataset, analysis, table, figure, and `outputs/public_paid_pilot.json`, as well as the synthetic test run. The dashboard reads the regenerated paid export.

The saved CSV retains answers, model comments, exact prompts, settings, and usage/cost fields. Provider response envelopes, internal reasoning summaries, and cache identifiers were omitted from this public copy. The recovered manifest records the original download hash, public CSV hash, omissions, and reported job charge. It was reconstructed from the saved run and is identified as recovered provenance. The original binary `.ep` artifact is unavailable locally. All retained CSV fields were checked against the original download. No new model calls are required.

To verify the dashboard export from a fresh clone, run the pipeline and then check `git diff --exit-code -- outputs/public_paid_pilot.json`. A zero exit code confirms the generated export matches the committed file byte for byte.

**Dashboard hosting.** The published app uses branch `main`, entry point `dashboard/app.py`, and dependencies in `dashboard/requirements.txt`. It reads `outputs/public_paid_pilot.json`. The Intro, Methodology, Results, and Explore pages show pilot counts, sell rates, and gaps, with model, emotion, and prompt-arm filters.

**Analysis plan (frozen before the main run):** [ANALYSIS_PLAN.md](ANALYSIS_PLAN.md).

**Self-audit:** [audits/01_self_audit.md](audits/01_self_audit.md).

## Why this question matters

A fintech designing investor nudges could use evidence about how simulated emotions affect sell/hold decisions. Researchers could use it to assess whether LLM “silicon subjects” reproduce a documented human pattern. Agreement with a human benchmark would not, by itself, establish that LLMs behave like real investors.

## Personas and predictions

The planned full design contains **24 emotional personas + 1 neutral control = 25 personas**. The neutral control has a fixed, generic investor background; it is not three additional personas. Background-matched neutral controls and a rational-economist control are optional extensions and increase the budget.

These predictions guide the planned main study. The pilot has already been examined. Before the main run, timestamp the hypotheses, comparisons, failure rules, and budget, and identify any predictions changed after the pilot.

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

## Planned main-study design

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

## Outcomes and analysis plan

The implemented analysis reports matched sell rates and gaps. The expanded background, wording, and uncertainty comparisons below are planned. For each persona, model, prompt arm, and wording:

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

## Planned main-study EDSL pipeline

**These are the main-study files.** The pilot versions of collection, dataset building, analysis, `run_all.py` and the dashboard now exist (see "How to run" above); the main-study tables and design expansion remain planned. EDSL is pinned to 1.0.9.

| Planned file | Purpose |
|---|---|
| `inputs/personas.csv` | Persona ID, emotion, background, control flag, and text for each prompt arm. |
| `inputs/scenarios.csv` | Base scenario ID, magnitude, holding period, fixed financial assumptions, and wording templates. |
| `inputs/models.csv` | Provider, exact model ID, settings, and dated price sources. |
| `code/build_design.py` | Expand personas × scenarios × gain/loss × models × arms × wordings × repeats; save seeded option order and prompt hashes. |
| `code/run_survey.py` | Build EDSL agents/scenarios and a sell/hold plus rating survey; save rendered prompts, raw responses, usage, and failures. |
| `code/analyze.py` | Validate keys/pairs, normalize answers, compute component rates and gaps, and produce intervals and hand-check tables from saved data. |
| `run_all.py` (implemented) | Rebuild derived outputs for raw runs present locally. The public checkout includes the synthetic run. |
| `dashboard/app.py` (implemented) | Display paid-pilot aggregate counts and sell rates. Response-level drill-down is a planned extension. |
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

The current dashboard displays paid-pilot summary tables and filtered gain/loss sell-rate charts. Confidence intervals, background and wording filters, response-level drill-down, and a neutral-control reference line are planned extensions.

The planned dashboard will show an **emotion × model grid** of disposition effects and confidence intervals, with filters for background, wording, and prompt arm. Each cell opens the underlying prompts and raw responses. Show the neutral-control estimate as a reference line within each model and arm, plus sample sizes and failure rates. Keep optional rational-control results distinct.

Before the final submission:

- Retain pinned dependencies and the documented offline commands, and record the supported Python version.
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

The [self-audit](audits/01_self_audit.md) records the outstanding checks. Uncertainty intervals, manual review of model comments, and a frozen main-study analysis plan are still pending. Paid answers, prompts, and the recovered manifest are now committed for response-level verification. In the pilot, return magnitude varies with company and holding period, option order is fixed within each scenario, and the neutral control has a generic background. These factors limit comparisons across cells.


- **Caricature and demand effects:** named fictional characters may produce stereotypes or familiar scripts. Description and neutral arms help assess sensitivity. Two prompt cues, the "past price moves say nothing about its future" sentence and EDSL's "Do not break character" instruction, are tested by switching them off (ANALYSIS_PLAN.md, S8; `python code/poc_run.py --ablation`). The word "fictional" stays and is a remaining cue.
- **Training leakage:** models may know the disposition-effect literature even when companies are fictional. Hiding the hypotheses reduces explicit cues but cannot remove prior knowledge.
- **Prompt sensitivity:** wording, question sequence, and option order may change the answer. Save them and report robustness results, including sign reversals.
- **Limited external validity:** hypothetical LLM choices lack real money, consequences, and human emotional experience.
- **Benchmark mismatch:** brokerage realization opportunities differ from our balanced experimental decisions; a similar gap does not establish human equivalence.
- **Dependence and small samples:** repeated outputs, shared prompts, and only three backgrounds per emotion limit inference; deterministic decoding or cached repeats may add no information.
- **Model drift:** provider updates can change responses despite the same model alias. Record available version metadata and preserve raw outputs.
- **Missingness and parsing:** refusals, malformed answers, and unequal failures can bias comparisons. Report them by cell and apply the frozen handling rule.
- **Researcher discretion:** many emotions, models, wordings, and outcomes create opportunities to select favorable results. Freeze primary tests and log every attempted specification.
- **Ambiguous rational choice:** equal expected returns alone do not make holding and selling economically equivalent. Fix future risk, alternatives, taxes, costs, and liquidity assumptions, and state the rational-control decision rule explicitly.
