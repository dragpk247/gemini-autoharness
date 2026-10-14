# Gemini AutoHarness

**Self-learning skill layer for Google Antigravity & Gemini CLI (`agy`).**

Inspired by [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness), this project equips Gemini with self-distilling, self-maintaining skill memory directly integrated into Antigravity's lifecycle hooks and progressive disclosure system.

## Key Features

- **Learns from Real Sessions**: Analyzes session transcripts (`transcript.jsonl`) when meaningful debugging or workflow solutions occur.
- **Antigravity Hook Integration**: Hooks seamlessly into `SessionStart` (indexing learned skills) and `Stop` (detecting completion milestones) via `hooks.json`.
- **Strict Self-Authored-Only Safety Gate**: Only updates and prunes skills tagged with `author: gemini-autoharness`. Hand-written skills in `~/.agents/skills/` are left completely untouched.
- **On-Demand `/learn` Command**: Provides an explicit `/learn` trigger to distill the current conversation into a permanent, reusable skill immediately.
- **Traceable Evidence Ledger**: Logs every creation, merge, and update with conversation ID and evidence snippet in `~/.gemini/autoharness/ledger.jsonl`.
- **Zero Third-Party Dependencies**: Pure Python 3.11+ standard library implementation.

## Architecture

```text
gemini-autoharness/
├── hooks.json             # Lifecycle hook configuration (SessionStart, Stop)
├── plugin.json            # Antigravity plugin manifest
├── skills/
│   └── learn/
│       └── SKILL.md       # Interactive /learn command definition
├── src/
│   └── autoharness/
│       ├── config.py      # Path resolution and reflection thresholds
│       ├── hook_runner.py # stdin/stdout hook handler
│       ├── ledger.py      # Append-only audit logging
│       ├── reflector.py   # Transcript parser and distillation engine
│       └── skill_store.py # Antigravity SKILL.md manager & safety gate
└── tests/
    └── test_core.py       # Full test suite
```

## Running Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
