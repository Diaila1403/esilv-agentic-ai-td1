#!/usr/bin/env python3
"""TD 2 Step 3 (Pair C): the kit routing simulator, adapted to the rule of DIA5-G3.

Adapted from the kit file atelier-routage.py (kept unchanged next to this file
as atelier-routage-kit.py, SHA-256 2971555a...). No API call, no key.

What changed compared with the kit:
- RESOURCES are the six routes of our portfolio (the five TD 1 models on their
  free plans, plus the pay-per-token route of gpt-oss-120b), read from
  routing-config.json; no model is written in this file.
- The level of each resource is not typed by hand: td1_families.py derives it
  from traces-td1.csv (highest level with no wrong value).
- A request names a question family and a use (dashboard, customer, payout)
  instead of a bare difficulty and a high_impact flag. The family gives the
  difficulty; the use gives the check. Difficulty chooses the model, stakes
  choose the check (Lecture 2).
- choose keeps the four branches of the kit in the same order (included, defer,
  paid, abstain). Inside a branch, ties are broken by the TD 1 rate on the
  family, then by the lowest level (keep the free quota of the strong model for
  the families only it solves), then by availability failures seen in TD 1.
- The check belongs to the request, not to the route: "none" is kept only for a
  dashboard when the chosen route is at 100 % on the family in TD 1; otherwise
  the family's stricter check applies, on any fallback route.
- Every reason cites the TD 1 cells behind the decision.

Availability states in the scenarios are assumptions, labelled "simulation".

Usage, from the repository root:
    python3 td2/C-routing/atelier-routage.py                       # all scenarios, JSON lines
    python3 td2/C-routing/atelier-routage.py --scenario deferrable # one scenario
    python3 td2/C-routing/atelier-routage.py --markdown            # table for the report
"""
import argparse
import json

from td1_families import analyse, evidence_key, fmt_unavailable, fmt_wrong

CONFIG, _CELLS, TD1_STATS, TD1_LEVELS, _PANELS, TD1_FAILED = analyse()


def cost_per_request(resource, envelope):
    price = resource["price_usd_per_million"]
    return round((envelope["input"] * price["input"] + envelope["output"] * price["output"]) / 1e6, 6)


def build_resources(config):
    resources = []
    for r in config["resources"]:
        key = evidence_key(r)
        cash = cost_per_request(r, config["token_envelope"]) if r["access"] == "tokens" else 0.0
        resources.append({
            "id": r["id"],
            "level": TD1_LEVELS[key][0],
            "access": r["access"],
            "available": True,
            "cash": cash,
            "allocation": cash if r["allocation"] is None else r["allocation"],
            "reset_minutes": None,
            "evidence": key,
            "route_tested_in_td1": r["route_tested_in_td1"],
        })
    return resources


RESOURCES = build_resources(CONFIG)


def td1(resource, family):
    return TD1_STATS[resource["evidence"]][family]


def rate(resource, family):
    s = td1(resource, family)
    return s["correct"] / s["cases"]


def failures(resource):
    return len(TD1_FAILED.get(resource["evidence"], ()))


def evidence_text(resource, family):
    s = td1(resource, family)
    text = f"{resource['id']} {s['correct']}/{s['cases']} on {family}"
    if s["correct_cells"]:
        text += f" (correct {', '.join(s['correct_cells'])}"
        text += f"; wrong {fmt_wrong(s['wrong'])}" if s["wrong"] else ""
        text += f"; {fmt_unavailable(s['unavailable'])}" if s["unavailable"] else ""
        text += ")"
    if not resource["route_tested_in_td1"]:
        text += ", evidence of the same model on its groq route, this route untested in TD 1"
    return text


def excluded_text(resources, family, difficulty):
    parts = []
    for r in resources:
        if r["level"] >= difficulty:
            continue
        s = td1(r, family)
        wrong = s["wrong"] or TD1_LEVELS[r["evidence"]][1]
        parts.append(f"{r['id']} level {r['level']} (wrong {fmt_wrong(wrong)})")
    return "; ".join(parts)


def panel_note(check, resources):
    """A quorum keeps its unavailable members in n: say how many votes are still needed."""
    for name, panel in CONFIG["panels"].items():
        if name in check:
            down = [r["id"] for r in resources if r["id"] in panel["members"] and not r["available"]]
            if down:
                return (f"{check} ({', '.join(down)} unavailable, stays in n = {len(panel['members'])}:"
                        f" k = {panel['k']} votes still needed among the others)")
    return check


def checks_for(fam, use, resource, family, resources):
    """The check of the request; 'none' only for a dashboard at 100 % on the family."""
    check = fam["checks"][use]
    if check == "none" and rate(resource, family) < 1:
        return panel_note(fam["checks"]["dashboard_if_not_100"], resources) + \
            f" (none refused: {resource['id']} below 100 % on {family} in TD 1)"
    if check == "none":
        return f"none (internal dashboard and {resource['id']} at 100 % on {family} in TD 1)"
    return panel_note(check, resources)


