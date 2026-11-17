"""The public behavioral results must rebuild from saved paid answers."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from build_dataset import tidy_from_raw
from export_public_pilot import export


class PaidExportChecks(unittest.TestCase):
    def test_saved_paid_answers_reproduce_public_export(self):
        expected = ROOT / "outputs" / "public_paid_pilot.json"
        run_id = json.loads(expected.read_text(encoding="utf-8"))["run_id"]
        folder = ROOT / "data" / "raw" / run_id
        manifest = json.loads((folder / "manifest.json").read_text())
        raw_path = folder / "raw_results.csv"
        self.assertEqual(hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                         manifest["committed_csv_sha256"])
        self.assertFalse(manifest["is_test"])
        raw = pd.read_csv(raw_path)
        self.assertEqual(len(raw), manifest["n_observations"])
        prompts = pd.read_csv(folder / "prompts.csv")
        pd.testing.assert_frame_equal(prompts, raw[prompts.columns])
        tidy = tidy_from_raw(raw, run_id, False, manifest["started_utc"])
        with tempfile.TemporaryDirectory() as tmp:
            source, dest = Path(tmp) / "responses.csv", Path(tmp) / "public.json"
            tidy.to_csv(source, index=False)
            export(source, dest)
            self.assertEqual(dest.read_bytes(), expected.read_bytes())
