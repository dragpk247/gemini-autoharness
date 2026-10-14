"""
Configuration models and defaults for Gemini AutoHarness.
"""

from dataclasses import dataclass, field
from pathlib import Path
import os

DEFAULT_MIN_TURNS = 4
DEFAULT_MIN_TOOL_STEPS = 3
DEFAULT_SKILL_AUTHOR = "gemini-autoharness"

@dataclass
class Config:
    # Target directory for learned skills
    # By default, writes to user global ~/.agents/skills or workspace .agents/skills
    skills_dir: Path = field(default_factory=lambda: Path(os.environ.get("AUTOHARNESS_SKILLS_DIR", Path.home() / ".agents" / "skills")))
    
    # State and audit tracking
    state_dir: Path = field(default_factory=lambda: Path(os.environ.get("AUTOHARNESS_STATE_DIR", Path.home() / ".gemini" / "autoharness")))
    
    # Thresholds before automatic reflection triggers
    min_turns: int = DEFAULT_MIN_TURNS
    min_tool_steps: int = DEFAULT_MIN_TOOL_STEPS
    
    # Self-authored gate
    author_tag: str = DEFAULT_SKILL_AUTHOR
    
    # Automated pruning/merging threshold
    similarity_threshold: float = 0.75

    def __post_init__(self):
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    @property
    def ledger_file(self) -> Path:
        return self.state_dir / "ledger.jsonl"
