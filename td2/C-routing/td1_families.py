#!/usr/bin/env python3
"""TD 2, Step 3 (Pair C): exact TD 1 accuracy per question family.

No network call, no key. Reads the stored TD 1 traces (traces-td1.csv) and the
family definitions of routing-config.json, keeps the last attempt of each
model x question cell, then gives for each family and each model:

- the correct / cases ratio and the cells behind it;
- the wrong values (verdict incorrect) and the availability failures
  (access_error, not_executed), kept apart: a wrong value is a capability
  failure, an HTTP 401 or 429 is an availability failure;
- the eligibility level of each model used by atelier-routage.py: the highest
  level L such that the model returned no wrong value on any cell of the
  families of level <= L, with at least one correct cell per family;
- as a cross-check, what three vote panels would have decided on the cells of
  the family (strict majority, an unavailable member stays in n). The official
  vote is Pair A's vote_k_sur_n; both counts must agree at the cross-review.

Usage, from the repository root:
    python3 td2/C-routing/td1_families.py               # Markdown tables for the report
    python3 td2/C-routing/td1_families.py --csv td2/C-routing/family-rates-td1.csv
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # repository root, two levels above td2/C-routing/
DEFAULT_CONFIG = HERE / "routing-config.json"


def load_config(path=DEFAULT_CONFIG):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def traces_path(config, override=None):
    return Path(override) if override else ROOT / config["traces"]


def last_attempts(path):
    """Return {(provider, model_requested, case_id): row}, keeping the last attempt."""
    cells = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["provider"], row["model_requested"], row["case_id"])
            rank = (int(row["attempts"] or 0), row["date_utc"])
            if key not in cells or rank >= cells[key][0]:
                cells[key] = (rank, row)
    return {key: rank_row[1] for key, rank_row in cells.items()}


def failed_attempt_cells(path):
    """Cells with at least one attempt that returned no value (HTTP 401, 429...)."""
    failed = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["verdict"] in ("access_error", "not_executed"):
                key = (row["provider"], row["model_requested"])
                failed.setdefault(key, set()).add(row["case_id"])
    return failed


def as_int(text):
    return int(text) if text not in (None, "") else None


def evidence_key(resource):
    ev = resource["td1_evidence"]
    return (ev["provider"], ev["model_requested"])


def family_stats(cells, config):
    """{(provider, model): {family: stats}} for every model found in the traces."""
    models = sorted({(p, m) for (p, m, _case) in cells})
    stats = {}
    for model_key in models:
        per_family = {}
        for fam_id, fam in config["families"].items():
            correct, wrong, unavailable, missing = [], [], [], []
            for case in fam["cases"]:
                row = cells.get((*model_key, case))
                if row is None:
                    missing.append(case)
                elif row["verdict"] == "correct":
                    correct.append(case)
                elif row["verdict"] == "incorrect":
                    wrong.append((case, as_int(row["value"]), as_int(row["reference"])))
                else:
                    unavailable.append((case, row["verdict"], row["http_status"]))
            per_family[fam_id] = {
                "cases": len(fam["cases"]),
                "correct": len(correct),
                "correct_cells": correct,
                "wrong": wrong,
                "unavailable": unavailable,
                "missing": missing,
            }
        stats[model_key] = per_family
    return stats


def eligibility_level(per_family, config):
    """Highest level L with no wrong value on families of level <= L.

    Returns (level, capping): capping lists the wrong cells that stop the model
    at the next level, so that a decision can cite them.
    """
    levels = sorted({fam["level"] for fam in config["families"].values()})
    reached = 0
    for level in levels:
        fams = [f for f, d in config["families"].items() if d["level"] == level]
        wrong = [w for f in fams for w in per_family[f]["wrong"]]
        no_evidence = [f for f in fams if per_family[f]["correct"] == 0]
        if wrong or no_evidence:
            return reached, wrong
        reached = level
    return reached, []


def vote(values, k):
    """Strict-majority count used only as a cross-check of Pair A's method."""
    counts = Counter(v for v in values if v is not None)
    if not counts:
        return "abstain", None, 0
    value, votes = counts.most_common(1)[0]
    return ("consensus", value, votes) if votes >= k else ("abstain", None, votes)


def panel_outcomes(cells, config, resources_by_id):
    """{panel: {family: Counter(correct consensus / wrong consensus / abstain)}}."""
    out = {}
    for name, panel in config["panels"].items():
        per_family = {}
        for fam_id, fam in config["families"].items():
            tally = Counter()
            details = []
            for case in fam["cases"]:
                values, reference = [], None
                for member in panel["members"]:
                    row = cells.get((*evidence_key(resources_by_id[member]), case))
                    executed = row is not None and row["verdict"] in ("correct", "incorrect")
                    values.append(as_int(row["value"]) if executed else None)
                    if row is not None:
                        reference = as_int(row["reference"])
                decision, value, votes = vote(values, panel["k"])
                if decision == "abstain":
                    label = "abstain"
                elif value == reference:
                    label = "correct consensus"
                else:
                    label = "WRONG consensus"
                tally[label] += 1
                details.append((case, label, value, votes, values, reference))
            per_family[fam_id] = (tally, details)
        out[name] = per_family
    return out


