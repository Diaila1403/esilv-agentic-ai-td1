# TD 2 · Pair A · Step 1: the k-of-n vote

**Members:** Diaila DIALLO, Meriam BOUMEDIENE · **Session:** 18 November 2026 · **Pack:** 2026-11-18-students-5
**Report section:** [`reports/td2.md`, Step 1](../../reports/td2.md#step-1--k-of-n-vote-pair-a) · **Reviews received:** [`review-1.md`](review-1.md) by Pair B, [`review-2.md`](review-2.md) by Pair C

## What was done

- `Orchestrateur.vote_k_sur_n` completed in `skeleton-multi-llm-en.py`: only executed proposals with a value vote, an unavailable member stays in n, k must be a strict majority (`n // 2 < k <= n`, else `ValueError`), a duplicate provider and model pair raises `ValueError`, abstention without a value when no value reaches k.
- The four synthetic examples of `atelier-vote.py` run: agreement, disagreement, unavailable members, wrong consensus.
- The twenty questions decided by the fixed 2-of-3 panel (gpt-oss-120b, north-mini-code:free, qwen3.8-27b, k = 2) and by the 3-of-5 quorum over the five TD 1 models (k = 3), on the last attempt of each cell of `traces-td1.csv`: [`comparaison-votes.csv`](comparaison-votes.csv).

## Files

| File | Content | Origin |
|---|---|---|
| [`skeleton-multi-llm-en.py`](skeleton-multi-llm-en.py) | Kit skeleton with `vote_k_sur_n` completed | Pair A |
| [`comparaison-votes.py`](comparaison-votes.py) | Builds the 2-of-3 versus 3-of-5 table | Pair A; paths fixed by Pair C, see the review |
| [`comparaison-votes.csv`](comparaison-votes.csv) | The twenty decisions: consensus, value, votes, agreement with the reference | Pair A, regenerated identical |
| [`atelier-vote.py`](atelier-vote.py) | Kit driver of the vote (synthetic examples, one real question) | kit, unchanged |
| [`sandbox_sqlite.py`](sandbox_sqlite.py) | Kit read-only SQLite sandbox, imported by the skeleton when it loads | kit, unchanged |
| [`check_vote_contract.py`](check_vote_contract.py) | Thirteen contract checks: duplicates, k bounds, unavailable members with n = 5, value 0 | Pair C, cross-review |

## Replay (from the repository root, no key, no network)

```bash
python3 td2/A-quorum/atelier-vote.py                                   # four synthetic examples
python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C09 # wrong consensus kept by 2-of-3
python3 td2/A-quorum/atelier-vote.py --traces td1/traces-td1.csv --case C17 # abstention (largest count 1)
python3 td2/A-quorum/comparaison-votes.py                              # rewrites comparaison-votes.csv
python3 td2/A-quorum/check_vote_contract.py                            # 13/13 PASS
```

## Main results

- 18 of the 20 decisions are the same in 2-of-3 and 3-of-5. C02: correct consensus 590320 in 2-of-3, abstention in 3-of-5. C09: wrong consensus 0 in 2-of-3 (north-mini-code and qwen, reference 487980), abstention in 3-of-5.
- C17: both abstain.
- A larger quorum removes the wrong consensus of C09 at the price of an abstention on C02.
