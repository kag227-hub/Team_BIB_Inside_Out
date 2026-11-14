# Disposition effect by persona and model: poc_TEST_v0

**SYNTHETIC DRY RUN: fixed hold/4 answers. Zeros are expected; not behavioral evidence.**

Disposition effect = gain sell rate - loss sell rate, in percentage points. Complete matched pairs only; at most 3 pairs per cell, so these are exploratory.

| model_id   | emotion       | prompt_arm          | persona_id             |   n_gain |   n_loss |   gain_sell_rate |   loss_sell_rate |   disposition_effect_pp |
|:-----------|:--------------|:--------------------|:-----------------------|---------:|---------:|-----------------:|-----------------:|------------------------:|
| test       | Embarrassment | character_name      | embarrassment_mid_name |        3 |        3 |                0 |                0 |                       0 |
| test       | Embarrassment | emotion_description | embarrassment_mid_desc |        3 |        3 |                0 |                0 |                       0 |
| test       | Fear          | character_name      | fear_mid_name          |        3 |        3 |                0 |                0 |                       0 |
| test       | Fear          | emotion_description | fear_mid_desc          |        3 |        3 |                0 |                0 |                       0 |
| test       | Joy           | character_name      | joy_mid_name           |        3 |        3 |                0 |                0 |                       0 |
| test       | Joy           | emotion_description | joy_mid_desc           |        3 |        3 |                0 |                0 |                       0 |
| test       | Neutral       | control             | neutral_generic        |        3 |        3 |                0 |                0 |                       0 |
| test       | Sadness       | character_name      | sadness_mid_name       |        3 |        3 |                0 |                0 |                       0 |
| test       | Sadness       | emotion_description | sadness_mid_desc       |        3 |        3 |                0 |                0 |                       0 |
