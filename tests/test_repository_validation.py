"""Regression tests for citation format versus protocol version metadata."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CitationVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.citation_path = self.repo / "CITATION.cff"
        self.citation = self.citation_path.read_text()

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(self.repo / "tests/validate_repository.py")],
            capture_output=True, text=True,
        )

    def test_required_cff_version_passes_repository_validation(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("7 negative controls", result.stdout)

    def test_protocol_version_declarations_are_rejected(self):
        for declaration in ("version: 6.0", "Version: 6.0", "VERSION: 6.0",
                            "version : 6.0", "  version: 6.0"):
            with self.subTest(declaration=declaration):
                self.citation_path.write_text(self.citation + "\n" + declaration + "\n")
                result = self.run_validator()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("AssertionError", result.stderr)
                self.assertIn("CITATION.cff must not declare a protocol version", result.stderr)


if __name__ == "__main__":
    unittest.main()
