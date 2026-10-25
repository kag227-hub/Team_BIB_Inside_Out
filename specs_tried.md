# Specifications tried

Append every attempted specification, pilot, failure, and deviation, including null results.

| ID | Date | Attempt | Outcome |
|---|---|---|---|
| POC-000 | 2026-10-24 | Original test-model survey, nine personas, three scenarios, fixed sell-first order | 54 synthetic rows; “Hello, world X” invalid answers; 0% valid decisions/ratings; 0/27 complete pairs. No behavioral inference. |
| POC-001 | 2026-10-24 | Fixed synthetic hold/4 answers; option seed 331; fresh memory cache; remote cache off; protected run prefixes; complete-pair analysis | 54 synthetic rows; 100% valid decisions/ratings; 27/27 pairs; $0 paid spending. Zero sell gaps are expected test fixtures. |
| CONFIG-001 | 2026-10-24 | GPT-5.6 Luna and Claude Haiku 5.5; low effort; 2,048 output-token caps | Selected before paid answers. Account availability/live behavior still to be verified. |
| PAID-000 | 2026-10-24 | Paid credential preflight | Stopped because EXPECTED_PARROT_API_KEY is absent from the process environment. No paid calls. Existing local setup being checked. |

The expanded eight-emotion, three-background, repeated/reworded experiment remains planned. Pilot emotional personas have only the mid-career background; the neutral control has a generic background. Model alternatives were researched, not run. These are engineering/pilot specifications, not the frozen main-study preregistration.

## Paid pilot execution

| ID | Date | Attempt | Outcome |
|---|---|---|---|
| PAID-001 | 2026-10-24 | Colab startup with execution log inside the protected output prefix | Guard stopped execution before requests; moved execution log outside outputs. No duplicate collection. |
| PAID-002 | 2026-10-24 (2026-10-25 UTC) | Run poc_paid_20261025T012651Z; selected models, 9 personas, 3 paired scenarios, low effort, seed 331 | 108 observations; 100% valid decisions/ratings; 54/54 pairs; zero exceptions/cache hits. Expected Parrot reports $0.0307; response metadata sums to $0.030918. Raw-artifact transfer and comment review pending. |
| ANALYSIS-001 | 2026-10-24 | Correct hand-check row selection to keep model/persona/scenario/repeat fixed | The original report selected two gain rows from different models. Fixed without changing behavioral estimates; regression suite now has four passing tests. |
