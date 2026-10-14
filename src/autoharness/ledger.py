"""
Audit ledger for tracking generated, merged, updated, and pruned skills.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

class Ledger:
    def __init__(self, ledger_path: Path):
        self.ledger_path = ledger_path

    def record(
        self,
        action: str,  # created, updated, merged, pruned
        skill_name: str,
        conversation_id: Optional[str] = None,
        reason: str = "",
        evidence_snippet: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "skill_name": skill_name,
            "conversation_id": conversation_id or "unknown",
            "reason": reason,
            "evidence_snippet": evidence_snippet,
            "metadata": metadata or {}
        }
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_history(self, skill_name: Optional[str] = None):
        if not self.ledger_path.exists():
            return []
        entries = []
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    if not skill_name or item.get("skill_name") == skill_name:
                        entries.append(item)
        return entries
