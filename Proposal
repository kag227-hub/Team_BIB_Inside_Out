# Inside Out Silicon Investors

**Team BIB · FIN 331**  
**Team members:** Natalie Leung, Ayushi Jain, Lily Notivsky, Kara Grossman

## Research question

Investors often have a general sense of their risk appetite, but many other aspects of personality may shape where and when they invest. Can we quantify these differences and categorize investment decisions by personality type? Could understanding an investor’s tendencies help them diversify?

We aim to explore these questions in **Inside Out Silicon Investors**, a project inspired by the Pixar film *Inside Out*. We use six of its emotions and add two more:

| Persona | Predicted investing behavior |
|---|---|
| **Joy** | Pride in gains leads to selling winners quickly. |
| **Sadness** | Regret leads to holding losers. |
| **Anger** | Holds losers to “make it back.” |
| **Fear** | Sells winners early; may also sell losers to reduce exposure. |
| **Disgust** | Sells losers quickly. |
| **Envy** | Holds or chases winners; our binary task tests the holding prediction only. |
| **Anxiety** | Sells winners early; may also sell losers to reduce uncertainty. |
| **Embarrassment** | Holds losers to avoid admitting a mistake. |

We plan to train different models to study these personas. The results could help predict how different personality types respond to market movements and offer a tool for exploring investment advice.

## Who could use the results?

A fintech team designing a trading app could use this study to assess whether simulated investors respond consistently enough to help screen ideas before recruiting human participants. Retail investors could also use the results to reflect on how different personas might react to market news—and how contradictory tendencies might affect their own diversification decisions.

One design question is whether showing the original purchase price prominently on a sell screen changes how users respond to gains and losses. If simulated decisions shift with small changes in wording, product teams would have a concrete reason to put less weight on those responses when deciding what to test with customers.

## Data and sample

Each row represents one model’s response to one persona and one version of a fictional scenario in a run. The main analysis fields are the model, persona, prompt type, scenario, signed return, and sell-or-hold decision. We also collect a 1–7 likelihood-to-sell rating as a secondary outcome. Written explanations and token usage support interpretation and cost tracking.

Our offline Checkpoint 2 dataset contains **108 synthetic rows** across two model labels, nine personas, and three scenarios, each with a gain and a loss version. For example, the synthetic Claude Haiku 5.5 response to the Embarrassment description and Brightwater Logistics records **Hold** and a likelihood-to-sell rating of **1 out of 7** at **+5%**. Its matched **−5%** row also records Hold and 1 out of 7.

Separately, the paid pilot collected **108 model responses** on October 24, 2026, yielding **54 complete gain/loss pairs**. The companies are fictional, so we would set and record the collection window before the larger run.

The team records:

- Persona prompts in `inputs/personas_poc.csv`
- Scenarios in `inputs/scenarios_poc.csv`
- Model IDs and settings in `inputs/models_poc.csv`
- Synthetic responses in `inputs/v0_responses.csv`

The paid collection script uses EDSL. We save raw responses and prompts to support rerunning the analysis. The public dashboard displays aggregate pilot results.

## Method

Each scenario has a gain and loss version of the same magnitude. For example, one prompt says a fictional stock is up 10% since purchase, while the other says it is down 10%. The firm, holding period, and expected future return remain the same. We compare character-name prompts with plain descriptions of the corresponding emotions and include a neutral investor as a reference.

`run_all.py` validates the offline inputs and builds the row-level dataset, sell-rate summary, and dashboard data. For each model and persona, we calculate:

> **Gain/loss sell-rate gap = percentage of gain cases where the model sells − percentage of loss cases where the model sells**

For example, if a model sells in 60% of gain cases and 40% of loss cases, the gap is **20 percentage points**. We include pairs with two valid decisions and report how many pairs contributed to each estimate. A positive gap means the model sold more often in gain scenarios.

We report results by model and prompt type, then check whether the direction of the gap holds across scenario rewordings.

## Threats and checks

Models may recognize the characters or reproduce familiar behavioral-finance answers. We use fictional firms and compare character names with plain emotion descriptions. The fictional scenarios contain no realized future prices or historical stock universe, limiting look-ahead and survivorship concerns in this design.

Duplicate rows, missing answers, or mismatched gain/loss versions could shift the estimates. We will check that response keys are unique, verify that matched scenarios differ only in the return’s sign, and report how many pairs were excluded.

The paid pilot has three pairs per model-and-persona combination, so a single decision can move a cell’s gap by about **33 percentage points**. We will use the pilot to check the experiment and report uncertainty in the larger study. Before collecting the larger sample, we will record our predictions and primary comparisons and log the specifications we try.

## Dashboard mockup

*[Insert your dashboard screenshot here.]*

The dashboard lets readers filter by model and persona prompt type, compare gain and loss sell rates, and see the gap and number of pairs behind each estimate. The neutral persona provides a reference for interpreting the character results.
