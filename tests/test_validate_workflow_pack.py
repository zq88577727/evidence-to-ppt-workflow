import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_workflow_pack.py"
SMOKE_INSTALL = ROOT / "scripts" / "smoke_install.py"
FIXTURES = ROOT / "tests" / "fixtures"


class WorkflowPackValidatorTest(unittest.TestCase):
    def run_validator(self, fixture_name):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / fixture_name)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def test_valid_pack_passes(self):
        result = self.run_validator("valid_pack")

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS workflow pack validation", result.stdout)
        self.assertIn("Credible A/B sources: 5", result.stdout)

    def test_accepted_claim_without_evidence_fails(self):
        result = self.run_validator("invalid_missing_evidence")

        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted", result.stdout)
        self.assertIn("empty Evidence", result.stdout)

    def test_unknown_source_id_fails(self):
        result = self.run_validator("invalid_unknown_source")

        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown source id S9", result.stdout)

    def test_low_credible_source_count_fails(self):
        result = self.run_validator("invalid_low_source_count")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Credible A/B sources: 4", result.stdout)
        self.assertIn("minimum required: 5", result.stdout)


class SmokeInstallTest(unittest.TestCase):
    def test_smoke_install_passes_when_required_skills_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            for skill_name in ["evidence-to-ppt-workflow", "gpt-researcher", "ppt-master"]:
                skill_dir = codex_home / "skills" / skill_name
                skill_dir.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text("# skill\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SMOKE_INSTALL), "--codex-home", str(codex_home)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS install smoke check", result.stdout)

    def test_smoke_install_reports_missing_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            skill_dir = codex_home / "skills" / "evidence-to-ppt-workflow"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("# skill\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SMOKE_INSTALL), "--codex-home", str(codex_home)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing skill", result.stdout)
        self.assertIn("gpt-researcher", result.stdout)


if __name__ == "__main__":
    unittest.main()