def short(model_key):
    return model_key[1].split("/")[-1]


def fmt_wrong(wrong):
    return ", ".join(f"{case}={value}" for case, value, _ref in wrong)


def fmt_unavailable(unavailable):
    return ", ".join(f"{case} HTTP {http}" for case, _verdict, http in unavailable)


def markdown(config, stats, levels, panels):
    fams = list(config["families"])
    models = list(stats)
    lines = ["### Exact TD 1 rate per family (last attempt of each cell, correct / cases)", ""]
    lines.append("| Family | Level | Cells | " + " | ".join(short(m) for m in models) + " |")
    lines.append("|---|---:|---|" + "---|" * len(models))
    for fam_id in fams:
        fam = config["families"][fam_id]
        row = [f"{fam_id} {fam['label']}", str(fam["level"]), ", ".join(fam["cases"])]
        for m in models:
            s = stats[m][fam_id]
            cell = f"{s['correct']}/{s['cases']}"
            notes = []
            if s["wrong"]:
                notes.append("wrong " + fmt_wrong(s["wrong"]))
            if s["unavailable"]:
                notes.append(fmt_unavailable(s["unavailable"]))
            row.append(cell + (f" ({'; '.join(notes)})" if notes else ""))
        lines.append("| " + " | ".join(row) + " |")
    totals = []
    for m in models:
        c = sum(stats[m][f]["correct"] for f in fams)
        n = sum(stats[m][f]["cases"] for f in fams)
        totals.append(f"**{c}/{n}**")
    lines.append("| **All** | | C01 to C20 | " + " | ".join(totals) + " |")
    lines += ["", "### Eligibility level derived from TD 1", "",
              "| Model | Level | Wrong cells that cap the level |", "|---|---:|---|"]
    for m in models:
        level, capping = levels[m]
        lines.append(f"| {short(m)} | {level} | {fmt_wrong(capping) or 'none: 20/20'} |")
    lines += ["", "### Cross-check: what each panel would have decided on the family cells", "",
              "| Family | " + " | ".join(f"{p} (k={config['panels'][p]['k']})" for p in panels) + " |",
              "|---|" + "---|" * len(panels)]
    for fam_id in fams:
        row = [fam_id]
        for p in panels:
            tally, details = panels[p][fam_id]
            text = ", ".join(f"{n} {label}" for label, n in sorted(tally.items()))
            wrong = [f"{c}: {v} with {votes} votes" for c, label, v, votes, _vals, _ref in details
                     if label == "WRONG consensus"]
            row.append(text + (f" ({'; '.join(wrong)})" if wrong else ""))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def write_csv(path, config, stats, levels):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["family", "label", "level", "cells", "provider", "model", "correct",
                         "cases", "rate", "correct_cells", "wrong_cells", "unavailable_cells",
                         "model_eligibility_level", "nature"])
        for (provider, model), per_family in stats.items():
            for fam_id, s in per_family.items():
                fam = config["families"][fam_id]
                writer.writerow([fam_id, fam["label"], fam["level"], " ".join(fam["cases"]),
                                 provider, model, s["correct"], s["cases"],
                                 f"{s['correct'] / s['cases']:.2f}", " ".join(s["correct_cells"]),
                                 fmt_wrong(s["wrong"]), fmt_unavailable(s["unavailable"]),
                                 levels[(provider, model)][0], "real TD 1 traces"])


def analyse(config_path=DEFAULT_CONFIG, traces=None):
    config = load_config(config_path)
    path = traces_path(config, traces)
    cells = last_attempts(path)
    stats = family_stats(cells, config)
    levels = {m: eligibility_level(per_family, config) for m, per_family in stats.items()}
    resources_by_id = {r["id"]: r for r in config["resources"]}
    panels = panel_outcomes(cells, config, resources_by_id)
    return config, cells, stats, levels, panels, failed_attempt_cells(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--traces", help="default: the traces file named in the config")
    parser.add_argument("--csv", help="also write the long table to this CSV file")
    args = parser.parse_args()
    config, _cells, stats, levels, panels, _failed = analyse(args.config, args.traces)
    covered = sorted(c for fam in config["families"].values() for c in fam["cases"])
    expected = [f"C{i:02d}" for i in range(1, 21)]
    if covered != expected:
        parser.error(f"families must cover C01 to C20 exactly once, got {covered}")
    print(markdown(config, stats, levels, panels))
    if args.csv:
        write_csv(args.csv, config, stats, levels)


if __name__ == "__main__":
    main()
