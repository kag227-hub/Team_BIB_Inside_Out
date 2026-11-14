"""Offline checks for the raw -> tidy step (code/build_dataset.py)."""
from pathlib import Path
import sys
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from build_dataset import HOLD, SELL, tidy_from_raw  # noqa: E402


def raw_rows(decisions, ratings):
    rows = []
    for i, (d, r) in enumerate(zip(decisions, ratings)):
        rows.append({"agent.persona_id": "p", "agent.emotion": "Joy", "agent.background": "mid",
                     "agent.prompt_arm": "character_name", "agent.is_control": 0,
                     "scenario.scenario_id": f"s{i // 2}", "scenario.version": ["gain", "loss"][i % 2],
                     "scenario.signed_return_pct": 5.0, "scenario.abs_return_pct": 5,
                     "scenario.prompt_hash": "h", "model.model": "m", "answer.decision": d,
                     "comment.decision_comment": "", "answer.sell_rating": r,
                     "scenario.decision_options": str([SELL, HOLD])})
    return pd.DataFrame(rows)


class BuildDatasetChecks(unittest.TestCase):
    def test_invalid_answers_never_become_hold(self):
        tidy = tidy_from_raw(raw_rows([SELL, "I refuse", HOLD, None], [7, 9, "4", 2.5]), "r", False, "t")
        self.assertEqual(tidy["sell"].tolist()[0], 1)
        self.assertTrue(pd.isna(tidy["sell"].iloc[1]))
        self.assertTrue(pd.isna(tidy["sell"].iloc[3]))
        self.assertEqual(tidy["sell_valid"].tolist(), [True, False, True, False])
        self.assertEqual(tidy["rating_valid"].tolist(), [True, False, True, False])
        self.assertEqual(tidy["option_order"].iloc[0], f"{SELL}|{HOLD}")

    def test_duplicate_keys_are_rejected(self):
        raw = raw_rows([SELL, HOLD], [5, 5])
        with self.assertRaises(AssertionError):
            tidy_from_raw(pd.concat([raw, raw]), "r", False, "t")

    def test_committed_run_rebuilds_with_expected_rows(self):
        for run in (ROOT / "data" / "raw").iterdir():
            if (run / "raw_results.csv").exists():
                raw = pd.read_csv(run / "raw_results.csv")
                tidy = tidy_from_raw(raw, run.name, True, "t")
                self.assertEqual(len(tidy), len(raw))


if __name__ == "__main__":
    unittest.main()
