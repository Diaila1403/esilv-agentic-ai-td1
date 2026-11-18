#!/usr/bin/env python3
"""TD 2 Step 3 (Pair C): the priority between included capacity and deferral, executed.

Runs the unchanged kit policy (atelier-routage-kit.py) on the exact situation
asked about in the assignment, then a variant that reverses the priority under
the operational condition written in reports/td2-step3-routing.md.
Synthetic resources and quota figures: nature "simulation", no API call.

Usage, from the repository root:
    python3 routing/priority_demo.py
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("kit", HERE / "atelier-routage-kit.py")
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)

# The situation of the question: a deferrable request that the free resource
# could serve; the free resource is exhausted (cash 0, allocation 0) and refills
# in 30 minutes, before the 120-minute deadline; the subscription is available
# (cash 0, allocation 0.04).
REQUEST = {"difficulty": 1, "high_impact": False, "can_wait": True,
           "deadline_minutes": 120, "budget": 0.30}
STATE = [dict(r, available=False, reset_minutes=30) if r["id"] == "small-free" else dict(r)
         for r in kit.RESOURCES]


def choose_with_reserve(request, resources, quota_left, reserve):
    """Reversed priority: keep the included quota for requests that cannot wait.

    Condition: the request can wait, a free eligible resource refills before
    the deadline, and the subscription quota left in its window is not larger
    than the reserve needed by non-deferrable requests before its own reset.
    """
    eligible = [r for r in resources if r["level"] >= request["difficulty"]]
    waiting = [r for r in eligible if not r["available"] and r["cash"] == 0
               and r["allocation"] == 0 and r["reset_minutes"] is not None
               and 0 < r["reset_minutes"] <= request["deadline_minutes"]]
    if request["can_wait"] and waiting and quota_left <= reserve:
        chosen = min(waiting, key=lambda r: r["reset_minutes"])
        return {"action": "defer", "resource": chosen["id"], "cash": 0,
                "reason": f"subscription quota left {quota_left} <= reserve {reserve} for "
                          "non-deferrable requests; free refill before deadline: recheck at wake-up",
                "wake_in_minutes": chosen["reset_minutes"]}
    return kit.choose(request, resources)


def show(label, result):
    print(json.dumps({"case": label, "nature": "simulation", "request": REQUEST,
                      "small-free": "exhausted, refill in 30 min", "result": result}))


if __name__ == "__main__":
    show("kit choose (unchanged)", kit.choose(REQUEST, STATE))
    show("reversed rule, quota scarce (5 left, reserve 8)", choose_with_reserve(REQUEST, STATE, 5, 8))
    show("reversed rule, quota ample (40 left, reserve 8)", choose_with_reserve(REQUEST, STATE, 40, 8))
