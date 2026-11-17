# Disposition effect by persona and model: poc_TEST_ablation_v0

**SYNTHETIC DRY RUN: fixed hold/4 answers. Zeros are expected; not behavioral evidence.**

Disposition effect = gain sell rate - loss sell rate, in percentage points. Complete matched pairs only; at most 3 pairs per cell, so these are exploratory.

| model_id   | emotion       | prompt_arm          | persona_id             |   n_gain |   n_loss |   gain_sell_rate |   loss_sell_rate |   disposition_effect_pp |
|:-----------|:--------------|:--------------------|:-----------------------|---------:|---------:|-----------------:|-----------------:|------------------------:|
| test       | Embarrassment | emotion_description | embarrassment_mid_desc |        3 |        3 |                0 |                0 |                       0 |
| test       | Neutral       | control             | neutral_generic        |        3 |        3 |                0 |                0 |                       0 |
