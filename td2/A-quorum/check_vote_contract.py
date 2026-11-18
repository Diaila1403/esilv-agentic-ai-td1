#!/usr/bin/env python3

"""Cross-review tool written by Pair C: checks vote_k_sur_n against the TD 2 contract.

Exercises the cases that atelier-vote.py does not cover: duplicate provider and
model pair, k outside the strict majority, unavailable members kept in n with
n = 5, value 0, executed proposal without a value. Synthetic proposals only
(nature: simulation), no network, no key.

Usage, from the repository root:
    python3 td2/A-quorum/check_vote_contract.py
Exit code 0 when every check passes, 1 otherwise.
"""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("student_skeleton", HERE / "skeleton-multi-llm-en.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def vote(proposals, k):
    return module.Orchestrateur.vote_k_sur_n(None, proposals, k)


def proposal(provider, model, value):
    return SimpleNamespace(provider=provider, model_requested=model, value=value,
                           verdict="executed" if value is not None else "error")


def panel(*values):
    return [proposal(f"provider{i}", f"model{i}", v) for i, v in enumerate(values)]


def raises_value_error(proposals, k):
    try:
        vote(proposals, k)
    except ValueError:
        return True
    return False


CHECKS = [
    ("2-of-3, two agree: consensus 100 with 2 votes",
     lambda: vote(panel(100, 100, 120), 2) == {"consensus": True, "value": 100, "votes": 2,
                                               "models": ["provider0:model0", "provider1:model1"]}),
    ("2-of-3, all differ: abstain, votes 1, no value invented",
     lambda: vote(panel(100, 110, 120), 2) == {"consensus": False, "value": None, "votes": 1, "models": []}),
    ("2-of-3, one unavailable stays in n: 2 agreeing votes still decide",
     lambda: vote(panel(100, 100, None), 2)["consensus"] is True),
    ("2-of-3, two unavailable: abstain (n stays 3, k stays 2)",
     lambda: vote(panel(100, None, None), 2) == {"consensus": False, "value": None, "votes": 1, "models": []}),
    ("3-of-5, two unavailable, two agree: abstain (threshold not lowered to 2 of 3 received)",
     lambda: vote(panel(42, 42, 41, None, None), 3)["consensus"] is False),
    ("3-of-5, two unavailable, three agree: consensus",
     lambda: vote(panel(42, 42, 42, None, None), 3)["value"] == 42),
    ("value 0 is a vote like any other",
     lambda: vote(panel(0, 0, 100), 2)["value"] == 0),
    ("executed proposal without a value does not vote",
     lambda: vote([SimpleNamespace(provider="a", model_requested="m", value=None, verdict="executed"),
                   *panel(1, 2)], 2)["consensus"] is False),
    ("duplicate (provider, model) pair raises ValueError",
     lambda: raises_value_error([proposal("groq", "openai/gpt-oss-120b", 1),
                                 proposal("groq", "openai/gpt-oss-120b", 1),
                                 proposal("openrouter", "cohere/north-mini-code:free", 2)], 2)),
    ("duplicate pair raises ValueError even when both are errors",
     lambda: raises_value_error([proposal("groq", "a", None), proposal("groq", "a", None),
                                 proposal("x", "b", 2)], 2)),
    ("k = 1 of 3 (not a strict majority) raises ValueError", lambda: raises_value_error(panel(1, 1, 2), 1)),
    ("k = 2 of 4 (not a strict majority) raises ValueError", lambda: raises_value_error(panel(1, 1, 2, 3), 2)),
    ("k = 4 of 3 (above n) raises ValueError", lambda: raises_value_error(panel(1, 1, 2), 4)),
]

# Documented, not a failure: the contract refuses the same (provider, model) pair
# only. The same model reached through two providers is accepted as two votes,
# whereas Lecture 2 counts it once. Avoid such a panel.
NOTE = vote([proposal("groq", "openai/gpt-oss-120b", 1),
             proposal("openrouter", "openai/gpt-oss-120b", 1),
             proposal("openrouter", "cohere/north-mini-code:free", 2)], 2)


def main():
    failed = 0
    for name, check in CHECKS:
        try:
            ok = bool(check())
        except Exception as exc:  # a crash is a failed check, reported with its cause
            ok, name = False, f"{name} (crashed: {type(exc).__name__}: {exc})"
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"NOTE  same model on two providers counts as {NOTE['votes']} votes: {NOTE}")
    print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} checks passed (nature: simulation)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
