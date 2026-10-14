# 🧠 Gemini AutoHarness

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/dragpk247/gemini-autoharness)

> **Self-learning skill layer and continuous memory harness for Google Antigravity & the Gemini CLI (`agy`).**

Inspired by [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness), **Gemini AutoHarness** gives AI agents self-distilling, self-maintaining memory. When you solve a difficult bug, configure a tricky environment, or develop a reusable workflow, AutoHarness distills those insights into structured, permanent skills—so your agent never forgets.

---

## ✨ Features

- 🔄 **Autonomous Reflection**: Evaluates session transcripts (`transcript.jsonl`) to detect non-trivial solutions, bug fixes, and custom workflows.
- ⚡ **Antigravity Lifecycle Hooks**: Plugs directly into `SessionStart` (indexing learned skills) and `Stop` (milestone detection) via `hooks.json`.
- 🛡️ **Zero Overwrite Safety Gate**: Only edits or prunes skills explicitly tagged with `author: gemini-autoharness`. Your hand-written skills in `~/.agents/skills/` are strictly protected and never modified.
- 💬 **Interactive `/learn` Command**: Explicitly trigger the `/learn` slash command to immediately distill the current conversation into a permanent skill.
- 📜 **Audit & Evidence Ledger**: Records every creation, update, and merge with conversation IDs and context snippets in `~/.gemini/autoharness/ledger.jsonl`.
- 🚀 **Zero Dependencies**: Pure Python 3.11+ standard library—no heavy frameworks or external packages required.

---

## 🏗️ How It Works

```
┌─────────────────────────┐
│     Active Session      │
│  (Fix bug, write tool)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   AutoHarness Reflector │ ◄── Session transcript & `/learn` command
└────────────┬────────────┘
             │
             ├──────────────────────────────────────────┐
             ▼                                          ▼
┌─────────────────────────┐                ┌─────────────────────────┐
│  Safety Gate Check 🛡️   │                │     Evidence Ledger     │
│ (author == autoharness) │                │  (~/.gemini/ledger)     │
└────────────┬────────────┘                └─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ ~/.agents/skills/<name> │ ──► Available to all future Antigravity &
│       (SKILL.md)        │     Gemini CLI agent sessions
└─────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Installation

Clone into your workspace or plugins directory:

```bash
git clone https://github.com/dragpk247/gemini-autoharness.git ~/Projects/gemini-autoharness
```

To enable AutoHarness as a global Antigravity plugin:

```bash
mkdir -p ~/.gemini/plugins
ln -sfn ~/Projects/gemini-autoharness ~/.gemini/plugins/gemini-autoharness
```

### 2. Using `/learn`

Whenever an agent finishes a task you want it to remember for future sessions, simply run:

```text
/learn
```
or ask:
> *"Save this setup as a skill so you remember it next time."*

AutoHarness will distill the key findings, create an optimized `SKILL.md` under `~/.agents/skills/`, and log the evidence to the ledger.

---

## 📂 Project Structure

```text
gemini-autoharness/
├── hooks.json             # Antigravity lifecycle hooks (SessionStart, Stop)
├── plugin.json            # Antigravity plugin manifest
├── skills/
│   └── learn/
│       └── SKILL.md       # Interactive /learn command definition
├── src/
│   └── autoharness/
│       ├── config.py      # Paths, thresholds & configuration
│       ├── hook_runner.py # Hook event router
│       ├── ledger.py      # Append-only audit logger
│       ├── reflector.py   # Transcript distillation engine
│       └── skill_store.py # Skill manager & safety gate
└── tests/
    └── test_core.py       # Unit test suite
```

---

## 🧪 Running Tests

Verify functionality anytime using the built-in test suite:

```bash
cd ~/Projects/gemini-autoharness
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

[MIT](LICENSE) © [dragpk247](https://github.com/dragpk247)