def unavailable_text(resources):
    down = [f"{r['id']} " + (f"refill announced in {r['reset_minutes']} min" if r["reset_minutes"]
                             else "no announced refill")
            for r in resources if not r["available"]]
    return f"unavailable: {'; '.join(down)}; " if down else ""


def choose(request, resources):
    """The kit policy, same branch order, with TD 1 evidence in every reason."""
    family = request["family"]
    fam = CONFIG["families"].get(family)
    if fam is None:
        return {"action": "abstain", "resource": None, "cash": 0, "checks": "human review",
                "reason": f"family {family} has no cell among C01 to C20: capability unknown "
                          "for every resource (not good, not bad); shadow test on real "
                          "questions before routing (Lecture 2, a new model arrives)"}
    difficulty = fam["level"]
    head = (f"{family} {fam['label']}, level {difficulty}, TD 1 cells {', '.join(fam['cases'])}")
    eligible = [r for r in resources if r["level"] >= difficulty]
    excluded = excluded_text(resources, family, difficulty)
    tail = f"; excluded: {excluded}" if excluded else ""

    down = unavailable_text(eligible)

    def decide(action, chosen, why, **extra):
        return {"action": action, "resource": chosen["id"], "cash": chosen["cash"] if action == "run" else 0,
                "checks": checks_for(fam, request["use"], chosen, family, resources),
                "reason": f"{head}: {evidence_text(chosen, family)}; {down}{why}{tail}", **extra}

    def rank(r):
        return (r["allocation"], -rate(r, family), r["level"], failures(r), r["id"])

    included = [r for r in eligible if r["available"] and r["cash"] == 0]
    if included:
        chosen = min(included, key=rank)
        return decide("run", chosen, "eligible included capacity, 0 USD")
    waiting = [r for r in eligible if not r["available"] and r["cash"] == 0
               and r["reset_minutes"] is not None
               and 0 < r["reset_minutes"] <= request["deadline_minutes"]]
    if waiting and request["can_wait"]:
        chosen = min(waiting, key=lambda r: (r["reset_minutes"], -rate(r, family), r["id"]))
        return decide("defer", chosen, "no eligible included capacity now; refill announced before "
                      "the deadline: recheck availability at wake-up",
                      wake_in_minutes=chosen["reset_minutes"])
    paid = [r for r in eligible if r["available"] and r["cash"] <= request["budget"]]
    if paid:
        chosen = min(paid, key=lambda r: (r["cash"], -rate(r, family), r["allocation"], r["id"]))
        return decide("run", chosen, f"available route within the authorised budget "
                      f"({chosen['cash']} <= {request['budget']} USD)")
    blocked = "; ".join(
        f"{r['id']} " + ("unavailable" if not r["available"] else f"{r['cash']} USD > budget {request['budget']}")
        for r in eligible)
    return {"action": "abstain", "resource": None, "cash": 0,
            "checks": f"nothing delivered (check required for {request['use']}: {fam['checks'][request['use']]})",
            "reason": f"{head}: no eligible resource within deadline and budget ({blocked}); "
                      f"never fall back in silence to a lower level{tail}"}


def scenarios():
    for sc in CONFIG["scenarios"]:
        resources = [dict(r, available=False, reset_minutes=sc["unavailable"][r["id"]])
                     if r["id"] in sc["unavailable"] else dict(r) for r in RESOURCES]
        yield sc, resources


def public_request(sc):
    req = dict(sc["request"])
    fam = CONFIG["families"].get(req["family"])
    req["difficulty"] = fam["level"] if fam else None
    return req


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", help="show only the named scenario")
    parser.add_argument("--markdown", action="store_true", help="print a Markdown table")
    args = parser.parse_args()
    found = False
    rows = []
    for sc, resources in scenarios():
        if args.scenario and sc["name"] != args.scenario:
            continue
        found = True
        result = choose(sc["request"], resources)
        if args.markdown:
            rows.append((sc, result))
        else:
            print(json.dumps({"scenario": sc["name"], "nature": "simulation", "policy": CONFIG["policy"],
                              "request": public_request(sc),
                              "unavailable": sc["unavailable"], "result": result}))
    if not found:
        parser.error("unknown scenario")
    if args.markdown:
        print("| Scenario | Request | Unavailable (refill, min) | Action | Resource | Cash USD | Check | Reason |")
        print("|---|---|---|---|---|---:|---|---|")
        for sc, res in rows:
            req = sc["request"]
            down = ", ".join(f"{k} ({v})" for k, v in sc["unavailable"].items()) or "none"
            action = res["action"] + (f", wake in {res['wake_in_minutes']} min" if "wake_in_minutes" in res else "")
            name = sc["name"] + (" *(added)*" if sc.get("added_by_pair_c") else "")
            print(f"| {name} | {req['family']}, {req['use']}, can_wait {req['can_wait']}, "
                  f"deadline {req['deadline_minutes']} min, budget {req['budget']} | {down} | {action} | "
                  f"{res['resource'] or '-'} | {res['cash']} | {res['checks']} | {res['reason']} |")


if __name__ == "__main__":
    main()
