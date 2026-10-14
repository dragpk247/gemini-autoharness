"""
Reflector module that analyzes transcripts from Antigravity/Gemini sessions
and extracts durable skills, procedures, or domain knowledge.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DISTILLATION_PROMPT = """You are an expert Autonomous Skill Distiller for AI coding agents.
Analyze the provided transcript of an agent session and extract ANY durable, reusable pattern, technique,
runbook, debugging fix, or domain-specific workflow discovered or executed.

Ignore transient conversational chatter, simple greetings, or one-off throwaway queries.

Output MUST be a JSON object conforming strictly to this structure:
{
  "has_durable_skill": true/false,
  "reasoning": "brief explanation of why this is or isn't a reusable skill",
  "skill": {
    "name": "concise-kebab-case-name",
    "title": "Clear Skill Title",
    "description": "Trigger instructions and summary for when this skill must be invoked",
    "content": "Detailed Markdown instructions, runbook steps, commands, and edge-cases",
    "evidence_snippet": "Relevant user prompt or command output that inspired this skill"
  }
}

Transcript summary:
"""

class Reflector:
    def __init__(self, model_caller=None):
        self.model_caller = model_caller

    def parse_transcript(self, transcript_path: Path) -> List[Dict[str, Any]]:
        """Parses Antigravity transcript.jsonl into user requests and tool execution traces."""
        if not transcript_path.exists():
            return []

        events = []
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    step = json.loads(line)
                    step_type = step.get("type")
                    source = step.get("source")
                    content = step.get("content", "")
                    tool_calls = step.get("tool_calls", [])

                    if step_type == "USER_INPUT":
                        events.append({"role": "user", "text": content})
                    elif step_type == "PLANNER_RESPONSE":
                        if tool_calls:
                            events.append({"role": "tool_calls", "calls": tool_calls})
                        if content:
                            events.append({"role": "assistant", "text": content})
                    elif step_type == "GENERIC" and content:
                        events.append({"role": "tool_output", "text": content[:500]})
                except Exception:
                    continue
        return events

    def should_reflect(self, events: List[Dict[str, Any]], min_turns: int = 4, min_tools: int = 3) -> bool:
        user_turns = sum(1 for e in events if e.get("role") == "user")
        tool_turns = sum(1 for e in events if e.get("role") == "tool_calls")
        return user_turns >= min_turns or tool_turns >= min_tools

    def format_for_reflection(self, events: List[Dict[str, Any]], max_chars: int = 15000) -> str:
        lines = []
        for e in events:
            role = e.get("role")
            if role == "user":
                lines.append(f"[User]: {e.get('text', '')}")
            elif role == "assistant":
                lines.append(f"[Assistant]: {e.get('text', '')}")
            elif role == "tool_calls":
                calls = [c.get("name") for c in e.get("calls", [])]
                lines.append(f"[Tool Calls]: {', '.join(calls)}")
            elif role == "tool_output":
                lines.append(f"[Output]: {e.get('text', '')[:200]}")
        
        full_text = "\n".join(lines)
        if len(full_text) > max_chars:
            return full_text[-max_chars:]
        return full_text
