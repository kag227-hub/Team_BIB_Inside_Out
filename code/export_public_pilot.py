"""Export only cell-level sell counts from a locally rebuilt paid pilot."""
import argparse
import json
from pathlib import Path

import pandas as pd


def export(source: Path, dest: Path):
    cols = ["run_id", "is_test", "model_id", "persona_id", "scenario_id",
            "repeat", "version", "emotion", "prompt_arm", "sell"]
    df = pd.read_csv(source, usecols=cols)
    if df.empty or not df["is_test"].eq(False).all() or df.run_id.nunique() != 1:
        raise ValueError("Expected one non-synthetic pilot run")
    ids = ["model_id", "emotion", "prompt_arm", "persona_id", "scenario_id", "repeat"]
    if df[ids + ["version"]].isna().any().any() or set(df.version) != {"gain", "loss"}:
        raise ValueError("Missing IDs or unexpected gain/loss versions")
    if not df.sell.dropna().isin([0, 1]).all():
        raise ValueError("Unexpected parsed sell value")
    pairs = df.pivot(index=ids, columns="version", values="sell").dropna()
    cells = df[ids[:3]].drop_duplicates().sort_values(ids[:3])
    counts = pairs.groupby(level=ids[:3]).agg(
        complete_pairs=("gain", "size"), gain_sells=("gain", "sum"), loss_sells=("loss", "sum"))
    table = cells.merge(counts, on=ids[:3], how="left", validate="one_to_one")
    for col in ["complete_pairs", "gain_sells", "loss_sells"]:
        table[col] = table[col].fillna(0).astype(int)
    payload = {"run_id": str(df.run_id.iloc[0]), "source": "paid_model_pilot",
               "observations": len(df), "cells": table.to_dict("records")}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export(args.source, args.destination)
