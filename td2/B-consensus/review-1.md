# Review of Pair B (Step 2 : Wrong Consensus) by Pair A

**Reviewed:** Pair B – Simeon SIMEONOV, Arthur GAUCHÉ, Imane BOUNA MOCTAR  
**Reviewers:** Diaila DIALLO, Meriam BOUMEDIENE (Pair A)  
**Date:** 18 November 2026  
**Verdict:** Changes requested

## 1. What we checked
We reviewed the Step 2 section in `reports/td2.md` and the README in `td2/B-consensus/`.
We checked the explanation of case C09, the two incorrect SQL queries, the reference value, and the comparison between the 2-of-3 and 3-of-5 voting systems.
We did not independently rerun the SQL queries on the database.

## 2. What holds

- Pair B identified a clear example of wrong consensus using real TD1 traces.
- In C09, Cohere and Qwen both returned 0, while the correct answer was 487980 cents.
- The 2-of-3 panel accepted the wrong value, while the 3-of-5 quorum abstained.
- The report explains why both SQL queries are incorrect.
- The delta analysis identifies six customers and accounts for the missing 487980 cents.
- The proposed independent reference check is relevant.

## 3. Changes requested

1. Add the SQL queries as separate files in `td2/B-consensus/`, so they can be easily tested.
2. Include the delta query and its output in the folder.
3. Complete the README with the files, results, and commands needed to reproduce the analysis.
4. Demonstrate the C09 voting result using Pair A's `vote_k_sur_n` implementation, rather than relying only on manual counting.

## 4. Remarks – No change required

The example is relevant because it shows that two models can agree on the same incorrect result for different reasons.

The report also correctly explains that increasing the quorum can prevent a wrong consensus, but can also lead to more abstentions.

## 5. Questions we could not answer

- Can the complete SQL analysis be reproduced directly from the files in `td2/B-consensus/`?
- Has the C09 result been tested using Pair A's voting function?

Overall, the analysis is clear and well supported in the report. The main improvement needed is to make the evidence reproducible from Pair B's own folder.
