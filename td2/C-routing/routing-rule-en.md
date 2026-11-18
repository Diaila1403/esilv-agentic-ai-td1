# Routing rule, DIA5-G3 (TD 2, Step 3, Pair C)

Policy `dia5-g3-routing-v1`, 18 November 2026, written with the kit worksheet `templates/routing-rule-en.md`. Evidence: the last attempt of each cell of [`traces-td1.csv`](../../td1/traces-td1.csv) (real calls, 21 October 2026), recomputed by [`td1_families.py`](td1_families.py) into [`family-rates-td1.csv`](family-rates-td1.csv). Configuration read by the code: [`routing-config.json`](routing-config.json). Prices: [`five-model-summary-en.csv`](../../td1/five-model-summary-en.csv) and portfolio of 28 September 2026.

**Principle.** Difficulty chooses the model, stakes choose the check. The family gives a level (1, 2, 3) and only routes whose TD 1 level is at least that level are eligible; the first route is the cheapest eligible one. All five TD 1 routes cost 0 USD: the three Groq routes are free-plan rows of the portfolio (G5, 0 / 0 USD per million); north-mini-code:free and dots-3-note-preview:free are absent from it and documented in [`five-model-summary-en.csv`](../../td1/five-model-summary-en.csv) as OpenRouter free routes priced 0 (read 21 October 2026). Ties are broken by: TD 1 rate on the family, then the lowest level (keep the free quota of the strong model for the families only it solves), then availability failures in TD 1. A combination takes the level of its hardest component.

**Uses and cost of an error.** *Dashboard* (internal, corrected at the next refresh): low. *Customer* (figure shown outside, the company is bound by it): medium to high. *Payout* (money moves, hard to reverse): high. `none` is allowed only for a dashboard **and** when the route answering is at 100 % on the family in TD 1; otherwise the stricter check applies, on any fallback route (the check belongs to the request, not to the route). *Reference* = the validated query of the family (convention of `reference-td1.csv`) run read-only by the local route `script#script` (G5, 0 USD); value delivered only if equal.

| Family (level) | TD 1 cells and exact rate, correct / cases | First model (0 USD) | Check: dashboard / customer / payout | If the first model is unavailable |
|---|---|---|---|---|
| **F1** period (1) | C01, C04, C05, C06, C07, C20. 120b 6/6, 20b 6/6, dots 6/6, qwen 5/6 (C20 HTTP 429), cohere 5/6 (C01 HTTP 401). No wrong value. | `dots-3-note-preview:free` (6/6, level 1) | none (dots 6/6) / 2-of-3, panel P1 = dots + gpt-oss-20b + qwen (TD 1: 6/6 correct consensus, C20 still decided with qwen down) / 3-of-5 then reference | gpt-oss-20b#groq (6/6, other provider), then gpt-oss-120b#groq (6/6), then north-mini-code:free, then qwen (5/6: `none` refused, 2-of-3 P1) |
| **F3** product list (1) | C03, C12, C13, C14. All five models 4/4. | `dots-3-note-preview:free` (4/4, level 1) | none / 2-of-3 P1 (4/4 correct consensus) / 3-of-5 then reference | north-mini-code:free (4/4), then gpt-oss-20b, qwen, gpt-oss-120b (all 4/4) |
| **F2b** age at the order (2) | C10. 120b, 20b, qwen 1/1; cohere 0/1 and dots 0/1, **both 119410** (wrong agreement). | `gpt-oss-20b#groq` (1/1, level 2) | none (20b 1/1) / reference / reference then human review | qwen3.8-27b (1/1), then gpt-oss-120b (1/1); never cohere or dots (C10 = 119410) |
| **F1+F2b** (2) | C18. 120b, 20b, qwen, cohere 1/1; dots 0/1 (39580). | `gpt-oss-20b#groq` (1/1) | as F2b | as F2b |
| **F2** completed age on a reference date (3) | C02, C08, C09, C11. 120b 4/4; qwen 3/4 (C09=0); 20b 2/4 (C02=0, C11=322160); cohere 1/4 (C08=0, C09=0, C02 HTTP 401); dots 1/4 (C02=135000, C08=0, C09=47900). | `gpt-oss-120b#groq` (4/4, only level-3 route) | none (120b 4/4) / **reference, not a quorum**: on C09 the fixed 2-of-3 panel keeps the shared wrong 0 of cohere and qwen, 3-of-5 abstains on C02 and C09 / reference then human review | no other eligible free route. Defer if the request can wait and the Groq refill comes before the deadline (recheck at wake-up); else `gpt-oss-120b#openrouter`, same model, 0.0006 USD within budget; else abstain. Never fall back to 20b, qwen, cohere or dots |
| **F1+F2** (3) | C15. 120b, 20b, cohere, dots 1/1; qwen 0/1 (C15=0). | `gpt-oss-120b#groq` | as F2 | as F2 |
| **F2+F3** (3) | C16. 120b, 20b, cohere, qwen 1/1; dots 0/1 (211260). | `gpt-oss-120b#groq` | as F2 | as F2 |
| **F1+F2+F3** (3) | C17, C19. 120b 2/2, 20b 2/2; cohere 1/2 (C17=371990), dots 1/2 (C17=152730); qwen 0/2 (C19=83580, C17 HTTP 429 twice). Fixed 2-of-3 abstains on C17. | `gpt-oss-120b#groq` | as F2 | as F2 |

