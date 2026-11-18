# Review of Pair B (Step 2, wrong consensus) by Pair C

**Status: pending.** At the time of review (18 November 2026, last commit on `main`: `bcd4ed3`), Pair B had pushed no file. This review will be completed on Pair B's commit. **Reviewers:** Pair C (Jean VASSEUR).

## What Pair C will re-run and check (Q2 rubric and Step 2 deliverable)

| # | Check | How |
|---|---|---|
| 1 | The case is identified and labelled: own batch or DEMO-SQL-C11 | README and report |
| 2 | At least two models return the **same wrong** value (`verdict = incorrect`, identical `value`) | against `td1/traces-td1.csv`, last attempt of each cell |
| 3 | The independent reference comes from `reference-td1.csv` (SQL on the database), never from a model | value and query |
| 4 | The panel and threshold are declared, and the 2-of-3 and 3-of-5 results are distinguished from the agreement itself | compared with Pair A's `comparaison-votes.csv` |
| 5 | The two SQL queries are complete and are the ones in the traces (`sql` column) | diff against the trace |
| 6 | The faulty WHERE or JOIN condition is explained exactly: which birth-date window it tests against the window "exactly 25 on the reference date" | re-reading the SQL |
| 7 | The delta query runs on `data/boutique.sqlite`, lists the `customer_id` rows with their revenue, and **its sum equals reference minus wrong value** | executed by Pair C on a fresh clone |
| 8 | An independent check able to detect the error is named (e.g. the reference query of the family, not another model) | README |

## Facts from our traces that the analysis can be checked against

Shared wrong values in `traces-td1.csv` (last attempt, identical `incorrect` value), from Pair C's family table:

| Case | Models agreeing on the wrong value | Wrong value | Reference | Fixed 2-of-3 | 3-of-5 |
|---|---|---:|---:|---|---|
| C09 | north-mini-code:free, qwen3.8-27b | 0 | 487980 | **keeps 0** (2 votes) | abstains |
| C08 | north-mini-code:free, dots-3-note-preview:free | 0 | 605580 | correct 605580 | correct (3 votes) |
| C10 | north-mini-code:free, dots-3-note-preview:free | 119410 | 558980 | correct 558980 | correct (3 votes) |

C09 is the only case where the wrong agreement wins a declared quorum; it is the one that justifies the reference check on age families in Pair C's routing rule. For C09 the delta query must account for 487980 cents.
