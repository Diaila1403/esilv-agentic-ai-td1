# TD 2, Step 3: the routing rule (Pair C)

Section of `reports/td2.md` written by Pair C, sub-group DIA5-G3, pack `2026-11-18-students-5`. To be merged into `reports/td2.md` at the cross-review (16:45 to 17:15).

**Nature of the evidence.** The rates are computed from the 104 **real** calls of `traces-td1.csv` (21 October 2026): no new network call in TD 2. The simulator outputs are **simulation**: the resources are our portfolio routes, but their availability (quota exhausted, refill time) is an assumption written in `routing/routing-config.json`. The quorum counts below are a cross-check computed by Pair C; the official vote is Pair A's `vote_k_sur_n`, and both must agree.

## 1. What Pair C did

| Deliverable | File |
|---|---|
| Exact TD 1 rate per family, computed by code from the traces | `routing/td1_families.py`, output `routing/family-rates-td1.csv` |
| The one-page routing rule | [`routing/routing-rule-en.md`](../routing/routing-rule-en.md) |
| Families, uses, checks, panels, resources and scenarios, read by the code (no model in the code) | `routing/routing-config.json` |
| Kit simulator, unchanged (SHA-256 `2971555aff39dede9e1a315ebb00d92d7b5c5f2eaf158199730fcc2c1839e28d`) | `routing/atelier-routage-kit.py`, output `routing/outputs/simulator-before.jsonl` |
| Simulator adapted to our rule (`RESOURCES` and `choose`) | `routing/atelier-routage.py`, output `routing/outputs/simulator-after.jsonl` |
| The priority between included capacity and deferral, executed | `routing/priority_demo.py`, output `routing/outputs/priority-demo.jsonl` |

Replay from the repository root (Python 3 standard library only, no key):

```bash
python3 routing/td1_families.py --csv routing/family-rates-td1.csv   # rates per family
python3 routing/atelier-routage-kit.py                                # kit, before adaptation
python3 routing/atelier-routage.py                                    # our rule, after adaptation
python3 routing/atelier-routage.py --scenario deferrable              # one scenario
python3 routing/priority_demo.py                                      # priority analysis
```

## 2. Exact TD 1 rate per family

Families follow the question types of `questions-td1.json`. C03, C13 and C14 also carry a period window but are typed "product list" by the kit; the eight families cover C01 to C20 exactly once (checked by the script). Rate = correct / cases on the **last attempt** of each cell; a wrong value (`incorrect`) and an availability failure (HTTP 401 `access_error`, HTTP 429 `not_executed`) are both "not correct", but only a wrong value lowers the eligibility level.

| Family | Level | Cells | gpt-oss-120b | gpt-oss-20b | qwen3.8-27b | north-mini-code:free | dots-3-note-preview:free |
|---|---:|---|---|---|---|---|---|
| F1 period | 1 | C01, C04, C05, C06, C07, C20 | 6/6 | 6/6 | 5/6 (C20 HTTP 429) | 5/6 (C01 HTTP 401) | 6/6 |
| F3 product list | 1 | C03, C12, C13, C14 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| F2b age at the time of the order | 2 | C10 | 1/1 | 1/1 | 1/1 | 0/1 (wrong C10=119410) | 0/1 (wrong C10=119410) |
| F1+F2b period + age at the order | 2 | C18 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 (wrong C18=39580) |
| F2 completed age on a reference date | 3 | C02, C08, C09, C11 | 4/4 | 2/4 (wrong C02=0, C11=322160) | 3/4 (wrong C09=0) | 1/4 (wrong C08=0, C09=0; C02 HTTP 401) | 1/4 (wrong C02=135000, C08=0, C09=47900) |
| F1+F2 | 3 | C15 | 1/1 | 1/1 | 0/1 (wrong C15=0) | 1/1 | 1/1 |
| F2+F3 | 3 | C16 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 (wrong C16=211260) |
| F1+F2+F3 | 3 | C17, C19 | 2/2 | 2/2 | 0/2 (wrong C19=83580; C17 HTTP 429) | 1/2 (wrong C17=371990) | 1/2 (wrong C17=152730) |
| **All** | | C01 to C20 | **20/20** | **18/20** | **15/20** | **14/20** | **13/20** |

The totals match `five-model-summary-en.csv` and the TD 1 report. Every one of the 16 wrong values is on a family with an age condition; no model returned a wrong value on F1 or F3.

**Eligibility level derived from TD 1** (highest level L with no wrong value on the families of level at most L; used as `level` in the simulator, computed, not typed):

