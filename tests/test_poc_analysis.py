"""Offline regression checks for paired estimates and cost provenance."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class AnalysisChecks(unittest.TestCase):
    def run_analysis(self, is_test=False, include_cost=True, two_models=False):
        (ROOT / "outputs").mkdir(exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=ROOT / "outputs")
        assert (ROOT / "outputs").resolve() in Path(temp.name).resolve().parents
        self.addCleanup(temp.cleanup)
        out = Path(temp.name)
        rows = []
        for scenario, gain, loss in [("s01", 1, 0), ("s02", 0, None)]:
            for version, sell in [("gain", gain), ("loss", loss)]:
                row = dict(run_id="fixture", persona_id="p", scenario_id=scenario,
                           version=version, model_id="fixture_model", repeat=0,
                           emotion="Joy", prompt_arm="character_name", sell=sell,
                           sell_valid=sell is not None, rating_valid=True,
                           decision_comment="", decision_raw="fixture",
                           sell_rating_raw=4, sell_rating=4)
                if include_cost:
                    row["raw_model_response__decision_cost"] = 0.01
                    row["cache_used__decision_cache_used"] = True
                rows.append(row)
        if two_models:
            rows += [dict(row, model_id="second_model") for row in list(rows)]
        path = out / "fixture_responses.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        # No input manifest: test the explicitly observed two-pair fixture.
        if is_test:
            path = out / "poc_TEST_fixture_responses.csv"
            pd.DataFrame(rows).to_csv(path, index=False)
        result = subprocess.run([sys.executable, str(ROOT / "code/poc_analyze.py"), str(path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        stem = path.name.replace("_responses.csv", "")
        rates = pd.read_csv(out / f"{stem}_rates.csv")
        costs = pd.read_csv(out / f"{stem}_cost_projection.csv")
        return rates, costs, result.stdout

    def test_complete_pairs_only_and_cached_cost(self):
        rates, costs, report = self.run_analysis()
        self.assertEqual(rates.disposition_effect_pp.iloc[0], 100)
        self.assertEqual(rates.n_gain.iloc[0], 1)
        self.assertIn("Incomplete pairs: 1", report)
        self.assertEqual(costs.total_cost_usd.iloc[0], 0)
        self.assertTrue(pd.isna(costs.cost_per_obs_usd.iloc[0]))

    def test_missing_cost_is_unknown(self):
        _, costs, _ = self.run_analysis(include_cost=False)
        self.assertTrue(pd.isna(costs.total_cost_usd.iloc[0]))

    def test_synthetic_cost_has_no_projection(self):
        _, costs, report = self.run_analysis(is_test=True)
        self.assertEqual(costs.total_cost_usd.iloc[0], 0)
        self.assertTrue(pd.isna(costs.proj_full_36000_usd.iloc[0]))
        self.assertIn("SYNTHETIC", report)

    def test_handcheck_is_a_pair_from_one_model(self):
        _, _, report = self.run_analysis(two_models=True)
        handcheck = report.split("## 6. Hand-check pair", 1)[1]
        self.assertIn("gain", handcheck)
        self.assertIn("loss", handcheck)
        self.assertNotIn("second_model", handcheck)


if __name__ == "__main__":
    unittest.main()
