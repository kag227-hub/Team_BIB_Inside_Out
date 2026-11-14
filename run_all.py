"""Rebuild the offline Checkpoint 2 dataset, summary, and dashboard data."""
import argparse
import csv
import hashlib
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = ("model_id", "persona_id", "scenario_id", "version")
VERSIONS = {"gain": 1, "loss": -1}


def load_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def keyed(rows, fields):
    result = {}
    for row in rows:
        key = tuple(row[field] for field in fields)
        if not all(key) or key in result:
            raise ValueError(f"Blank or duplicate key: {key}")
        result[key] = row
    return result


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(inputs, source):
    personas = keyed(load_csv(inputs / "personas_poc.csv"), ("persona_id",))
    scenarios = keyed(load_csv(inputs / "scenarios_poc.csv"), ("scenario_id",))
    models = keyed(load_csv(inputs / "models_poc.csv"), ("model_id",))
    raw = keyed(load_csv(source), KEY)
    expected = set(product((x[0] for x in models), (x[0] for x in personas),
                           (x[0] for x in scenarios), VERSIONS))
    if set(raw) != expected or not expected:
        raise ValueError(f"Design mismatch: {len(expected - raw.keys())} missing, "
                         f"{len(raw.keys() - expected)} unexpected")
    rows = []
    kinds, run_ids = set(), set()
    for key in sorted(expected):
        model, persona, scenario, version = key
        p, s, r = personas[(persona,)], scenarios[(scenario,)], raw[key]
        kind = r["source_kind"]
        if kind not in ("synthetic", "collected"):
            raise ValueError(f"Unknown provenance at {key}")
        kinds.add(kind)
        run_ids.add(r["run_id"])
        sign_return = VERSIONS[version] * int(s["abs_return_pct"])
        if int(r["signed_return_pct"]) != sign_return:
            raise ValueError(f"Incorrect signed return at {key}")
        answer, rating = r["decision"].strip(), r["rating"].strip()
        sell = {"Sell": 1, "Hold": 0}.get(answer)
        rating_value = int(rating) if rating in "1 2 3 4 5 6 7".split() else None
        rows.append(dict(zip(KEY, key)) | {
            "run_id": r["run_id"], "source_kind": kind, "emotion": p["emotion"],
            "background": p["background"], "arm": p["prompt_arm"],
            "company": s["company"], "holding_period": s["holding_period"],
            "signed_return_pct": sign_return, "decision_raw": answer,
            "sell": sell, "rating_raw": rating, "rating": rating_value,
        })
    if len(kinds) != 1 or len(run_ids) != 1 or "" in run_ids:
        raise ValueError("Provide exactly one labeled run and one source type")
    by_pair = {}
    for r in rows:
        key = tuple(r[k] for k in KEY[:-1])
        by_pair.setdefault(key, {})[r["version"]] = r
    groups = {}
    for (model, persona, _), sides in by_pair.items():
        p = personas[(persona,)]
        groups.setdefault((model, p["emotion"], p["prompt_arm"]), []).append(sides)
    summary = []
    for (model, emotion, arm), pairs in sorted(groups.items()):
        valid = [p for p in pairs if all(r["sell"] is not None for r in p.values())]
        rated = [p for p in pairs if all(r["rating"] is not None for r in p.values())]
        n = len(valid)
        g, l = [sum(p[v]["sell"] for p in valid) for v in VERSIONS]
        summary.append(dict(model_id=model, emotion=emotion, arm=arm,
                            expected_pairs=len(pairs), complete_pairs=n,
                            gain_sells=g, loss_sells=l,
                            gain_sell_rate=g/n if n else None,
                            loss_sell_rate=l/n if n else None,
                            gap_pp=round(100*(g-l)/n, 2) if n else None,
                            complete_rating_pairs=len(rated),
                            rating_gap=round(sum(p["gain"]["rating"]-p["loss"]["rating"]
                                                 for p in rated)/len(rated), 2) if rated else None))
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses", type=Path, default=ROOT / "inputs/v0_responses.csv")
    args = parser.parse_args()
    inputs, outputs = ROOT / "inputs", ROOT / "outputs"
    rows, summary = build(inputs, args.responses)
    outputs.mkdir(exist_ok=True)
    write_csv(outputs / "v0_dataset.csv", rows)
    write_csv(outputs / "v0_sell_rates.csv", summary)
    payload = {
        "source_kind": rows[0]["source_kind"], "run_id": rows[0]["run_id"],
        "input_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [args.responses, *(inputs / (name + "_poc.csv")
                       for name in ("personas", "scenarios", "models"))]
        },
        "summary": summary, "rows": rows,
    }
    (outputs / "v0_dashboard.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"{len(rows)} {payload['source_kind']} rows; "
          f"{sum(r['complete_pairs'] for r in summary)} complete decision pairs")


if __name__ == "__main__":
    main()
