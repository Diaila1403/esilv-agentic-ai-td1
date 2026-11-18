import sys
import csv
import importlib.util
from pathlib import Path
from types import SimpleNamespace

# Files
TRACES = Path("traces-td1.csv")
REFERENCES = Path("reference-td1.csv")

# Fixed panel from atelier-vote.py
PANEL_3 = [
    ("groq", "openai/gpt-oss-120b"),
    ("openrouter", "cohere/north-mini-code:free"),
    ("groq", "qwen/qwen3.8-27b"),
]

# Load the vote method already implemented
KIT = Path.home() / "Downloads/esilv-student-2026-10-18/kit-td1"
spec = importlib.util.spec_from_file_location(
    "student_skeleton", KIT / "skeleton-multi-llm-en.py"
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

vote = lambda proposals, k: module.Orchestrateur.vote_k_sur_n(
    None, proposals, k
)

# Read the CSV files
with TRACES.open(encoding="utf-8", newline="") as f:
    traces = list(csv.DictReader(f))

with REFERENCES.open(encoding="utf-8", newline="") as f:
    references = {
        row["case_id"]: int(row["revenue_cents"])
        for row in csv.DictReader(f)
    }

# Keep the five models from the TD1 traces
models = list(dict.fromkeys(
    (row["provider"], row["model_requested"])
    for row in traces if row["nature"] == "real"
))

if len(models) != 5:
    raise ValueError("Expected exactly five models")

results = []

for case in sorted(references):
    # Last attempt per model and question
    latest = {}
    for row in traces:
        if row["case_id"] == case and row["nature"] == "real":
            key = (row["provider"], row["model_requested"])
            latest[key] = row

    def make_proposals(panel):
        proposals = []
        for provider, model in panel:
            row = latest.get((provider, model), {})
            value = row.get("value", "")
            valid = (
                row.get("verdict") in {"correct", "incorrect"}
                and value not in ("", None)
            )
            proposals.append(SimpleNamespace(
                provider=provider,
                model_requested=model,
                value=int(value) if valid else None,
                verdict="executed" if valid else "error"
            ))
        return proposals

    result_3 = vote(make_proposals(PANEL_3), 2)
    result_5 = vote(make_proposals(models), 3)

    reference = references[case]

    results.append({
        "case": case,
        "reference": reference,
        "2_of_3_consensus": result_3["consensus"],
        "2_of_3_value": result_3["value"],
        "2_of_3_votes": result_3["votes"],
        "2_of_3_correct": (
            result_3["value"] == reference
            if result_3["consensus"] else None
        ),
        "3_of_5_consensus": result_5["consensus"],
        "3_of_5_value": result_5["value"],
        "3_of_5_votes": result_5["votes"],
        "3_of_5_correct": (
            result_5["value"] == reference
            if result_5["consensus"] else None
        ),
        "decision_changed": (
            result_3["consensus"] != result_5["consensus"]
            or result_3["value"] != result_5["value"]
        )
    })

# Save the comparison
output = Path("comparaison-votes.csv")
with output.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Questions evaluated:", len(results))
print("Decisions changed:", sum(r["decision_changed"] for r in results))
print("Comparison saved to:", output)

for row in results:
    print(
        row["case"],
        "| 2/3:", row["2_of_3_value"],
        "| 3/5:", row["3_of_5_value"],
        "| changed:", row["decision_changed"]
    )

