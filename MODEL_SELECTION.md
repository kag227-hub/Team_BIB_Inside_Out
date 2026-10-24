# Pilot model selection

Selected October 24, 2026, before observing any paid responses.

| Model ID | Provider | Input / output USD per million tokens | Pilot settings |
|---|---|---|---|
| `gpt-5.6-luna` | OpenAI | $0.20 / $1.20 | low reasoning effort; temperature 1; 2,048 maximum completion tokens |
| `claude-haiku-5-5` | Anthropic | $0.10 / $0.50 for short prompts | adaptive thinking; low effort; sampling parameters omitted by EDSL; 2,048 maximum output tokens |

We chose cost-sensitive text models from different providers to test the survey across model families without flagship-model prices. Selection is based on task fit and cost, not on answers supporting our hypotheses. Effort settings are not equivalent across providers: interpret findings as model-and-configuration comparisons.

Official sources checked October 23–24, 2026:

- [OpenAI GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [Anthropic Claude Haiku 5.5](https://platform.claude.com/docs/en/models/haiku-5-5/overview)
- [Anthropic model lifecycle](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [EDSL model discovery](https://docs.expectedparrot.com/en/latest/language_models.html)

The old Claude 3.5 Haiku placeholder is retired. GPT-4o mini and GPT-4.1 mini are marked deprecated in OpenAI documentation. Haiku 4.5 remains a legacy alternative, but was not selected or run.

Provider documentation does not establish availability or pricing through Expected Parrot. Confirm both exact IDs and the account-based job estimate before collecting responses. Stop and log a deviation if either is unavailable; do not silently substitute. The selected IDs are documented model identifiers, not independently verified immutable snapshots. Preserve raw responses, settings, run dates, and available version metadata.

## Planning estimate

The paid pilot has 54 observations per model and two questions per observation: **108 requests per model, 216 total**, before retries. Assuming **2,000 input and 500 billed output tokens per request**, with no discounts:

| Scope | OpenAI | Anthropic | Combined |
|---|---:|---:|---:|
| 108-observation pilot | $0.1080 | $0.0486 | $0.1566 |
| 2,000-observation MVP | $2.00 | $0.90 | $2.90 |
| 12,000 observations | $12.00 | $5.40 | $17.40 |
| 36,000 observations | $36.00 | $16.20 | $52.20 |

These are assumption-based estimates, not measured costs, invoices, or spending caps. Billed thinking tokens, retries, and service pricing can change the total. Output caps are 2,048 tokens per question; check truncation during the pilot. Re-estimate from uncached usage and reconcile account billing before scaling.
