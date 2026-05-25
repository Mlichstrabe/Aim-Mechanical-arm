import unittest

from src.project_paths import AIMTOOLS_CANONICAL, ROOT, SAMPLE_DIR, list_missing_aimtools, resolve_aimtools_dir


class ProjectPathsTests(unittest.TestCase):
    def test_root_contains_src_and_data(self):
        self.assertTrue((ROOT / "src").is_dir())
        self.assertTrue(SAMPLE_DIR.is_dir())

    def test_missing_aimtools_lists_expected_files_when_empty(self):
        missing = list_missing_aimtools()
        if not (resolve_aimtools_dir() / "PTM-4.aimtool").is_file():
            self.assertIn("PTM-4.aimtool", missing)


if __name__ == "__main__":
    unittest.main()
