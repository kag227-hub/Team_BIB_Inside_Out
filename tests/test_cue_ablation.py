"""Offline checks for the demand-cue ablation (instructor audit A3)."""
from pathlib import Path
import sys
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from build_dataset import tidy_from_raw  # noqa: E402
from cue_ablation import pair_diffs, summarize  # noqa: E402
from poc_run import PAST_MOVES_CLAUSE, build_agents, build_scenarios  # noqa: E402

SCEN = pd.read_csv(ROOT / "inputs" / "scenarios_poc.csv")
PERSONAS = pd.read_csv(ROOT / "inputs" / "personas_poc.csv")
SYSTEM_LINE = "Do not break character"


class ScenarioCueChecks(unittest.TestCase):
    def test_default_scenarios_unchanged_by_ablation_code(self):
        rows = pd.DataFrame(build_scenarios(SCEN))
        self.assertTrue(rows["scenario_text"].str.contains(PAST_MOVES_CLAUSE, regex=False).all())
        committed = pd.read_csv(ROOT / "data/raw/poc_TEST_v0/raw_results.csv")
        self.assertEqual(set(rows["prompt_hash"]), set(committed["scenario.prompt_hash"]))

    def test_cue_removes_only_the_clause_and_keeps_option_order(self):
        rows = pd.DataFrame(build_scenarios(SCEN, past_moves_levels=[1, 0]))
        on = rows[rows.cue_past_moves.eq(1)].set_index(["scenario_id", "version"])
        off = rows[rows.cue_past_moves.eq(0)].set_index(["scenario_id", "version"])
        self.assertEqual(len(on), len(off))
        for k in on.index:
            self.assertEqual(on.loc[k, "scenario_text"].replace(PAST_MOVES_CLAUSE, ""),
                             off.loc[k, "scenario_text"])
            self.assertEqual(on.loc[k, "decision_options"], off.loc[k, "decision_options"])


class SystemLineChecks(unittest.TestCase):
    def test_agents_override_edsl_instruction_only_when_cue_is_off(self):
        agents = build_agents(PERSONAS.head(1), system_line_levels=[1, 0])
        by_cue = {a.traits["cue_system_line"]: a for a in agents}
        self.assertIn(SYSTEM_LINE, by_cue[1].instruction)
        self.assertEqual(by_cue[0].instruction, "")

    def test_committed_dry_run_prompts_match_cue_cells(self):
        p = pd.read_csv(ROOT / "data/raw/poc_TEST_ablation_v0/prompts.csv")
        self.assertEqual(len(p.groupby(["agent.cue_system_line", "scenario.cue_past_moves"])), 4)
        for col in ("prompt.decision_system_prompt", "prompt.sell_rating_system_prompt"):
            has_line = p[col].fillna("").str.contains(SYSTEM_LINE)
            self.assertTrue((has_line == p["agent.cue_system_line"].eq(1)).all())
        has_clause = p["prompt.decision_user_prompt"].str.contains(PAST_MOVES_CLAUSE, regex=False)
        self.assertTrue((has_clause == p["scenario.cue_past_moves"].eq(1)).all())


class AnalysisChecks(unittest.TestCase):
    def test_old_runs_default_to_both_cues_on(self):
        raw = pd.read_csv(ROOT / "data/raw/poc_TEST_v0/raw_results.csv")
        tidy = tidy_from_raw(raw, "poc_TEST_v0", True, "t")
        self.assertTrue(tidy["cue_past_moves"].eq(1).all() and tidy["cue_system_line"].eq(1).all())

    def test_contrasts(self):
        # One persona, 3 scenarios. Removing the past-moves sentence turns "hold both" (DE 0) into
        # "sell gain, hold loss" (DE +100); the system line does nothing.
        rows = []
        for s in ["s01", "s02", "s03"]:
            for past in (1, 0):
                for sys_ in (1, 0):
                    for version in ("gain", "loss"):
                        sell = 1 if (past == 0 and version == "gain") else 0
                        rows.append(dict(model_id="m", persona_id="p", scenario_id=s, repeat=0,
                                         cue_past_moves=past, cue_system_line=sys_,
                                         version=version, sell=sell, sell_valid=True))
        out = summarize(pair_diffs(pd.DataFrame(rows)))
        est = out[out.persona_id.eq("p")].set_index("estimate")
        self.assertEqual(est.loc["remove_past_moves", "value_pp"], 100)
        self.assertEqual(est.loc["remove_system_line", "value_pp"], 0)
        self.assertEqual(est.loc["interaction", "value_pp"], 0)
        self.assertEqual(est.loc["DE_both_cues", "value_pp"], 0)
        self.assertEqual(est.loc["DE_no_cues", "value_pp"], 100)
        self.assertEqual(est.loc["remove_past_moves", "n_scenarios"], 3)


if __name__ == "__main__":
    unittest.main()
