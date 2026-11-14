import csv
import tempfile
import unittest

from run_all import ROOT, build, load_csv, write_csv


class Checkpoint2(unittest.TestCase):
    def setUp(self):
        self.inputs = ROOT / "inputs"
        self.fixture = self.inputs / "v0_responses.csv"

    def test_counts_and_hand_calculated_cell(self):
        rows, summary = build(self.inputs, self.fixture)
        self.assertEqual(len(rows), 108)
        self.assertEqual(sum(r["complete_pairs"] for r in summary), 54)
        joy = next(s for s in summary if (s["model_id"], s["emotion"], s["arm"]) ==
                   ("gpt-5.6-luna", "Joy", "character_name"))
        # Fixture rows for joy_mid_name: gain choices Hold/Hold/Sell;
        # loss choices Hold/Hold/Hold. The independently counted gap is 1/3.
        self.assertEqual((joy["gain_sells"], joy["loss_sells"], joy["gap_pp"]),
                         (1, 0, 33.33))

    def test_missing_and_duplicate_rows_fail_loudly(self):
        rows = load_csv(self.fixture)
        with tempfile.TemporaryDirectory(dir=ROOT / "outputs") as d:
            path = ROOT / "outputs" / d / "responses.csv"
            for bad, message in [(rows[1:], "1 missing"), (rows + rows[:1], "duplicate")]:
                write_csv(path, bad)
                with self.assertRaisesRegex(ValueError, message):
                    build(self.inputs, path)

    def test_invalid_answer_removes_whole_decision_pair_only(self):
        rows = load_csv(self.fixture)
        rows[0]["decision"] = "Unknown"
        with tempfile.TemporaryDirectory(dir=ROOT / "outputs") as d:
            path = ROOT / "outputs" / d / "responses.csv"
            write_csv(path, rows)
            _, summary = build(self.inputs, path)
        self.assertEqual(sum(r["complete_pairs"] for r in summary), 53)
        self.assertEqual(sum(r["complete_rating_pairs"] for r in summary), 54)
