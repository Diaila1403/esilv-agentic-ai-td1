# TD 2 · 18 November 2026 · The quorum, then the routing rule

Sub-group **DIA5-G3** (DIA5) · pack `2026-11-18-students-5` · assignment: [TD 2](https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/students/kit-td1/enonce-td2-en.html) · session report: [`reports/td2.md`](../reports/td2.md)

Input of the whole session: the TD 1 outputs in [`td1/`](../td1/README.md), mainly [`traces-td1.csv`](../td1/traces-td1.csv) (104 real calls) and [`reference-td1.csv`](../td1/reference-td1.csv). No new network call.

## One folder per pair

| Step | Pair | Folder | What is in it | Status |
|---|---|---|---|---|
| 1. The k-of-n vote | A | [`A-quorum/`](A-quorum/README.md) | `vote_k_sur_n`, driver, twenty-question table 2-of-3 versus 3-of-5 | done, reviewed by C |
| 2. The wrong consensus | B | [`B-consensus/`](B-consensus/README.md) | shared wrong value, faulty SQL clause, delta query | written in the report (C09), reviewed by C; evidence files to commit |
| 3. The routing rule | C | [`C-routing/`](C-routing/README.md) | rates per family, one-page rule, simulator before and after, priority analysis | done, to be reviewed by A and B |

Each folder holds the pair's files, its `README.md` (what was done, files, replay commands, results) and the two reviews it received, `review-1.md` and `review-2.md`, written by the two other pairs in alphabetical order.

## Cross-review

| Folder | `review-1.md` | `review-2.md` |
|---|---|---|
| `A-quorum/` | by Pair B: (A-quorum/review-1.md) | by Pair C: (A-quorum/review-2.md) |
| `B-consensus/` | by Pair A: (B-consensus/review-1.md) | by Pair C: (B-consensus/review-2.md) |
| `C-routing/` | by Pair A: (C-routing/review-1.md) | by Pair B: (C-routing/review-2.md) |

## Replay everything (from the repository root, Python 3, no key, no network)

```bash
# Pair A
python3 td2/A-quorum/atelier-vote.py
python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C09
python3 td2/A-quorum/comparaison-votes.py
python3 td2/A-quorum/check_vote_contract.py
# Pair C
python3 td2/C-routing/td1_families.py --csv td2/C-routing/family-rates-td1.csv
python3 td2/C-routing/atelier-routage-kit.py
python3 td2/C-routing/atelier-routage.py
python3 td2/C-routing/priority_demo.py
```