Eligibility levels derived from TD 1 (highest level with no wrong value): gpt-oss-120b **3** (20/20); gpt-oss-20b **2** (capped by C02, C11); qwen3.8-27b **2** (capped by C09, C15, C19); north-mini-code:free **1** (capped by C10); dots-3-note-preview:free **1** (capped by C10, C18). gpt-oss-20b is right on C15 to C19 but wrong on their F2 component (C02, C11), so it is not eligible for combinations with F2.

**Unavailability, every family.** One retry at most per call, `Retry-After` at most 60 s (kit limits). HTTP 401 (account, as cohere on C01, C02): next model at once, a retry is useless. HTTP 429 (quota, as qwen on C16, C17, C19, C20): next eligible model. No eligible route left: **defer** if the request can wait and a refill is announced before the deadline, and measure availability again at wake-up; otherwise the **paid** route within budget; otherwise **abstain** and say why. A check in error means no delivery. Delay and cost basis: the only paid route, gpt-oss-120b#openrouter, costs 0.0006 USD per question (2,000 tokens in at 0.15, 500 out at 0.6 USD per million).

**Scenario outcomes** (`python3 td2/C-routing/atelier-routage.py`, simulation):

| ID | Situation | Selected action | Reason tied to the rule | Evidence or explicit assumption |
|---|---|---|---|---|
| R1 | Ordinary F1 question, dashboard, all routes up | run dots-3, check none | level 1, 6/6 on F1 | C01, C04, C05, C06, C07, C20 |
| R2 | F1 for a customer, dots-3 down, no refill announced | run gpt-oss-20b, 2-of-3 P1 with dots kept in n | next eligible route at 100 % | 20b 6/6 on F1; assumption: 401 as cohere C01 |
| R3 | F2 deferrable, gpt-oss-120b#groq exhausted, refill 60 min | defer 60 min, recheck | only level-3 free route | C02, C08, C09, C11; assumption: 429 |
| R4 | F2 urgent, budget 0 | abstain | paid route 0.0006 USD > 0; no silent fallback | 20b wrong C02, C11; qwen wrong C09 |
| R5 | F2 payout, models agree | run gpt-oss-120b, reference then human review | an agreement can be wrong | C09: cohere = qwen = 0, reference 487980 |

Limits: twenty questions give a batch-specific hypothesis, not a general error rate, a permanent ranking or a quorum guarantee. F2b, F1+F2b, F1+F2 and F2+F3 rest on one cell each. One run at temperature 0. gpt-oss-120b and gpt-oss-20b share a family. The paid route made no call in TD 1.
