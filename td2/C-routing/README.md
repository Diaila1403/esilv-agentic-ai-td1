# TD 2 · Pair C · Step 3: the routing rule

**Members:** Jean VASSEUR, Lina ZAAG · **Session:** 18 November 2026 · **Pack:** 2026-11-18-students-5
**Report section:** [`reports/td2.md`, Step 3](../../reports/td2.md#step-3--the-routing-rule-pair-c) · **One-page rule:** [`routing-rule-en.md`](routing-rule-en.md)

## What we did

1. Computed by code, from the 104 real calls of [`traces-td1.csv`](../../td1/traces-td1.csv), the exact TD 1 rate (correct / cases) of each model on each question family, and derived each model's eligibility level (highest level with no wrong value).
2. Wrote the one-page routing rule: per family, the cells and rates that justify it, the first model called, the check for three uses (internal dashboard, figure shown to a customer, amount paid out) and the course of action when the first model is unavailable.
3. Ran the kit simulator unchanged (before), then adapted `RESOURCES` and `choose` to our rule (after): our six portfolio routes, levels computed from TD 1, the check following the request to the fallback route, TD 1 cells in every reason.
4. Explained, and executed, why the kit `choose` runs an available subscription before deferring to an exhausted free resource, and when that priority should be reversed.

## Files

| File | Content |
|---|---|
| [`routing-rule-en.md`](routing-rule-en.md) | The one-page rule (kit worksheet format) |
| [`routing-config.json`](routing-config.json) | Families, levels, uses, checks, vote panels, resources with prices and sources, scenarios: everything the code reads |
| [`td1_families.py`](td1_families.py) | Rates per family, eligibility levels, quorum cross-check, from the traces |
| [`family-rates-td1.csv`](family-rates-td1.csv) | Its output: one row per family and model, with the cells |
| [`atelier-routage-kit.py`](atelier-routage-kit.py) | Kit simulator, byte-identical (SHA-256 `2971555aff39dede9e1a315ebb00d92d7b5c5f2eaf158199730fcc2c1839e28d`) |
| [`atelier-routage.py`](atelier-routage.py) | Simulator adapted to our rule |
| [`priority_demo.py`](priority_demo.py) | Kit `choose` on the priority question, and the reversed variant |
| [`outputs/`](outputs/) | `simulator-before.jsonl`, `simulator-after.jsonl`, `priority-demo.jsonl` |

## Replay (from the repository root, Python 3 standard library, no key, no network)

```bash
python3 td2/C-routing/td1_families.py --csv td2/C-routing/family-rates-td1.csv
python3 td2/C-routing/atelier-routage-kit.py      # before: the seven kit scenarios
python3 td2/C-routing/atelier-routage.py          # after: our rule, seven kit scenarios + five added
python3 td2/C-routing/atelier-routage.py --scenario deferrable
python3 td2/C-routing/priority_demo.py
```

Each command regenerates its file in `outputs/` byte for byte (checked on 18 November 2026).

## Main results

- All 16 wrong values of TD 1 are on families with an age condition; no model returned a wrong value on F1 (period) or F3 (product list).
- Levels from TD 1: gpt-oss-120b 3 (20/20), gpt-oss-20b 2 (capped by C02, C11), qwen3.8-27b 2 (C09, C15, C19), north-mini-code:free 1 (C10), dots-3-note-preview:free 1 (C10, C18).
- First model: dots-3 on F1 and F3, gpt-oss-20b on F2b and F1+F2b, gpt-oss-120b on F2 and its combinations: all free, the lowest sufficient level first, so the gpt-oss-120b quota is kept for the families only it solves.
- Check on age families: the reference query, not a quorum. On C09 the fixed 2-of-3 panel keeps the shared wrong value 0 of north-mini-code and qwen (reference 487980), and the 3-of-5 quorum abstains.
- Our independent count of the 2-of-3 and 3-of-5 decisions agrees with Pair A's `comparaison-votes.csv` on all twenty questions.

## Reviews received

[`review-1.md`](review-1.md) by Pair A and [`review-2.md`](review-2.md) by Pair B, to write (each file already holds the outline of a review).
