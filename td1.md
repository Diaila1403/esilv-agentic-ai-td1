# TD1 — Trustworthy Generative AI: Text-to-SQL Evaluation

**Course:** Next Generation AI 
**Session:** 21 October 2026  
**Group:** DIA5-G3  
**Repository:** https://github.com/Diaila1403/esilv-agentic-ai-td1  
**Members:** Diaila DIALLO, Meriam BOUMEDIENE, Lina ZAAQ, Imane BOUNA MOCTAR, Arthur GAUCHÉ, Jean VASSEUR, Simeon SIMEONOV

## 1. Objective and methodology

We evaluated five language models on 20 natural-language questions about revenue in a SQLite retail database (`data/boutique.sqlite`). The goal was to test whether models could generate executable SQL that returns the correct revenue in euro cents, and to compare accuracy, failures, reliability and response time.

We first prepared and checked the reference answers independently using SQL against the database. We then ran the provided multi-LLM skeleton against the five assigned models, retained the raw traces, and compared the returned values with the references. A correct verdict means that the executed query produced the expected numerical result; it does not by itself prove that every aspect of the SQL is semantically equivalent to the reference query.

The analysis below uses the consolidated real-call trace file. Replayed or synthetic examples are **not** counted as real model calls.

## 2. Models and results

| Model | Provider | Correct / 20 questions | Accuracy | Main observation |
|---|---|---:|---:|---|
| A — `openai/gpt-oss-120b` | Groq | 20/20 | **100%** | All 20 questions answered correctly |
| B — `openai/gpt-oss-20b` | Groq | 18/20 | **90%** | Two mistakes involving age/date conditions |
| C — `cohere/north-mini-code:free` | OpenRouter | 14/20 | **70%** | Four incorrect results and two access errors |
| D — `qwen/qwen3.8-27b` | Groq | 15/20 | **75%** | Three incorrect results and two questions without an executed successful result; rate limits caused extra attempts |
| E — `dots-studio/dots-3-note-preview:free` | OpenRouter | 13/20 | **65%** | Seven incorrect numerical results |

Accuracy is computed using the **20 distinct questions per model**, rather than dividing by the number of API attempts. Access failures and unanswered questions are counted as unsuccessful questions. Model D has 24 recorded real calls for 20 distinct questions because some calls were retried; these extra attempts must remain visible in the evidence but must not inflate the question count.

### Observed latency

The following values are descriptive averages over the recorded real-call rows with a numeric `latency_ms`, including unsuccessful attempts. They are **not** controlled performance benchmarks.

| Model | Mean recorded latency |
|---|---:|
| A | 970 ms |
| B | 702 ms |
| C | 2,807 ms |
| D | 650 ms |
| E | 2,849 ms |

Latency may vary with network conditions, service load, rate limiting, and the mix of successful and failed calls. In particular, model D's average includes short failed requests, so it should not be interpreted as the fastest successful SQL generator without further analysis.

## 3. Errors and possible causes

**Model A:** No incorrect answers were observed in this 20-question test set. This is evidence of strong performance on these questions, not a guarantee of correctness on other datasets or prompts.

**Model B:** Questions **C02** and **C11** returned incorrect values. Examination of the generated SQL indicates mistakes in the birth-date boundaries used to select customers of a given age. This illustrates how a query can be syntactically valid yet implement the wrong date logic.

**Model C:** Questions **C01** and **C02** failed because the API returned `HTTP 401: User not found`; these are access problems, not demonstrated SQL reasoning failures. Questions **C08, C09, C10, and C17** produced incorrect values. Their precise SQL-level causes should be confirmed by inspecting each recorded query against the reference.

**Model D:** Questions **C09, C15, and C19** produced incorrect values. Questions **C17 and C20** did not obtain an executed answer in the recorded runs. Several calls returned `HTTP 429` rate-limit errors, including retries for C16, C17, C19 and C20. C16 was later answered correctly, and C19 later returned an incorrect value. This shows why preserving every attempt matters: API availability and answer quality are different failure categories.

