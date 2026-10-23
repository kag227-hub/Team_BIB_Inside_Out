# STATUS — Checkpoint 1 (Oct 23, 2026)

**Team BIB · "Inside Out" Silicon Investors · Seed #13**

<!-- Fill in the [brackets] after running code/poc_run.py and code/poc_analyze.py. Keep it to ~3 paragraphs. -->

**What we picked and why.** We picked seed #13: do LLM investor personas show the disposition effect, selling winners more often than losers (Odean, 1998)? We build the personas from the *Inside Out* emotions (Joy, Sadness, Anger, Fear, Disgust, Anxiety, Envy, Embarrassment) crossed with three investor backgrounds, plus a neutral control. Each persona sees matched gain and loss versions of the same fictional stock, which differ only in the sign of the return. The emotions give us testable predictions before we run anything (Joy should lock in gains; Embarrassment should hold losers). We also compare naming the character with describing the emotion, which tests whether the model reacts to the movie cue or to the feeling.

**What the proof of concept got, and what broke.** `code/poc_run.py` ran [9] personas (4 emotions × 2 prompt arms, mid-career background, plus neutral) × 3 base scenarios (±5%, ±10%, ±20%) × gain/loss × 2 models ([model A], [model B]) = [108] survey observations, saved in `outputs/poc_2026-10-23_responses.csv`. A built-in assert confirms that every gain/loss prompt pair differs only in the sign of the return. Results: [X]% of decisions and [Y]% of ratings parsed as valid; [N] of [54] matched pairs were complete; [refusals / character breaks / comments that cite "loss aversion" or the disposition effect: describe]. Actual cost was $[total], or $[per obs] per observation, which projects to about $[MVP] for the 2,000-observation MVP and $[full] for the full 36,000 design (`outputs/*_cost_projection.csv`). What broke: [e.g., model B wrapped answers in extra text and failed parsing; caching made repeats free and identical; EDSL adds a "Do not break character" system line we did not write]. We are not reading anything into the sell rates yet: with 3 pairs per cell, they are noise.

**Questions for you.**
1. Budget: is $[amount] reasonable, and can we use [models], or do you want specific ones?
2. Repeats: with temperature [1.0] and caching off, is 3 repeats per cell enough, or should we spend on more personas/scenarios instead?
3. Benchmark: is comparing our gain-minus-loss sell rate with Odean's PGR − PLR (14.8% − 9.8% = 5.0 pp) acceptable as an analogue, given that his rates come from realization opportunities in brokerage accounts?
4. Leakage: since we can't test "after the cutoff" here, is a rational-economist control plus the comment-recitation check enough to address "the model is reciting the textbook"?
