# TD 2 · Pair B · Step 2: the wrong consensus

**Members:** *[to complete]* · **Session:** 18 November 2026 · **Pack:** 2026-11-18-students-5
**Report section:** [`reports/td2.md`, Step 2](../../reports/td2.md#step-2--the-wrong-consensus-pair-b) · **Reviews received:** [`review-1.md`](review-1.md) by Pair A (to write), [`review-2.md`](review-2.md) by Pair C (pending)

> **Status: not pushed yet.** Folder created by Pair C for the per-pair layout on 18 November 2026. Pair B replaces this README with its own: what was done, files, commands that replay it, results.

## Expected in this folder (assignment, Step 2, and assessment, Q2)

| Evidence | Suggested file |
|---|---|
| The identified case: question, models agreeing, shared wrong value, independent reference from `reference-td1.csv`, nature (own batch or DEMO-SQL-C11) | this README and Step 2 of `reports/td2.md` |
| Declared panel and threshold, and what the fixed 2-of-3 panel and the 3-of-5 quorum return (counted by hand, then with Pair A's `vote_k_sur_n`) | idem |
| The two complete SQL queries returned by the models, and the exact WHERE or JOIN condition that produces the wrong value | `queries-<case>.sql` |
| The delta SELECT executed on `data/boutique.sqlite`: the exact `customer_id` rows (and their revenue excluding VAT) counted by the reference and missed or added by the faulty queries; their sum equals reference minus wrong value | `delta-<case>.sql` and its output |
| The independent check able to detect the error | README |
| The commands that replay it from a fresh clone; `data/boutique.sqlite` committed, or its SHA-256 and the path of the kit file | README |