| Model | Level | Wrong cells that cap the level |
|---|---:|---|
| gpt-oss-120b | 3 | none: 20/20 |
| gpt-oss-20b | 2 | C02=0, C11=322160 |
| qwen3.8-27b | 2 | C09=0, C15=0, C19=83580 |
| north-mini-code:free | 1 | C10=119410 |
| dots-3-note-preview:free | 1 | C10=119410, C18=39580 |

**What a quorum would have decided on each family** (cross-check, last attempt, an unavailable member stays in n):

| Family | fixed 2-of-3 (120b, cohere, qwen) | P1 2-of-3 (dots, 20b, qwen) | 3-of-5 (all five) |
|---|---|---|---|
| F1 | 6 correct | 6 correct | 6 correct |
| F3 | 4 correct | 4 correct | 4 correct |
| F2b, F1+F2b | 2 correct | 2 correct | 2 correct |
| F2 | 3 correct, **1 wrong consensus (C09: 0 with 2 votes)** | 2 correct, 2 abstain | 2 correct, 2 abstain (C02, C09) |
| F1+F2, F2+F3 | 2 correct | 2 correct | 2 correct |
| F1+F2+F3 | 1 correct, 1 abstain (C17) | 1 correct, 1 abstain | 1 correct, 1 abstain |

This table drives the choice of the check. On F1 and F3 a 2-of-3 quorum of free models has decided every cell correctly, even with one member down (C01 cohere HTTP 401, C20 qwen HTTP 429): it is an adequate check for a customer figure. On F2 the same kind of quorum either keeps a shared wrong value (C09, cohere and qwen both return 0 against the reference 487980) or abstains: a quorum of free models cannot see the cause, which is the completed-age convention. For F2 and its combinations the rule therefore requires the **reference** check (the validated query of the family), not a quorum.

## 3. The rule in one paragraph

The full one-page rule, with the cells of each line, is [`routing/routing-rule-en.md`](../routing/routing-rule-en.md). The family gives the level; the first route is the cheapest eligible route; every TD 1 route costs 0 USD, so ties go to the best TD 1 rate on the family, then to the **lowest** level. As a result, dots-3 (level 1, 6/6 and 4/4) answers F1 and F3 first, gpt-oss-20b (level 2, C10 and C18 correct) answers F2b first, and gpt-oss-120b (the only level-3 route) is kept for F2 and the combinations with F2. The check depends on the use: `none` only for an internal dashboard on a route at 100 % on the family; 2-of-3 for a customer on F1 and F3; reference for a customer on the age families; 3-of-5 then reference (F1, F3) or reference then human review (age families) for a payout. When the first route is unavailable: the next eligible route, then deferral if the request can wait and a refill is announced before the deadline, then the paid route gpt-oss-120b#openrouter (0.0006 USD per question) within budget, then abstention, never a silent fallback to a lower level.

## 4. Simulator, before adaptation (kit, unchanged)

`python3 routing/atelier-routage-kit.py`, full output in `routing/outputs/simulator-before.jsonl`:

| Scenario | Request | Action | Resource | Cash USD | Check |
|---|---|---|---|---:|---|
| simple | difficulty 1, can_wait, deadline 120, budget 0.30 | run | small-free | 0 | read-only execution and value check |
| complex | difficulty 3 | run | senior-subscription | 0 | read-only execution and value check |
| deferrable | difficulty 3, subscription exhausted (refill 60) | defer, wake in 60 min | senior-subscription | 0 | read-only execution and value check |
| urgent | difficulty 3, cannot wait, deadline 5, subscription exhausted | run | senior-api | 0.30 | read-only execution and value check |
| budget exhausted | difficulty 3, cannot wait, budget 0, subscription exhausted | abstain | - | 0 | read-only execution and value check |
| high impact | difficulty 3, high_impact | run | senior-subscription | 0 | source verification and human review |
| unknown capability | difficulty 4 | abstain | - | 0 | read-only execution and value check |

Reading of each decision: *simple*, small-free and the subscription are both included (cash 0), `min` on `(allocation, level, id)` takes small-free (allocation 0). *complex*, small-free is filtered out by `level >= difficulty`; the subscription is the only included resource. *deferrable*, no included resource at level 3 (senior-api has cash 0.30), the subscription refills in 60 min <= 120 and the request can wait: defer. *urgent*, the request cannot wait, so the paid branch runs senior-api at 0.30 <= 0.30. *budget exhausted*, senior-api at 0.30 > 0: abstain. *high impact*, the same route as *complex*; only the check changes: the stakes choose the check, not the model. *unknown capability*, no resource has level 4. What the kit does not say: the reasons cite no evidence, the levels are typed by hand, and the abstain reason "no eligible resource within deadline and budget" is the same whether the cause is capability (*unknown capability*) or budget (*budget exhausted*).

