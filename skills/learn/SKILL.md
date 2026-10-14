---
name: learn
description: >-
  Analyze the current session, distill durable debugging solutions, techniques,
  and workflows into a self-maintaining skill in ~/.agents/skills/, and record
  an entry in the AutoHarness ledger.
---

# /learn Skill Distiller

When invoked (via `/learn` or when the user asks to save/remember the current solution):

1. **Review Session Context**:
   - Inspect the transcript and identify the core solution, fix, or workflow discovered in this conversation.
   - Separate durable patterns (reusable commands, bug fixes, architecture rules) from one-off tasks.

2. **Stage or Update Skill**:
   - Format the skill following the Antigravity `SKILL.md` specification:
     ```markdown
     ---
     name: <concise-name>
     description: >-
       <Trigger condition and summary>
     author: gemini-autoharness
     ---

     # <Title>

     <Instructions and runbook>
     ```
   - Target location: `~/.agents/skills/<skill-name>/SKILL.md` (or workspace `.agents/skills/<skill-name>/SKILL.md`).

3. **Check Safety Gate**:
   - If a skill with that name already exists, verify that it contains `author: gemini-autoharness`.
   - Never overwrite user-authored skills. Merge new lessons into existing self-authored skills where appropriate.

4. **Record Evidence in Ledger**:
   - Append an entry to `~/.gemini/autoharness/ledger.jsonl`:
     ```json
     {"action": "created", "skill_name": "<skill-name>", "reason": "...", "timestamp": "..."}
     ```
