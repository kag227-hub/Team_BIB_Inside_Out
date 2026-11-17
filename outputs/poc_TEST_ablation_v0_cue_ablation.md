# Demand-cue ablation: poc_TEST_ablation_v0

**SYNTHETIC DRY RUN: fixed hold/4 answers. Zeros are expected; not behavioral evidence.**

Audit A3. DE = gain sell rate - loss sell rate (pp), complete matched pairs only. `remove_X` = DE without cue X minus DE with it, averaged over the other cue. 95% interval: percentile bootstrap over base scenarios (B = 10,000, seed 331). Exploratory (ANALYSIS_PLAN.md, S8); with few base scenarios the intervals are coarse.

| model_id   | persona_id                        | estimate           |   value_pp |   ci95_lo_pp |   ci95_hi_pp |   n_scenarios |   n_pairs |
|:-----------|:----------------------------------|:-------------------|-----------:|-------------:|-------------:|--------------:|----------:|
| test       | embarrassment_mid_desc            | DE_both_cues       |          0 |            0 |            0 |             3 |         3 |
| test       | embarrassment_mid_desc            | DE_no_past_moves   |          0 |            0 |            0 |             3 |         3 |
| test       | embarrassment_mid_desc            | DE_no_system_line  |          0 |            0 |            0 |             3 |         3 |
| test       | embarrassment_mid_desc            | DE_no_cues         |          0 |            0 |            0 |             3 |         3 |
| test       | embarrassment_mid_desc            | remove_past_moves  |          0 |            0 |            0 |             3 |        12 |
| test       | embarrassment_mid_desc            | remove_system_line |          0 |            0 |            0 |             3 |        12 |
| test       | embarrassment_mid_desc            | interaction        |          0 |            0 |            0 |             3 |        12 |
| test       | neutral_generic                   | DE_both_cues       |          0 |            0 |            0 |             3 |         3 |
| test       | neutral_generic                   | DE_no_past_moves   |          0 |            0 |            0 |             3 |         3 |
| test       | neutral_generic                   | DE_no_system_line  |          0 |            0 |            0 |             3 |         3 |
| test       | neutral_generic                   | DE_no_cues         |          0 |            0 |            0 |             3 |         3 |
| test       | neutral_generic                   | remove_past_moves  |          0 |            0 |            0 |             3 |        12 |
| test       | neutral_generic                   | remove_system_line |          0 |            0 |            0 |             3 |        12 |
| test       | neutral_generic                   | interaction        |          0 |            0 |            0 |             3 |        12 |
| test       | pooled (equal weight per persona) | DE_both_cues       |          0 |            0 |            0 |             3 |         6 |
| test       | pooled (equal weight per persona) | DE_no_past_moves   |          0 |            0 |            0 |             3 |         6 |
| test       | pooled (equal weight per persona) | DE_no_system_line  |          0 |            0 |            0 |             3 |         6 |
| test       | pooled (equal weight per persona) | DE_no_cues         |          0 |            0 |            0 |             3 |         6 |
| test       | pooled (equal weight per persona) | remove_past_moves  |          0 |            0 |            0 |             3 |        24 |
| test       | pooled (equal weight per persona) | remove_system_line |          0 |            0 |            0 |             3 |        24 |
| test       | pooled (equal weight per persona) | interaction        |          0 |            0 |            0 |             3 |        24 |