## 5. Simulator, after adaptation (our rule)

`python3 routing/atelier-routage.py`, full output with the complete reason of each decision in `routing/outputs/simulator-after.jsonl`. The seven kit scenarios are kept with the same structure (F2 plays the role of difficulty 3, gpt-oss-120b#groq the role of the exhausted included resource); five scenarios are added to exercise the lines of our rule.

| Scenario | Request | Unavailable (refill, min) | Action | Resource | Cash USD | Check | TD 1 cells cited in the reason |
|---|---|---|---|---|---:|---|---|
| simple | F1 (level 1), dashboard | - | run | dots-3-note-preview:free#openrouter | 0 | none | C01, C04, C05, C06, C07, C20 |
| complex | F2 (level 3), dashboard | - | run | gpt-oss-120b#groq | 0 | none | C02, C08, C09, C11 |
| deferrable | F2, dashboard, can wait, deadline 120 | gpt-oss-120b#groq (60) | defer, wake in 60 min | gpt-oss-120b#groq | 0 | none | C02, C08, C09, C11 |
| urgent | F2, dashboard, cannot wait, deadline 5 | gpt-oss-120b#groq (60) | run | gpt-oss-120b#openrouter | 0.0006 | none | C02, C08, C09, C11 |
| budget exhausted | F2, dashboard, cannot wait, budget 0 | gpt-oss-120b#groq (60) | abstain | - | 0 | nothing delivered | C02, C08, C09, C11 |
| high impact | F2, payout | - | run | gpt-oss-120b#groq | 0 | reference, then human review before payment | C02, C08, C09, C11 |
| unknown capability | F4 (not in C01 to C20), dashboard | - | abstain | - | 0 | human review | none: no cell for F4 |
| first model unavailable *(added)* | F1, customer, cannot wait | dots-3 (no refill announced) | run | gpt-oss-20b#groq | 0 | 2-of-3 P1, dots stays in n = 3, 2 votes still needed | C01, C04, C05, C06, C07, C20 |
| product list for a customer *(added)* | F3, customer | - | run | dots-3-note-preview:free#openrouter | 0 | 2-of-3 P1 | C03, C12, C13, C14 |
| age at the order *(added)* | F2b (level 2), dashboard | - | run | gpt-oss-20b#groq | 0 | none | C10 |
| age at the order, two routes down *(added)* | F1+F2b, dashboard, cannot wait | gpt-oss-20b (1), qwen3.8-27b (1) | run | gpt-oss-120b#groq | 0 | none | C18 (and C10 for the exclusion of cohere) |
| combined age question for a customer *(added)* | F1+F2+F3 (level 3), customer | - | run | gpt-oss-120b#groq | 0 | reference; mismatch: abstain and log | C17, C19 (C02, C11, C17, C19 for the exclusions) |

Example of a complete reason (*budget exhausted*): "F2 completed age on a reference date, level 3, TD 1 cells C02, C08, C09, C11: no eligible resource within deadline and budget (gpt-oss-120b#groq unavailable; gpt-oss-120b#openrouter 0.0006 USD > budget 0); never fall back in silence to a lower level; excluded: dots-3-note-preview:free#openrouter level 1 (wrong C02=135000, C08=0, C09=47900); north-mini-code:free#openrouter level 1 (wrong C08=0, C09=0); gpt-oss-20b#groq level 2 (wrong C02=0, C11=322160); qwen3.8-27b#groq level 2 (wrong C09=0)".

**What changed between before and after.** The branch order of `choose` is the kit's (included, defer, paid, abstain), so *deferrable*, *urgent* and *budget exhausted* take the same branch as in the kit. What changes: (1) the levels come from TD 1, so the simple question goes to the lowest eligible free route (dots-3) and not to a generic small-free; (2) inside a branch, ties are broken by the TD 1 rate on the family before the level, which matters for the fallback (*first model unavailable* goes to gpt-oss-20b at 6/6, not to cohere at 5/6); (3) the check is a function of the use and of the TD 1 rate of the route that answers, and it follows the request to the fallback route; (4) the paid route costs 0.0006 USD (same model as the level-3 free route) instead of 0.30; (5) *unknown capability* now abstains for the right reason, an absent family, and asks for a shadow test.

## 6. Why the supplied `choose` prefers an available subscription to a deferral, and when to reverse it

**Exact reading of the branches.** `choose` tests four branches in a fixed order and returns in the first non-empty one:

1. `included = [r for r in eligible if r["available"] and r["cash"] == 0]`: run the `min` on `(allocation, level, id)`;
2. `waiting`: eligible, **not** available, `cash == 0`, `0 < reset_minutes <= deadline_minutes`, used only if `request["can_wait"]`: defer;
3. `paid`: eligible, available, `cash <= budget`: run the cheapest;
4. otherwise abstain.

A subscription has `cash == 0`, so it belongs to `included` whatever its `allocation`: allocation is not a filter, only the first sort key inside branch 1 (when both are available, the free route wins because its allocation is 0). When the free resource is exhausted and the subscription is available, branch 1 is not empty and returns `run` on the subscription: branch 2 is never evaluated, even when the free resource refills well before the deadline. Executed with the kit code (`routing/outputs/priority-demo.jsonl`, line 1): small-free exhausted with a refill in 30 min, request that can wait 120 min, result `run senior-subscription`, cash 0.

**Why this order makes sense.**

- **No new spending either way.** The subscription fee is already paid; `allocation` is an accounting share of a fixed fee, not cash. Running now and deferring both cost 0 cash, and running now delivers 30 to 60 minutes earlier.
- **A refill time is a promise, not a fact** (Lecture 2). At wake-up the free route may still refuse: in TD 1 qwen3.8-27b received HTTP 429 on both attempts of C17 and C20, the retry budget ran out and the cells stayed `not_executed`. A deferral adds a queue, a second measurement and a second chance of failure; available capacity removes them.
- **Unused included quota is lost** at the end of its window. As long as the quota is ample, consuming it on a deferrable request has no opportunity cost.

**When the priority should be reversed.** When that last point is false, that is when the included quota has an opportunity cost. Operational condition: the request can wait, a free resource that is eligible for the family (TD 1 evidence) refills before `deadline_minutes`, and the subscription quota left in its current window is **not larger than the reserve** needed by the requests that cannot wait (urgent, high-stakes, or level-3 requests that only this resource serves) until the subscription's own reset. Spending the quota now would then push a later urgent request to the paid route (cash > 0) or to abstention: the deferrable request should wait for the free resource and the quota should be kept. The same holds when the subscription has a fair-use cap beyond which use is billed or throttled, since its allocation then turns into real cash. The free route's refill must be a measured pattern, not only an announced time, because a failed wake-up would delay the request twice. Executed in `routing/priority_demo.py` (`choose_with_reserve`, which delegates to the kit `choose` otherwise): 5 requests left against a reserve of 8 gives `defer small-free, wake in 30 min`; 40 left gives `run senior-subscription`, as in the kit.

**Link with our rule.** Our six resources contain no subscription. The scarce capacity in our portfolio is the free quota of gpt-oss-120b#groq, the only level-3 route, and the same reasoning applies to it: among equally accurate free routes our `rank` takes the lowest level first, so F1 and F3 go to dots-3 and F2b to gpt-oss-20b, and the gpt-oss-120b quota stays available for F2 and its combinations, which no other free route can answer.

## 7. Limits and hypotheses

- Twenty questions support a batch-specific hypothesis, not a general error rate, a permanent ranking or a quorum error guarantee. F2b, F1+F2b, F1+F2 and F2+F3 rest on **one cell each**; F1+F2+F3 on two.
- One run per cell at temperature 0: no measure of run-to-run variability. A model version can change without notice.
- The level is "no wrong value on the families up to L": a single wrong value in a later batch would lower it. The rule must be recomputed (`td1_families.py`) on every new batch.
- gpt-oss-120b and gpt-oss-20b belong to the same family: in the 3-of-5 quorum their errors may be correlated.
- gpt-oss-120b#openrouter inherits the TD 1 evidence of the same model on Groq (portfolio: capability does not change with the route), but this route made no call in TD 1; it should be checked on our questions before carrying a customer figure without the reference check.
- dots-3-note-preview is a preview free route absent from the portfolio: it can disappear, and its mean latency in TD 1 was 2.8 s against 0.7 s for gpt-oss-20b. For an interactive use, the rule could put gpt-oss-20b first on F1 and F3 at the price of its quota.
- Availability states, refill times and the subscription quota figures of the demo are assumptions (simulation). The 2,000 / 500 token envelope over-estimates the measured TD 1 means (560 to 641 tokens in, 135 to 279 out).
- The reference check assumes that the question matches a validated family template; a question outside the eight families has no reference and no TD 1 evidence (*unknown capability*).

## 8. Contribution and AI assistance

- Pair C, Step 3: Jean VASSEUR, *[partner of Pair C to add]*.
- AI assistance (Claude Code) was used to write the scripts, compute the tables and draft this section from the traces, the assignment and Lecture 2. Prompt as used, 18 November 2026: "Ensuite il faut faire le td2 ici : https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/index.html, moi je suis chargé de la partie STEP3 (pair C), fais la pour moi." Pair C has re-run every command above and remains responsible for every line.
