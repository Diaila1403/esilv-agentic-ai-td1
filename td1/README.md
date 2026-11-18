# TD 1 21 October 2026 · Comparing models on the same questions

Sub-group **DIA5-G3** (DIA5) · assignment: [TD 1](https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/students/kit-td1/enonce-td1-en.html) · session report: [`reports/td1.md`](../reports/td1.md)

Five free models (gpt-oss-120b, gpt-oss-20b and qwen3.8-27b on Groq; north-mini-code:free and dots-3-note-preview:free on OpenRouter) answered the twenty text-to-SQL questions of the kit; each SQL query was run read-only on `data/boutique.sqlite` and compared with an independent reference.

## Files

| File | Content |
|---|---|
| [`reference-td1.csv`](reference-td1.csv) | C01 to C20: reference query and value in euro cents, computed on the database |
| [`traces-td1.csv`](traces-td1.csv) | consolidated trace: 104 real calls, one line per call, retries included (100 cells + 4 retries of qwen3.8-27b) |
| [`traces-A.csv`](traces-A.csv) to [`traces-E.csv`](traces-E.csv) | raw traces of each member, one model each (A gpt-oss-120b, B gpt-oss-20b, C north-mini-code:free, D qwen3.8-27b, E dots-3-note-preview:free) |
| [`traces-B.jsonl`](traces-B.jsonl), `state-A.jsonl`, `state-C.jsonl`, `state-D.jsonl`, `state-E.jsonl` | JSONL state files written by the skeleton during the calls |
| [`five-model-summary-en.csv`](five-model-summary-en.csv) | the five models: public index, prices, access route, results per question family |
| [`model-question-comparison-en.csv`](model-question-comparison-en.csv) | one row per model and question: status, value, reference, explanation |

## Results (from the report)

| Model | Correct / 20 |
|---|---:|
| gpt-oss-120b | 20 |
| gpt-oss-20b | 18 |
| qwen3.8-27b | 15 |
| north-mini-code:free | 14 |
| dots-3-note-preview:free | 13 |

These files moved from the repository root to `td1/` on 18 November 2026 to follow the `td1/ td2/ td3/ reports/` layout; their content is unchanged. The submitted TD 1 version is the commit recorded in Moodle.
