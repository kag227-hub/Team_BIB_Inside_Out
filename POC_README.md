# Proof of concept (Checkpoint 1)

```bash
pip install -r requirements.txt
python code/poc_run.py --test        # free dry run with EDSL's fake "test" model: checks the plumbing
python code/poc_run.py               # real run with the models in inputs/models_poc.csv (prints a cost estimate first)
python code/poc_analyze.py outputs/poc_2026-10-23_responses.csv
```

Set `EXPECTED_PARROT_API_KEY` in your environment (or a git-ignored `.env`) before a real run. Edit `inputs/models_poc.csv` to the two models the team picks first.

| File | What it is |
|---|---|
| `inputs/personas_poc.csv` | 4 emotions × 2 prompt arms (mid-career) + neutral control = 9 personas |
| `inputs/scenarios_poc.csv` | 3 fictional companies at 5%, 10%, 20%; each becomes a gain and a loss version |
| `inputs/models_poc.csv` | The two models (placeholders until the team picks) |
| `code/poc_run.py` | Builds the design, asserts sign-only pairs, runs EDSL, saves raw + tidy rows |
| `code/poc_analyze.py` | Parse rates, pair completeness, flags, sell rates, cost projection, hand-check pair |
| `STATUS.md` | Checkpoint memo template: fill the brackets from the feasibility report |
