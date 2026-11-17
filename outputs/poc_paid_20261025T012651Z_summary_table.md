# Disposition effect by persona and model: poc_paid_20261025T012651Z

Disposition effect = gain sell rate - loss sell rate, in percentage points. Complete matched pairs only; at most 3 pairs per cell, so these are exploratory.

| model_id         | emotion       | prompt_arm          | persona_id             |   n_gain |   n_loss |   gain_sell_rate |   loss_sell_rate |   disposition_effect_pp |
|:-----------------|:--------------|:--------------------|:-----------------------|---------:|---------:|-----------------:|-----------------:|------------------------:|
| claude-haiku-5-5 | Embarrassment | character_name      | embarrassment_mid_name |        3 |        3 |            0.333 |            0.667 |                 -33.333 |
| claude-haiku-5-5 | Embarrassment | emotion_description | embarrassment_mid_desc |        3 |        3 |            0.667 |            0     |                  66.667 |
| claude-haiku-5-5 | Fear          | character_name      | fear_mid_name          |        3 |        3 |            1     |            1     |                   0     |
| claude-haiku-5-5 | Fear          | emotion_description | fear_mid_desc          |        3 |        3 |            1     |            1     |                   0     |
| claude-haiku-5-5 | Joy           | character_name      | joy_mid_name           |        3 |        3 |            0     |            0     |                   0     |
| claude-haiku-5-5 | Joy           | emotion_description | joy_mid_desc           |        3 |        3 |            0     |            0.333 |                 -33.333 |
| claude-haiku-5-5 | Neutral       | control             | neutral_generic        |        3 |        3 |            0     |            0     |                   0     |
| claude-haiku-5-5 | Sadness       | character_name      | sadness_mid_name       |        3 |        3 |            0.333 |            0     |                  33.333 |
| claude-haiku-5-5 | Sadness       | emotion_description | sadness_mid_desc       |        3 |        3 |            1     |            0.667 |                  33.333 |
| gpt-5.6-luna     | Embarrassment | character_name      | embarrassment_mid_name |        3 |        3 |            0.333 |            1     |                 -66.667 |
| gpt-5.6-luna     | Embarrassment | emotion_description | embarrassment_mid_desc |        3 |        3 |            1     |            0.667 |                  33.333 |
| gpt-5.6-luna     | Fear          | character_name      | fear_mid_name          |        3 |        3 |            0.667 |            0.667 |                   0     |
| gpt-5.6-luna     | Fear          | emotion_description | fear_mid_desc          |        3 |        3 |            0.667 |            1     |                 -33.333 |
| gpt-5.6-luna     | Joy           | character_name      | joy_mid_name           |        3 |        3 |            0.333 |            1     |                 -66.667 |
| gpt-5.6-luna     | Joy           | emotion_description | joy_mid_desc           |        3 |        3 |            0     |            0.667 |                 -66.667 |
| gpt-5.6-luna     | Neutral       | control             | neutral_generic        |        3 |        3 |            0.667 |            0.333 |                  33.333 |
| gpt-5.6-luna     | Sadness       | character_name      | sadness_mid_name       |        3 |        3 |            0.333 |            0.667 |                 -33.333 |
| gpt-5.6-luna     | Sadness       | emotion_description | sadness_mid_desc       |        3 |        3 |            1     |            1     |                   0     |
