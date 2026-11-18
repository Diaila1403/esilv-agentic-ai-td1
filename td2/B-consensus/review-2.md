# Review of Pair B (Step 2, wrong consensus) by Pair C

**Reviewed:** Step 2 of `reports/td2.md` at commit `04c8f06` (18 November 2026, 15:11; `main` at `76c5a41` when reviewed). Pair B: Simeon SIMEONOV, Arthur GAUCHÉ, Imane BOUNA MOCTAR. **Reviewers:** Pair C (Jean VASSEUR). **Date:** 18 November 2026.

**Verdict:** the analysis is right and every figure holds. We re-derived it from `td1/traces-td1.csv` and re-executed every query on `data/boutique.sqlite`. The content meets the Q2 level 2 evidence: two models with the same wrong value, the reference, the quorum result kept apart from the agreement, the cause in the SQL and an independent check. What is missing is the evidence in the repository: nothing in `td2/B-consensus/` replays the analysis, and the "delta" query does not involve the faulty clauses. Four changes are requested. None of them changes a number.

## 1. What we re-ran

Database: `data/boutique.sqlite` of the kit `kit-td1/`, opened read-only, SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`. Traces: last attempt of each model on each question, in file order.

| Check | Result |
|---|---|
| Shared wrong values on the twenty questions, all five models (`verdict = incorrect`, identical `value`) | exactly your three: **C08** 0 (north-mini-code, Dots; reference 605580), **C09** 0 (north-mini-code, qwen3.8-27b; reference 487980), **C10** 119410 (north-mini-code, Dots; reference 558980). There is no other. |
| The five C09 cells | 120b 487980 correct, 20b 487980 correct, qwen 0 incorrect, north-mini-code 0 incorrect, Dots 47900 incorrect; `nature = real`, one attempt each |
| `python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C09` | fixed panel, n = 3, k = 2: `consensus: true, value: 0, votes: 2` (north-mini-code, qwen), `matches_reference: false` |
| Own count, every question: fixed 2-of-3, 3-of-5, Pair C's P1 (Dots, 20b, qwen) | C09: fixed **0** (wrong), 3-of-5 abstains (487980: 2, 0: 2, 47900: 1), P1 abstains (1 vote each). C09 is the only question where a quorum keeps a wrong value. C08 and C10 are outvoted (correct in all three). C02: 3-of-5 abstains where 2-of-3 is right. All of this agrees with Pair A's `comparaison-votes.csv`. |
| Your SQL blocks against the `sql` column of the trace | qwen and the reference: identical. north-mini-code: **reformatted and its two comments removed** (same logic, same result). |
| Execution of the C09 queries | north-mini-code 0, qwen 0, Dots 47900, gpt-oss-120b 487980, reference 487980 |
| Row-level version of the two faulty queries (`SELECT DISTINCT c.customer_id` with the same `FROM`/`WHERE`) | both count **no customer**. Dots counts C003 only. |
| Your delta query | the six rows of your table (C001, C002, C003, C007, C008, C009), total **487980**: exact |
| Your explanation of the north-mini-code clause | right: the left-hand side is the birth year minus 0 or 1. On this database it takes values from 1958 to 2006, never 25. |
| Your explanation of the qwen clause | right on both points: the age is taken at `o.date`, and `date(birth_date, '+26 years')` keeps the month and day. On this database that holds for every customer: none is born on 29 February, the only date that `+26 years` would move. The interval is empty. |
| Boundaries of the reference window ]2000-09-26 ; 2001-09-26] | C003 (born 2001-09-26, 25 that day) is counted. C005 (born 2000-09-26, 26 that day) and C004 (2000-09-25) are not. No customer of the window is without orders. |

## 2. What holds

- The case is identified, real, taken from the five models and not only from the panel. The choice of C09 is argued: it is the only shared wrong value that wins the fixed panel.
- The agreement is kept apart from the quorum result: the same 0 wins 2-of-3 and is blocked by 3-of-5. The price of 3-of-5 (C02) is stated.
- The two root causes are different and both explained. The conclusion follows: the agreement is an accident, not evidence.
- The independent check is named (the family's reference query, a plausibility rule) and linked to Pair C's rule for F2. Limits are written: one batch, one run.

## 3. Changes requested

1. **Put the evidence in `td2/B-consensus/` with a README that replays it.** The folder holds no file from Pair B. The analysis exists only as text in the report, and the queries were run on a database that is not in the repository. Why: hand-in ("commit the report with the code, prompts and evidence"), code basics ("a README whose commands replay the work"), assessment ("the instructor marks what has been shown on screen"). Suggested files:
   - `queries-c09.sql`: the three model queries and the reference, verbatim;
   - `delta-c09.sql` and its output `delta-c09.csv`;
   - `README.md`: the commands, the path `kit-td1/data/boutique.sqlite` and its SHA-256 (above).
2. **Make the delta query a delta.** Your query is the reference query grouped by customer. It never uses the faulty `WHERE` clauses, so it shows what the reference counts, not what the faulty queries miss. The assignment asks for the rows "counted by your reference query but missed (or wrongly added) by the faulty queries". The valued outcome is "the delta query isolating the exact rows that differ from the reference". Here the result is the same because the faulty queries count nothing, but the query has to show that. A version that puts both conditions on the same order lines, executed by Pair C (same six rows; `added_cents` 0; missed 487980 for each faulty query, so 487980 − 487980 + 0 = 0, the wrong value):

   ```sql
   WITH lines AS (
     SELECT c.customer_id, c.birth_date, o.quantity_product * p.price AS cents,
            (c.birth_date <= date('2026-09-26', '-25 years')
             AND c.birth_date > date('2026-09-26', '-26 years')) AS in_reference,
            ((CAST(SUBSTR(c.birth_date, 1, 4) AS INTEGER) -
              CASE WHEN SUBSTR(c.birth_date, 6, 2) > '09' THEN 1
                   WHEN SUBSTR(c.birth_date, 6, 2) = '09' AND SUBSTR(c.birth_date, 9, 2) > '26' THEN 1
                   ELSE 0 END) = 25) AS in_cohere,
            ((strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
             AND strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date)
             AND strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years'))) AS in_qwen
     FROM orders o
     JOIN customers c ON o.customer_id = c.customer_id
     JOIN product p ON o.product_id = p.product_id
   )
   SELECT 'north-mini-code' AS faulty_query, customer_id, birth_date,
          SUM(CASE WHEN in_reference AND NOT in_cohere THEN cents ELSE 0 END) AS missed_cents,
          SUM(CASE WHEN in_cohere AND NOT in_reference THEN cents ELSE 0 END) AS added_cents
   FROM lines WHERE in_reference OR in_cohere GROUP BY customer_id
   UNION ALL
   SELECT 'qwen3.8-27b', customer_id, birth_date,
          SUM(CASE WHEN in_reference AND NOT in_qwen THEN cents ELSE 0 END),
          SUM(CASE WHEN in_qwen AND NOT in_reference THEN cents ELSE 0 END)
   FROM lines WHERE in_reference OR in_qwen GROUP BY customer_id
   ORDER BY faulty_query, customer_id;
   ```

3. **Quote the north-mini-code query as returned.** The report gives it reformatted, without its two comments `-- Compute age on 2026-09-26` and `-- Age = year difference`. The assignment asks for "the two complete SQL queries". Those comments help your diagnosis: the model says it computes a difference with 2026 and never writes 2026.
4. **Show the vote instead of counting by hand.** "Counted by hand" is the weakest form of Evidence 1. Two sources already in the repository show it on screen:
   - the fixed panel: `python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C09` (output in section 1);
   - the 3-of-5 quorum: the C09 row of `td2/A-quorum/comparaison-votes.csv` (abstention).

   Cite both.

## 4. Remarks, no change required

- **Dots, 47900.** It is less a boundary slip than a window of one day instead of one year. Its condition `'2026-09-26' = birth_date + 25 years` keeps only customers whose 25th birthday is exactly the reference date: only C003. The case also tests your proposed checks. The plausibility rule ("0 for an age group that has customers is suspicious") catches the two 0 values, but not 47900. The family's reference query catches all three. Worth saying, because it is the argument for the reference check rather than a sanity rule.
- **Pair C's rule.** The rule applies a reference check to F2 for customer and payout uses. For a dashboard it sends F2 to gpt-oss-120b (20/20, right on C09) without a check. Your sentence holds if it names those uses.
- **The two correct votes.** Your note that 120b and 20b share a family is right: the 2–2 tie in 3-of-5 rests on two models that are not independent.
- **Boundary customers.** For the oral, C003 (counted) and C005 and C004 (not counted) show the convention at both ends of the window in a few seconds.

## 5. For the demonstration in front of the instructor (Q2)

1. `python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C09`: the panel keeps 0 with two votes, while the reference is 487980.
2. The two queries, verbatim. Point at the `WHERE` of each: a birth year compared with 25; an empty month-day interval at the order date.
3. The delta query on `data/boutique.sqlite`: six customers, 487980 cents missed, 0 added.
4. The check that detects it: the family's reference query. The plausibility rule is not enough (Dots, 47900).
