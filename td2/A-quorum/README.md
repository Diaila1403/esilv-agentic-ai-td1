# TD2 Pair A: k-of-n Voting
**Members:** Diaila DIALLO, Meriam BOUMEDIENE  
**Date:** 18 November 2026

## 1. What we wanted to do
In this part of TD2, our goal was to understand how several AI models can work together to make a decision.
During TD1, we noticed that models could return different answers to the same question. Sometimes, they could even agree on a wrong answer.
We wanted to see whether using a voting system with more models could make the final decision more reliable.

## 2. Our implementation
We completed the `vote_k_sur_n()` function in `skeleton-multi-llm-en.py`.
The idea is simple: a response is accepted only if at least `k` out of `n` models agree on the same value.
We also had to respect some important rules:
- Only successfully executed responses with a valid value can vote.
- An unavailable model still counts in the total number of models.
- The required number of votes must be a strict majority.
- The same model cannot vote twice.
- If there are not enough matching votes, the system abstains.
We tested our function using `atelier-vote.py`, including cases where models disagree, become unavailable or agree on an incorrect answer.
We also ran `check_vote_contract.py`, and all **13 tests passed**.

## 3. Connection with what we learned in class
In class, we discussed why working with several LLM APIs can be challenging.
For example, an API can return an HTTP error such as **429**, meaning that too many requests have been sent. In that situation, a retry mechanism can be useful, sometimes with a delay before trying again.
We also discussed timeouts, including waiting limits such as 5 seconds, to avoid blocking the whole system when a model takes too long to respond.
These concepts are important for our voting system because a model might fail to produce an answer even after retries.
In our part, we did not implement a new retry mechanism. Instead, we used the execution results already available in the TD1 traces.
This helped us understand an important point: **a model that fails or times out should not vote, but it should still count in the original panel size.**

## 4. Comparing 2-of-3 and 3-of-5
We wrote `comparaison-votes.py` to compare two voting configurations using the 20 questions from TD1.
- **2of3:** at least 2 out of 3 models must agree.
- **3of5:** at least 3 out of 5 models must agree.
We used `traces-td1.csv` to recover the models' answers and `reference-td1.csv` to check whether the accepted answers were correct.
The results were saved in `comparaison-votes.csv`.

## 5. What we observed
Out of 20 questions, **18 decisions stayed the same**, while **2 changed**.
The two interesting cases were:
**C02:** The 2of3 system accepted the correct answer, 590320. However, the 3-of-5 system abstained because there were not enough matching votes.
**C09:** The 2of3 system accepted 0, even though the correct answer was 487980. With 3-of-5, the system abstained instead of accepting this wrong answer.
For C17, both configurations abstained.
These results showed us that increasing the required number of votes can prevent some incorrect consensuses, but it can also reject correct answers.

## 6. How to reproduce our results
From the repository root:
```bash
python3 td2/A-quorum/atelier-vote.py
python3 td2/A-quorum/comparaison-votes.py
python3 td2/A-quorum/check_vote_contract.py
```
The comparison evaluates 20 questions and identifies 2 changed decisions. The contract tests pass (13/13).

## 7. Conclusion
This exercise helped us understand that agreement between AI models does not necessarily mean that their answer is correct.
We also saw why handling unavailable models matters when designing a reliable voting system.
The 3-of-5 configuration avoided the incorrect consensus observed in C09, but it also abstained on the correct answer in C02.
**Our main takeaway is that a stronger voting requirement does not automatically guarantee better answers. It creates a trade-off between accepting answers and abstaining when there is not enough agreement.**
