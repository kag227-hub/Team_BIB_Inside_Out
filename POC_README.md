# Proof of concept: Checkpoint 1

Selected models: **GPT-5.6 Luna** and **Claude Haiku 5.5**. See [MODEL_SELECTION.md](MODEL_SELECTION.md) for rationale, settings, sources, and estimates.

Run from the repository root with Python 3.13:

```bash
python -m pip install -r requirements.txt
python code/poc_run.py --plan
python code/poc_run.py --test --run-id poc_TEST_local_check
python code/poc_analyze.py outputs/poc_TEST_local_check_responses.csv
```

The free test returns fixed synthetic hold/4 answers to validate the pipeline. It is not behavioral evidence. Use a new run ID for each execution; existing artifacts cannot be overwritten.

## Paid-run procedure

Set `EXPECTED_PARROT_API_KEY` in the runner's local environment or ignored `.env`. Never paste a key into chat or commit it.

Check account availability first:

```bash
python -c "from edsl import Model; print(Model.available(service_name='openai', search_term='gpt-5.6-luna', force_refresh=True)); print(Model.available(service_name='anthropic', search_term='claude-haiku-5-5', force_refresh=True))"
python code/poc_run.py --run-id poc_paid_001
python code/poc_analyze.py outputs/poc_paid_001_responses.csv
```

The runner prints its planning estimate and EDSL's account-based estimate before asking whether to proceed. It stops if credentials or the EDSL estimate are unavailable. Review the estimate against the team's budget before answering yes. `--yes` is available for an intentionally unattended run; it still requires a successful estimate. An estimate is not a provider-enforced spending cap.

Inspect at least ten comments per model for refusals, character breaks, and textbook recitation. Check truncation, saved prompts, and one independently calculated pair. Reconcile usage with account billing. Regex flags alone cannot replace human review.

Add raw EDSL results, raw CSV, prompts, tidy responses, manifest, saved estimate, and generated reports to the PR after checking for credentials. Update **STATUS_checkpoint1.md** with measured model IDs, validity, completeness, failures, costs, and hand-check findings. Keep the PR a draft until paid-run evidence is present.

The pilot uses nine personas (four emotions × two arms + neutral), three scenarios, two gain/loss versions, and two models: 108 observations and 54 pairs. Seed 331 randomizes option order across scenarios, preserving order within each pair. Fresh in-memory caching and disabled remote caching prevent prior-run reuse. Manifests record input hashes and effective model settings.

| File | Purpose |
|---|---|
| `inputs/personas_poc.csv` | Persona texts |
| `inputs/scenarios_poc.csv` | Fictional company/scenario facts |
| `inputs/models_poc.csv` | Selected settings and price provenance |
| `code/poc_run.py` | Collection and raw/tidy artifacts |
| `code/poc_analyze.py` | Validity, pairing, rates, cost projections, hand check |
| `STATUS_checkpoint1.md` | Executed evidence and outstanding work |
| `specs_tried.md` | Specifications, failures, and deviations |
