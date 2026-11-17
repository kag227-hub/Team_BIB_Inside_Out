# PoC feasibility report: poc_paid_20261025T012651Z

## 1. Valid answers (share of rows)

|                                             |   n |   sell_valid |   rating_valid |
|:--------------------------------------------|----:|-------------:|---------------:|
| ('claude-haiku-5-5', 'character_name')      |  24 |            1 |              1 |
| ('claude-haiku-5-5', 'control')             |   6 |            1 |              1 |
| ('claude-haiku-5-5', 'emotion_description') |  24 |            1 |              1 |
| ('gpt-5.6-luna', 'character_name')          |  24 |            1 |              1 |
| ('gpt-5.6-luna', 'control')                 |   6 |            1 |              1 |
| ('gpt-5.6-luna', 'emotion_description')     |  24 |            1 |              1 |

## 2. Matched pairs

- Pairs expected: 54
- Complete pairs (both answers valid): 54
- Incomplete pairs: 0 (kept and reported, never dropped silently)

## 3. Comment flags (share of rows)

|                                             |   mentions_theory |   breaks_character |
|:--------------------------------------------|------------------:|-------------------:|
| ('claude-haiku-5-5', 'character_name')      |             0     |                  0 |
| ('claude-haiku-5-5', 'control')             |             0.333 |                  0 |
| ('claude-haiku-5-5', 'emotion_description') |             0     |                  0 |
| ('gpt-5.6-luna', 'character_name')          |             0     |                  0 |
| ('gpt-5.6-luna', 'control')                 |             0     |                  0 |
| ('gpt-5.6-luna', 'emotion_description')     |             0     |                  0 |

Read 10 comments per model by hand too; regex flags miss things.

## 4. Sell rates (complete pairs only; at most 3 pairs per cell; exploratory)

|                                                                                        |   gain_sell_rate |   loss_sell_rate |   n_gain |   n_loss |   disposition_effect_pp |
|:---------------------------------------------------------------------------------------|-----------------:|-----------------:|---------:|---------:|------------------------:|
| ('claude-haiku-5-5', 'embarrassment_mid_desc', 'Embarrassment', 'emotion_description') |            0.667 |            0     |        3 |        3 |                  66.667 |
| ('claude-haiku-5-5', 'embarrassment_mid_name', 'Embarrassment', 'character_name')      |            0.333 |            0.667 |        3 |        3 |                 -33.333 |
| ('claude-haiku-5-5', 'fear_mid_desc', 'Fear', 'emotion_description')                   |            1     |            1     |        3 |        3 |                   0     |
| ('claude-haiku-5-5', 'fear_mid_name', 'Fear', 'character_name')                        |            1     |            1     |        3 |        3 |                   0     |
| ('claude-haiku-5-5', 'joy_mid_desc', 'Joy', 'emotion_description')                     |            0     |            0.333 |        3 |        3 |                 -33.333 |
| ('claude-haiku-5-5', 'joy_mid_name', 'Joy', 'character_name')                          |            0     |            0     |        3 |        3 |                   0     |
| ('claude-haiku-5-5', 'neutral_generic', 'Neutral', 'control')                          |            0     |            0     |        3 |        3 |                   0     |
| ('claude-haiku-5-5', 'sadness_mid_desc', 'Sadness', 'emotion_description')             |            1     |            0.667 |        3 |        3 |                  33.333 |
| ('claude-haiku-5-5', 'sadness_mid_name', 'Sadness', 'character_name')                  |            0.333 |            0     |        3 |        3 |                  33.333 |
| ('gpt-5.6-luna', 'embarrassment_mid_desc', 'Embarrassment', 'emotion_description')     |            1     |            0.667 |        3 |        3 |                  33.333 |
| ('gpt-5.6-luna', 'embarrassment_mid_name', 'Embarrassment', 'character_name')          |            0.333 |            1     |        3 |        3 |                 -66.667 |
| ('gpt-5.6-luna', 'fear_mid_desc', 'Fear', 'emotion_description')                       |            0.667 |            1     |        3 |        3 |                 -33.333 |
| ('gpt-5.6-luna', 'fear_mid_name', 'Fear', 'character_name')                            |            0.667 |            0.667 |        3 |        3 |                   0     |
| ('gpt-5.6-luna', 'joy_mid_desc', 'Joy', 'emotion_description')                         |            0     |            0.667 |        3 |        3 |                 -66.667 |
| ('gpt-5.6-luna', 'joy_mid_name', 'Joy', 'character_name')                              |            0.333 |            1     |        3 |        3 |                 -66.667 |
| ('gpt-5.6-luna', 'neutral_generic', 'Neutral', 'control')                              |            0.667 |            0.333 |        3 |        3 |                  33.333 |
| ('gpt-5.6-luna', 'sadness_mid_desc', 'Sadness', 'emotion_description')                 |            1     |            1     |        3 |        3 |                   0     |
| ('gpt-5.6-luna', 'sadness_mid_name', 'Sadness', 'character_name')                      |            0.333 |            0.667 |        3 |        3 |                 -33.333 |

## 5. Cost (actual) and projection to the full design

| model_id         |   observations |   total_cost_usd |   cost_per_obs_usd |   share_cached |   mean_decision_input_tokens |   mean_decision_output_tokens |   mean_sell_rating_input_tokens |   mean_sell_rating_output_tokens |   proj_mvp_2000_usd |   proj_arms_repeats_12000_usd |   proj_full_36000_usd |
|:-----------------|---------------:|-----------------:|-------------------:|---------------:|-----------------------------:|------------------------------:|--------------------------------:|---------------------------------:|--------------------:|------------------------------:|----------------------:|
| claude-haiku-5-5 |             54 |         0.018774 |        0.000347659 |              0 |                        341.8 |                         317.7 |                           357.8 |                            237.7 |                0.35 |                          2.09 |                  6.26 |
| gpt-5.6-luna     |             54 |         0.012144 |        0.000224889 |              0 |                        242.9 |                          14.5 |                           251.9 |                              5.8 |                0.22 |                          1.35 |                  4.05 |

Synthetic runs have $0 spend and no cost extrapolation. Real-run projections use fully uncached observations only. Missing cost metadata remains unknown; provider/Expected Parrot billing must be reconciled separately.

## 6. Hand-check pair (verify against *_prompts.csv and the raw results)

| persona_id             | scenario_id   | version   | model_id         | decision_raw      |   sell |   sell_rating_raw |   sell_rating |   obs_cost_usd |
|:-----------------------|:--------------|:----------|:-----------------|:------------------|-------:|------------------:|--------------:|---------------:|
| embarrassment_mid_desc | s01           | gain      | claude-haiku-5-5 | Sell the position |      1 |                 3 |             3 |       0.000452 |
| embarrassment_mid_desc | s01           | loss      | claude-haiku-5-5 | Hold the position |      0 |                 2 |             2 |       0.000328 |
