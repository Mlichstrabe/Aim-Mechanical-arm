import unittest
from pathlib import Path

from src.project_paths import (
    AIMOOE_OUTPUT_DIR,
    HAND_EYE_DIR,
    LEGACY_DATATIMO_DIR,
    ROOT,
    legacy_datatimo_dir,
    resolve_aimtools_dir,
)


class RestructureCompatTests(unittest.TestCase):
    def test_root_launchers_exist(self):
        for name in ("Init.py", "Demo.py", "demo1.py", "Aimooe_timo.py", "CollectedToolData.py"):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_legacy_datatimo_maps_to_outputs(self):
        self.assertEqual(legacy_datatimo_dir(), AIMOOE_OUTPUT_DIR)

    def test_hand_eye_experiment_dirs_defined(self):
        self.assertEqual(HAND_EYE_DIR, ROOT / "data" / "experiments" / "hand_eye")

    def test_resolve_aimtools_prefers_canonical_dir(self):
        self.assertIn(resolve_aimtools_dir().name.lower(), ("aimtools",))


class MigrationScriptTests(unittest.TestCase):
    def test_migrate_dry_run_returns_list(self):
        from src.project_paths import migrate_legacy_layout

        result = migrate_legacy_layout(dry_run=True)
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
