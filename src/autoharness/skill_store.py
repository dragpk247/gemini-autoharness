"""
Safe skill storage adhering to Antigravity SKILL.md specs with a strict self-authored gate.
"""

from pathlib import Path
from typing import Optional, Dict, List
import re

SKILL_TEMPLATE = """---
name: {name}
description: >-
  {description}
author: {author}
---

# {title}

{content}
"""

class SkillStore:
    def __init__(self, skills_dir: Path, author_tag: str = "gemini-autoharness"):
        self.skills_dir = skills_dir
        self.author_tag = author_tag

    def is_self_authored(self, skill_dir: Path) -> bool:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            return False
        content = skill_file.read_text(encoding="utf-8")
        # Check author frontmatter tag
        return f"author: {self.author_tag}" in content

    def list_learned_skills(self) -> List[str]:
        skills = []
        for p in self.skills_dir.iterdir():
            if p.is_dir() and self.is_self_authored(p):
                skills.append(p.name)
        return sorted(skills)

    def get_skill(self, name: str) -> Optional[Dict[str, str]]:
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return None
        raw = skill_file.read_text(encoding="utf-8")
        
        # Simple frontmatter parse
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
        if not frontmatter_match:
            return {"content": raw, "name": name, "description": "", "raw": raw}
        
        fm = frontmatter_match.group(1)
        body = frontmatter_match.group(2)
        desc = ""
        for line in fm.splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
        
        return {
            "name": name,
            "description": desc,
            "content": body.strip(),
            "raw": raw
        }

    def save_skill(self, name: str, description: str, title: str, content: str) -> Path:
        target_dir = self.skills_dir / name
        target_dir.mkdir(parents=True, exist_ok=True)
        skill_file = target_dir / "SKILL.md"

        # Gate check: If file exists and is NOT self-authored, refuse to overwrite!
        if skill_file.exists() and not self.is_self_authored(target_dir):
            raise PermissionError(
                f"Safety Guard: Skill '{name}' was not created by {self.author_tag}. "
                "Refusing to overwrite user-authored skill."
            )

        rendered = SKILL_TEMPLATE.format(
            name=name,
            description=description.strip(),
            author=self.author_tag,
            title=title.strip(),
            content=content.strip()
        )
        skill_file.write_text(rendered, encoding="utf-8")
        return skill_file

    def remove_skill(self, name: str) -> bool:
        target_dir = self.skills_dir / name
        if not target_dir.exists():
            return False
        if not self.is_self_authored(target_dir):
            raise PermissionError(
                f"Safety Guard: Skill '{name}' is not self-authored. Refusing removal."
            )
        import shutil
        shutil.rmtree(target_dir)
        return True
