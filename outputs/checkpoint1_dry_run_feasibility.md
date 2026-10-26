# PoC feasibility report: poc_TEST_validated

**SYNTHETIC DRY RUN: validates plumbing only. No behavioral evidence or paid spending.**

## 1. Valid answers (share of rows)

|                                 |   n |   sell_valid |   rating_valid |
|:--------------------------------|----:|-------------:|---------------:|
| ('test', 'character_name')      |  24 |            1 |              1 |
| ('test', 'control')             |   6 |            1 |              1 |
| ('test', 'emotion_description') |  24 |            1 |              1 |

## 2. Matched pairs

- Pairs expected: 27
- Complete pairs (both answers valid): 27
- Incomplete pairs: 0 (kept and reported, never dropped silently)

## 3. Comment flags (share of rows)

|                                 |   mentions_theory |   breaks_character |
|:--------------------------------|------------------:|-------------------:|
| ('test', 'character_name')      |                 0 |                  0 |
| ('test', 'control')             |                 0 |                  0 |
| ('test', 'emotion_description') |                 0 |                  0 |

Read 10 comments per model by hand too; regex flags miss things.

## 4. Sell rates (complete pairs only; at most 3 pairs per cell; exploratory)

|                                                                            |   gain_sell_rate |   loss_sell_rate |   n_gain |   n_loss |   disposition_effect_pp |
|:---------------------------------------------------------------------------|-----------------:|-----------------:|---------:|---------:|------------------------:|
| ('test', 'embarrassment_mid_desc', 'Embarrassment', 'emotion_description') |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'embarrassment_mid_name', 'Embarrassment', 'character_name')      |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'fear_mid_desc', 'Fear', 'emotion_description')                   |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'fear_mid_name', 'Fear', 'character_name')                        |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'joy_mid_desc', 'Joy', 'emotion_description')                     |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'joy_mid_name', 'Joy', 'character_name')                          |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'neutral_generic', 'Neutral', 'control')                          |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'sadness_mid_desc', 'Sadness', 'emotion_description')             |                0 |                0 |        3 |        3 |                       0 |
| ('test', 'sadness_mid_name', 'Sadness', 'character_name')                  |                0 |                0 |        3 |        3 |                       0 |

## 5. Cost (actual) and projection to the full design

| model_id   |   observations |   total_cost_usd |   cost_per_obs_usd |   share_cached |   mean_decision_input_tokens |   mean_decision_output_tokens |   mean_sell_rating_input_tokens |   mean_sell_rating_output_tokens | proj_mvp_2000_usd   | proj_arms_repeats_12000_usd   | proj_full_36000_usd   |
|:-----------|---------------:|-----------------:|-------------------:|---------------:|-----------------------------:|------------------------------:|--------------------------------:|---------------------------------:|:--------------------|:------------------------------|:----------------------|
| test       |             54 |                0 |                nan |              0 |                            1 |                             1 |                               1 |                                1 |                     |                               |                       |

Synthetic runs have $0 spend and no cost extrapolation. Real-run projections use fully uncached observations only. Missing cost metadata remains unknown; provider/Expected Parrot billing must be reconciled separately.

## 6. Hand-check pair (verify against *_prompts.csv and the raw results)

| persona_id             | scenario_id   | version   | model_id   | decision_raw      |   sell |   sell_rating_raw |   sell_rating |   obs_cost_usd |
|:-----------------------|:--------------|:----------|:-----------|:------------------|-------:|------------------:|--------------:|---------------:|
| embarrassment_mid_desc | s01           | gain      | test       | Hold the position |      0 |                 4 |             4 |              0 |
| embarrassment_mid_desc | s01           | loss      | test       | Hold the position |      0 |                 4 |             4 |              0 |
