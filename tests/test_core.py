import unittest
from pathlib import Path
import tempfile
import shutil
import sys
import os

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from autoharness.config import Config
from autoharness.skill_store import SkillStore
from autoharness.ledger import Ledger
from autoharness.reflector import Reflector

class TestAutoHarness(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tmp_path = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_config_initialization(self):
        skills_dir = self.tmp_path / "skills"
        state_dir = self.tmp_path / "state"
        cfg = Config(skills_dir=skills_dir, state_dir=state_dir)
        self.assertTrue(skills_dir.exists())
        self.assertTrue(state_dir.exists())
        self.assertEqual(cfg.ledger_file, state_dir / "ledger.jsonl")

    def test_skill_store_save_and_safety_gate(self):
        skills_dir = self.tmp_path / "skills"
        store = SkillStore(skills_dir, author_tag="gemini-autoharness")

        # 1. Save self-authored skill
        path = store.save_skill(
            name="test-skill",
            description="A test skill",
            title="Test Skill",
            content="Step 1: run test"
        )
        self.assertTrue(path.exists())
        self.assertTrue(store.is_self_authored(path.parent))
        self.assertIn("test-skill", store.list_learned_skills())

        # 2. Verify non-self-authored skill cannot be overwritten
        foreign_dir = skills_dir / "user-custom"
        foreign_dir.mkdir(parents=True)
        foreign_file = foreign_dir / "SKILL.md"
        foreign_file.write_text("---\nname: user-custom\nauthor: user\n---\nCustom stuff")

        self.assertFalse(store.is_self_authored(foreign_dir))
        with self.assertRaises(PermissionError):
            store.save_skill("user-custom", "desc", "title", "content")

    def test_ledger_records_and_reads(self):
        ledger_path = self.tmp_path / "ledger.jsonl"
        ledger = Ledger(ledger_path)
        ledger.record(
            action="created",
            skill_name="test-skill",
            conversation_id="conv-123",
            reason="test reflection"
        )
        history = ledger.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["skill_name"], "test-skill")
        self.assertEqual(history[0]["conversation_id"], "conv-123")

    def test_reflector_turn_logic(self):
        reflector = Reflector()
        events = [
            {"role": "user", "text": "hello"},
            {"role": "assistant", "text": "hi"},
            {"role": "user", "text": "fix bug"},
            {"role": "tool_calls", "calls": [{"name": "run_command"}]},
            {"role": "tool_calls", "calls": [{"name": "view_file"}]},
            {"role": "tool_calls", "calls": [{"name": "run_command"}]},
        ]
        self.assertTrue(reflector.should_reflect(events, min_turns=4, min_tools=3))

if __name__ == "__main__":
    unittest.main()
