# Review of Pair C (Step 3, routing rule) by Pair A

**Reviewed:** the files of [`README.md`](README.md) in `td2/C-routing/` (folder last changed at commit `cca74d9`, 18 November 2026, 15:23) and Step 3 of [`reports/td2.md`](../../reports/td2.md#step-3--the-routing-rule-pair-c); `main` at `23d0b80` (16:11) when reviewed. Pair C: Jean VASSEUR, Lina ZAAG. **Reviewers:** Pair A (Diaila DIALLO, Meriam BOUMEDIENE). **Date:** 18 November 2026.

**Verdict:** the content meets the Q3 level 2 evidence. There is one line per family with the first model and the check, the TD 1 cells and rates are on every line, and the rule says what to do when the first model is unavailable. Every figure we recomputed, with our own code and with our `vote_k_sur_n`, matches. The blocking problem is not Pair C's doing: at `23d0b80` the replay crashes because `td1/traces-td1.csv` was edited at 16:09. Until `td1/` is restored, the repository does not show the work. We request six changes. The first is blocking; the other five are small.

## 1. What we re-ran

Python 3.13, no key, no network. Two commits: `23d0b80` (`main` when reviewed) and `00de7e3` (15:58, the last commit before the edits to `td1/`), checked out in a separate worktree.

| Check | Result |
|---|---|
| The five README commands at `23d0b80` | `td1_families.py`, `atelier-routage.py` and `atelier-routage.py --scenario deferrable` **crash** with `KeyError: 'provider'`. `atelier-routage-kit.py` and `priority_demo.py` run (they do not read the traces). |
| Cause | Commits `ad7d5ab` to `e7548b4` (16:04 to 16:09, account Diaila1403) add one blank line to 14 files of `td1/` and edit the title of `td1/README.md`. In `traces-td1.csv` it is line 1 (a lone `\r`), so `csv.DictReader` reads an empty header. SHA-256 of `traces-td1.csv`: `889c2dc1…7906d` at `00de7e3`, `cdae32aa…da121` at `23d0b80`. The same edit breaks Pair A's `atelier-vote.py --traces td1/traces-td1.csv --case C09` (`KeyError: 'case_id'`) and `comparaison-votes.py` (`KeyError: 'nature'`). |
| The five README commands at `00de7e3` | All exit 0. `family-rates-td1.csv`, `outputs/simulator-before.jsonl`, `outputs/simulator-after.jsonl` (12 lines) and `outputs/priority-demo.jsonl` are regenerated **byte-identical** (`cmp`). `--scenario deferrable` prints the `deferrable` line of `simulator-after.jsonl`. An unknown scenario name exits 2. |
| `sha256sum atelier-routage-kit.py` | `2971555a…9e28d`, as stated. |
| Our own recount (our script, last attempt in file order, not `td1_families.py`) | 104 rows, all `real`. Last attempts: 80 correct, 16 incorrect, 2 `access_error` (north-mini-code C01, C02, HTTP 401), 2 `not_executed` (qwen C17, C20, HTTP 429 on both attempts). All 40 family × model cells of `family-rates-td1.csv` are identical. Totals are 20, 18, 15, 14 and 13, and the 16 wrong values are all on age families. Pair C picks the last attempt by `(attempts, date_utc)` and we used file order: both give the same row for the four qwen retries (C16, C17, C19, C20). |
| Our `vote_k_sur_n` on Pair C's three panels, 20 questions | Same outcomes as Pair C's table "What a quorum would have decided". On F2, fixed 2-of-3 gives 3 correct and the wrong 0 on C09; P1 and 3-of-5 give 2 correct and abstain on C02 and C09. On F1+F2+F3, all three panels abstain on C17. Fixed 2-of-3 and 3-of-5 are identical to our `comparaison-votes.csv` on 20/20. |
| Fallback order in `choose` (dashboard, cannot wait; the chosen route removed one at a time) | F1: dots-3 > gpt-oss-20b > gpt-oss-120b#groq > north-mini-code > qwen > gpt-oss-120b#openrouter > abstain. F3: dots-3 > north-mini-code > gpt-oss-20b > qwen > gpt-oss-120b#groq > gpt-oss-120b#openrouter > abstain. F2b: gpt-oss-20b > qwen > gpt-oss-120b#groq > gpt-oss-120b#openrouter > abstain. This is the order in the last column of `routing-rule-en.md`. |
| F1 for a customer with dots-3 down (scenario *first model unavailable*), check replayed with our vote on the six F1 cells | P1 with dots-3 kept in n = 3 gives **5 correct, and abstains on C20** (qwen HTTP 429). The panel north-mini-code + gpt-oss-20b + qwen gives 6/6 on F1 and 4/4 on F3. |
| F1 dashboard with dots-3, gpt-oss-20b, gpt-oss-120b#groq and north-mini-code down | `choose` runs qwen with the check "2-of-3 quorum, panel P1-2of3 (…) k = 2 votes still needed among the others". Only qwen is left in P1, so **the check cannot pass**. |
| Wake-up with the route still exhausted (F2 dashboard, refill announced again in 60 min) | With 60 min left, `choose` **defers again**. With 59 min left, it runs gpt-oss-120b#openrouter. |
| Prices, envelope and measures cited | 0.15 / 0.6 USD per million in `five-model-summary-en.csv`; 2,000 × 0.15 + 500 × 0.6 per million = 0.0006 USD. Mean tokens are 560 to 641 in and 135 to 279 out; mean latency is 2.85 s for dots-3 and 0.70 s for gpt-oss-20b. All as written. |
| `routing-rule-en.md` printed (pandoc + wkhtmltopdf, A4, 11 pt text, 9 pt tables, 15 mm margins) | **2 pages**, 1,085 words. Page 2 holds the end of the unavailability paragraph, the scenario table and the limits. Without those two parts it is still slightly over one page (856 words). |
| Question texts | C12 is the only F3 cell without a period window; C03, C13 and C14 have one. |

## 2. What holds

- The rates are computed by code from the traces, not typed, and the eligibility level of each route is derived from them (highest level with no wrong value). A wrong value and an HTTP 401 or 429 are kept apart: only a wrong value lowers a level.
- Every line of the rule cites its cells and the `correct / cases` ratio for all five models. The Q3 question "which TD 1 cell justifies this line?" has an answer on the page.
- The checks follow the consistency constraint:
  - `none` only for a dashboard on a route at 100 % on the family;
  - a quorum for a customer figure on F1 and F3;
  - the reference for every age family;
  - reference then human review for a payout.

  The choice of the reference over a quorum on F2 is argued with C09, where our fixed panel keeps the wrong 0.
- The check belongs to the request and follows it to the fallback route (`checks_for`). When qwen (5/6 on F1) answers, `none` is refused.
- No model is written in the code: `RESOURCES` is built from `routing-config.json`, as the reproducibility rules ask. The kit file is kept byte-identical next to the adapted one, so before and after can be compared.
- The priority analysis reads the four branches of `choose` correctly: allocation is a sort key, not a filter. It runs the kit on the exact situation of the question, states a concrete condition for reversing the priority (quota left ≤ reserve for the requests that cannot wait) and runs it.
- Simulations are labelled `simulation`. The limits are written: one cell for four of the families, one run, the paid route untested.

## 3. Changes requested

1. **Restore `td1/` and pin the input (blocking, before 17:30).** Why: the assessment says "The README's commands must replay the work" and "a level 2 outcome with no evidence in the session's repository drops to 1". The TD 2 assignment says "TD 1 is not reopened". Where: `git checkout 00de7e3 -- td1/`, then commit. Pair A takes this one, since our Q1 demo breaks too; Pair C then re-runs its five commands. To catch the next edit:
   - write the SHA-256 of `td1/traces-td1.csv` (`889c2dc185debd79c68cfc4595928cfdf5cd5a1f4edf5f205eddd47705b7906d`) in `td2/C-routing/README.md`;
   - make `last_attempts` stop with a clear message when the header lacks `provider`, `case_id` or `verdict`.
2. **Do not credit gpt-oss-120b#openrouter with a TD 1 score it does not have.** In *urgent* the check reads "none (internal dashboard and gpt-oss-120b#openrouter at 100 % on F2 in TD 1)". That route made no call in TD 1 (`route_tested_in_td1: false`, and your own limits say so). The constraint allows no check only where *that model* scored 100 % in TD 1. OpenRouter can also serve one model ID through several upstream providers, so "same model" is an assumption. Where: in `checks_for` (`atelier-routage.py`), when `route_tested_in_td1` is false, apply `dashboard_if_not_100` (the reference, local, 0 USD), or at least write "evidence inherited from the groq route". Then regenerate `simulator-after.jsonl` and the *urgent* row of report §5.
3. **Say what happens to the quorum check when its members are down.** Scenario *first model unavailable* keeps P1 with dots-3 in n = 3, so gpt-oss-20b and qwen must both answer and agree. On the six F1 cells this abstains on C20 (qwen HTTP 429), and qwen is the route with the most availability failures in TD 1 (four cells). Report §2 says the quorum decided every cell "even with one member down": here two are down. With one more route down, the check can no longer pass at all (section 1), yet `choose` still runs the model. Where: rows F1 and F3 and scenario R2 of `routing-rule-en.md`, `panels` in `routing-config.json`, `panel_note` in `atelier-routage.py`, report §2. Do one of the following:
   - name a fallback panel, for instance north-mini-code + gpt-oss-20b + qwen (three families; with our vote, 6/6 on F1 and 4/4 on F3);
   - or write that the customer figure is withheld when fewer than k members are up, and abstain at once in that case.
4. **Bring the rule to one page.** Q3 says "Bring a one-page rule", and it prints on two (section 1). The scenario table and the limits are already in the report (§5, §7): link to them instead. Also shorten the F2 cell and the unavailability paragraph. Where: `routing-rule-en.md`.
5. **Make the README commands write what they claim to regenerate.** The README says "Each command regenerates its file in `outputs/` byte for byte", but the commands print to the terminal. Add `> td2/C-routing/outputs/simulator-after.jsonl` (and the same for the other two). Alternatively, add a line `| diff - td2/C-routing/outputs/…` that prints nothing when the output is unchanged. Where: `td2/C-routing/README.md`.
6. **Use one spelling of Lina's name.** It is "ZAAG" in `td2/C-routing/README.md` and in your review of Pair B, but "ZAAQ" in `README.md`, `reports/td1.md` and three places in `reports/td2.md` (members, §8, Contributions). Why: for the hand-in, the report states each member's contribution. Use the spelling of her Moodle account everywhere.

## 4. Remarks, no change required

- **`none` on a single cell.** On F2b and F1+F2b, the dashboard runs gpt-oss-20b with no check on the strength of C10 or C18 alone (1/1). This meets the letter of the constraint, and your limits say so. Expect the instructor to ask whether 1/1 counts as "100 %". A minimum number of cells before `none` would be one answer.
- **dots-3 first on F1 and F3.** It is a preview route, absent from the portfolio, and about four times slower than gpt-oss-20b (2.85 s against 0.70 s). For a dashboard it keeps the other quotas free, as you argue. For a customer figure the P1 quorum calls gpt-oss-20b and qwen anyway, so the choice of first model makes no difference there.
- **Three of the four F3 cells also have a period.** If the instructor points at the F3 line: C12 is the product-only cell, and C03, C13 and C14 also carry a period. Report §2 says so; the rule page does not.
- **Deferral at the deadline edge.** The condition `0 < reset_minutes <= deadline_minutes` lets `choose` defer a second time with no margin (section 1: 60 min left, refill announced in 60 min, defer). This comes from the kit. Either of these would avoid planning a delivery that cannot happen in time:
  - a margin (refill + call + reference check < deadline);
  - a limit of one deferral.

  A scenario *wake-up, still exhausted* would show it.
- **Quorum cross-check.** `td1_families.py` counts with its own `vote()`, which does not check the strict majority or duplicates. We ran our `vote_k_sur_n` on your panels and it agrees (section 1). Importing it, as `priority_demo.py` imports the kit, would leave a single implementation.

## 5. Questions we could not answer after the walkthrough

- **What does the model add on the age families?** The reference check runs the family's validated query locally at 0 USD and delivers the model's value only if it is equal, so the script alone would give the same figure. The model is needed only for a question that fits no validated template, and then there is no reference to check against. What does the rule do for such an F2 question?
- **Why wait 60 minutes to save 0.0006 USD?** In *deferrable*, the paid route of the same model is available at 0.0006 USD within a 0.30 budget. Yet the kit order (defer before paid) makes a dashboard wait an hour. Your §6 argues for running now on capacity already paid for. At what price per question would you pay rather than wait?

## 6. Before the marking (Q3, 17:30)

1. Restore `td1/` (change 1), then at `main` run `python3 td2/C-routing/td1_families.py` and `python3 td2/C-routing/atelier-routage.py | diff - td2/C-routing/outputs/simulator-after.jsonl` (no output means identical).
2. Keep `family-rates-td1.csv` open next to the rule: for any line, the cells are in the `correct_cells` and `wrong_cells` columns.
3. For "what if the first model is unavailable": `python3 td2/C-routing/atelier-routage.py --scenario "first model unavailable"`, then `--scenario deferrable`.

---

*AI assistance, declared as the assessment requires:* this review was drafted with Claude from the re-runs above, and Pair A checked it and remains responsible for it. Prompt as used, 18 November 2026: "remplie la review 1 pour la pair C ( je suis pair A) : https://github.com/Diaila1403/esilv-agentic-ai-td1/tree/main/td2/C-routing".
