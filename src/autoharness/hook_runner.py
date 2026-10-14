"""
Hook dispatcher that conforms to Antigravity hooks.json lifecycle contracts.
"""

import sys
import json
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from autoharness.config import Config
from autoharness.reflector import Reflector
from autoharness.skill_store import SkillStore
from autoharness.ledger import Ledger

def handle_session_start(payload: dict, config: Config, store: SkillStore) -> dict:
    learned = store.list_learned_skills()
    if not learned:
        return {}

    # Surface index of learned skills at session startup
    index_msg = (
        f"🤖 [AutoHarness] Loaded {len(learned)} self-learned skill(s): "
        f"{', '.join(learned)}. Use them when matching problems arise."
    )
    return {
        "injectSteps": [
            {
                "ephemeralMessage": index_msg
            }
        ]
    }

def handle_stop(payload: dict, config: Config, store: SkillStore, ledger: Ledger) -> dict:
    conv_id = payload.get("conversationId", "unknown")
    transcript_path_str = payload.get("transcriptPath")
    
    if not transcript_path_str:
        return {}
    
    transcript_path = Path(transcript_path_str)
    if not transcript_path.exists():
        return {}

    reflector = Reflector()
    events = reflector.parse_transcript(transcript_path)

    if not reflector.should_reflect(events, min_turns=config.min_turns, min_tools=config.min_tool_steps):
        return {}

    # Queue or log background analysis signal
    task_file = config.state_dir / "pending_distillations.jsonl"
    with open(task_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "conversation_id": conv_id,
            "transcript_path": str(transcript_path),
            "events_count": len(events)
        }) + "\n")

    return {}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing hook event argument"}))
        sys.exit(1)

    event_type = sys.argv[1]
    
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception as e:
        payload = {}

    config = Config()
    store = SkillStore(config.skills_dir, config.author_tag)
    ledger = Ledger(config.ledger_file)

    if event_type == "SessionStart":
        resp = handle_session_start(payload, config, store)
    elif event_type == "Stop":
        resp = handle_stop(payload, config, store, ledger)
    elif event_type in ("PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation"):
        resp = {}
    else:
        resp = {}

    print(json.dumps(resp))

if __name__ == "__main__":
    main()