**Model E:** Questions **C02, C08, C09, C10, C16, C17, and C18** produced incorrect numerical values. The exact causes should be established from the corresponding SQL traces, rather than assumed from the incorrect verdict alone.

**Cross-model observation:** Age-related and date-sensitive questions appear repeatedly among the failed cases. This suggests that date arithmetic and boundary conventions deserve particular attention in the next evaluation, but a more detailed query-by-query review is required before attributing every failure to that cause.

## 4. Reliability, limitations and model choice

For this specific test set, model A achieved the best accuracy (20/20), followed by model B (18/20). Model B may be a useful option when its speed or cost is preferable, but its mistakes on age-based filters would need validation before using its SQL without review. Models C and E were less accurate in this sample. Model D was affected by both incorrect outputs and API rate limiting.

The dataset includes only 20 questions, so these results cannot establish general model rankings. The models were accessed through different providers, and network/service conditions were not controlled. An incorrect numerical result may come from wrong SQL logic; an HTTP error is instead an access or availability failure. The reference comparison checks the returned amount, not the complete meaning of the generated SQL. Any deployment handling financial calculations should execute SQL in a restricted read-only environment and validate important answers against trusted calculations.

**Cost limitation:** The available consolidated trace does not contain populated `cost_native` values. We therefore do **not** claim a verified per-model cost ranking. A price-based recommendation requires documented provider prices and comparable token accounting. The free-tier labels for models C and E should not be treated as a complete cost analysis.

## 5. Evidence and reproducibility

- [Reference SQL and expected revenue values](../reference-td1.csv)
- [Consolidated real-call traces](../traces-td1.csv)
- [Model B CSV traces](../traces-B.csv)
- [Model B JSONL traces](../traces-B.jsonl)
- [Model-by-question comparison](../model-question-comparison-en.csv)
- [Five-model summary](../five-model-summary-en.csv)

The links above refer to the expected repository paths; confirm that each file exists at that path before submission. Preserve the original raw traces alongside the cleaned consolidated CSV. Do not include API keys or other secrets in the repository.

The consolidated file contains **104 real-call rows** for **100 distinct model/question combinations**; the four additional rows are retries for model D. Four duplicated CSV header rows were removed during consolidation without changing the recorded model results. An offline replay previously used to inspect model B's errors must be labeled as a **replay** and must not be added to the 104 real calls.

## 6. Team contributions

| Member | Contribution |
|---|---|
| Lina ZAAQ | Model A calls and trace verification |
| Diaila DIALLO | Model B calls, trace verification and review of C02/C11 |
| Meriam BOUMEDIENE | Model C calls and trace verification |
| Simeon SIMEONOV | Model D calls, retries and rate-limit investigation |
| Arthur GAUCHÉ | Model E calls and trace verification |
| Imane BOUNA MOCTAR | Independent verification of reference values using SQL queries executed against the SQLite database |
| Jean VASSEUR | Independent verification of reference values using SQL queries executed against the SQLite database |

The team checked the reference calculations against the actual database before comparing model outputs.

## 7. Next steps

1. Inspect each incorrect SQL query and record one evidence-based cause per failure in the model-question comparison table.
2. Complete the official model-question comparison and five-model summary CSV templates, including any verified token/cost data and the distinction between incorrect SQL and API errors.
3. Confirm that all reference answers and all five sets of raw traces are in the public GitHub repository.
4. Use the TD1 findings to prepare TD2, especially model voting, routing decisions, and handling incorrect SQL or API failures.
5. Review this report collectively, commit the final evidence and submit the repository URL, full commit hash and report-at-commit link on Moodle by **25 October 2026, 23:59 Paris time**.

## 8. AI assistance disclosure

AI assistance was used to help structure and draft this Markdown report from the group's recorded traces and assignment instructions. The group is responsible for verifying every result, interpretation, contribution and repository link before submission.
