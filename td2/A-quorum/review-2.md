# Review of Pair A (Step 1, k-of-n vote) by Pair C

**Reviewed:** commit `b53981c` (18 November 2026, 14:19; files then moved by Pair A into this folder, commits `06f72c1` to `bcd4ed3`, whitespace changes only), files `skeleton-multi-llm-en.py`, `comparaison-votes.py`, `comparaison-votes.csv`, Step 1 of `reports/td2.md`. **Reviewers:** Pair C (Jean VASSEUR, Lina ZAAG). **Date:** 18 November 2026.

**Verdict:** the vote is correct and the table is right. Two reproducibility problems blocked a replay from a fresh clone; Pair C fixed them at the review (please confirm). Four changes are requested for the report, two of them to reach level 2 on Q1.

## 1. What we re-ran

| Command | Result |
|---|---|
| `python3 td2/A-quorum/atelier-vote.py` | the four synthetic examples give the decisions of your table: agreement 100 (2 votes), disagreement abstain (1), unavailable abstain (1), wrong consensus 0 (2, reference 100) |
| `atelier-vote.py --traces td1/traces-td1.csv --case` C01, C02, C09, C17, C20 | C01 792800 (2 votes, north-mini-code HTTP 401 kept in n); C02 590320 (2); C09 **0** (2, reference 487980); C17 abstain (largest count 1); C20 1106090 (2, qwen HTTP 429 kept in n) |
| `python3 td2/A-quorum/check_vote_contract.py` | **13/13 PASS**: duplicate pair refused even when both are errors, k = 1 of 3, 2 of 4 and 4 of 3 refused, 3-of-5 with two members down abstains on 2 agreeing votes and decides on 3, value 0 votes, an executed proposal without a value does not |
| `python3 td2/A-quorum/comparaison-votes.py` | `comparaison-votes.csv` regenerated **byte-identical** to commit `b53981c` |
| Independent count by Pair C (`td2/C-routing/td1_families.py`, own strict-majority count, not your code) | agrees on all twenty questions: 2-of-3 keeps the wrong 0 on C09 and abstains on C17; 3-of-5 abstains on C02, C09 and C17 |

## 2. What holds

- The five points of the docstring contract are implemented, in the right order: the duplicate check comes before the verdict test, so two errors from the same pair are refused too; `votes` is the largest count on abstention; no value is ever invented.
- The values quoted for C02, C09 and C17 are exact (checked against `traces-td1.csv`).
- The conclusion is the right one: a stricter quorum gives more abstentions, not more truth (Lecture 2).

## 3. Fixed by Pair C at the review (please confirm)

| # | Problem | Effect | Fix |
|---|---|---|---|
| F1 | `comparaison-votes.py` loaded the skeleton from `~/Downloads/esilv-student-2026-10-18/kit-td1/`, a folder on the author's machine, and read the traces from the current directory | crashed on every other machine; on the author's machine it ran a copy that is not necessarily the committed one | loads the skeleton next to the script, reads `td1/traces-td1.csv` and `td1/reference-td1.csv`, writes the CSV next to itself; output unchanged |
| F2 | The skeleton imports `sandbox_sqlite` when it loads; neither `sandbox_sqlite.py` nor the driver `atelier-vote.py` was committed | `atelier-vote.py`, the Q1 demonstration, failed from a fresh clone with `FileNotFoundError: sandbox`. The assessment rule: an outcome at 2 whose evidence is absent from the repository drops to 1 | both kit files added unchanged next to the skeleton |

## 4. Changes requested

1. **Add the test outputs for duplicates and k bounds to the report.** The hand-in asks for "test outputs for agreement, disagreement, unavailable members and duplicate routes"; the report shows the first three only. Paste the output of `check_vote_contract.py` (or your own tests) under *Synthetic Tests*. This is the Q1 level-2 evidence: "two accesses to the same provider and model pair count as one vote".
2. **Comment the vote margins, not only the two changed decisions.** The assignment asks for an explanation "for every question where moving from 2-of-3 to 3-of-5 changes the decision (for instance ... shifting the vote margin because of an HTTP 429 or an invalid SQL statement)". In your CSV: C01 and C02 decided with 2 votes because north-mini-code got HTTP 401 (kept in n); C20 with 2 because qwen got HTTP 429 twice; C08 and C10 only 3 votes in 3-of-5 because north-mini-code and dots agree on a wrong value (0 on C08, 119410 on C10); C15 and C19 2 votes because qwen is wrong (0; 83580 after a 429 retry). One more failure on these cells turns them into abstentions.
3. **Add the `votes` and reference-agreement columns to the twenty-question table of the report.** They are in the CSV; the expected artefact lists "consensus or abstention, value, votes, agreement with the reference".
4. **C02: name the verdicts and say what it proves.** gpt-oss-20b `incorrect` 0, dots `incorrect` 135000, north-mini-code `access_error` HTTP 401. The 2-of-3 consensus on C02 is reached with the HTTP 401 member still counted in n = 3: that is the Q1 level-2 evidence "an unavailable member stays in n", already in your data.

## 5. Remarks, no change required

- The contract refuses the same (provider, model) pair only: the same model reached through two providers counts as two votes (checked: gpt-oss-120b via groq and via openrouter gives a 2-vote consensus). Lecture 2 counts it once. Never put both routes of one model in a panel; Pair C's rule has gpt-oss-120b on groq and on openrouter, as fallbacks, never as two voters.
- The 3-of-5 quorum contains gpt-oss-120b and gpt-oss-20b, the same family: the "distinct families" property of the fixed panel does not hold for it. Worth one sentence.
- The last attempt is the last row in file order, as in `atelier-vote.py`. Correct on our chronological traces; sort by `(attempts, date_utc)` if trace files are ever merged out of order.
- Cosmetic: no blank line between the end of `vote_k_sur_n` and the next section banner of the skeleton.

## 6. For the demonstration in front of the instructor (Q1)

`--case C17` shows an abstention (largest count 1, no value invented); `--case C01` shows an unavailable member kept in n; `check_vote_contract.py` shows the duplicate pair refused.
