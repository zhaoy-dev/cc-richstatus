# cc-richstatus

A rich, two-line status bar for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that shows model info, token usage, cost estimation, context window progress, and more — all column-aligned in your terminal.

## Preview

```
🧠 Opus 4.6 (1M context)       📂 myproject/src  📝 +70/-41         💾 1.0M ██░░░░░░░░ 20%
💬 ↓477.0k ↑3.5k (↓1.0k ↑254)  ⚡ ↓1.7k ↑32.1k   💰 $0.98 ($0.038)  🕔 4.9min (API 1.9min)
```

## Quick Start

Paste this to Claude Code:

```
Configure the status line using https://raw.githubusercontent.com/zhaoy-dev/cc-richstatus/main/statusline.py
```

## What's Displayed

| Icon | Field | Description |
|------|-------|-------------|
| 🧠 | Model | Active model name |
| 📂 | Directory | Last two segments of working directory |
| 📝 | Changes | Lines added / removed in this session |
| 💾 | Context | Context window size, usage progress bar, and percentage |
| 💬 | Tokens | Total and current-turn input/output tokens |
| ⚡ | Cache | Cache write (↓) and cache read (↑) tokens for current turn |
| 💰 | Cost | Total session cost and current-turn cost (estimated) |
| 🕔 | Duration | Total session time and API time |

### Cost Estimation

Current-turn cost is calculated locally using official pricing (updated 2026-03-26):

| Model | Input | Cache Write | Cache Read | Output |
|-------|-------|-------------|------------|--------|
| Opus | $5.00/M | $6.25/M | $0.50/M | $25.00/M |
| Sonnet | $3.00/M | $3.75/M | $0.30/M | $15.00/M |
| Haiku | $1.00/M | $1.25/M | $0.10/M | $5.00/M |

## Requirements

- Python 3.8+
- Claude Code CLI

## Installation

### Manual setup

1. Copy `statusline.py` to your Claude config directory:

```bash
# macOS / Linux
cp statusline.py ~/.claude/statusline.py

# Windows
copy statusline.py %USERPROFILE%\.claude\statusline.py
```

2. Add the status line config to `~/.claude/settings.json`:

```jsonc
{
  "statusLine": {
    "type": "command",
    "command": "python ~/.claude/statusline.py"          // macOS / Linux
    // "command": "python %USERPROFILE%/.claude/statusline.py"  // Windows
  }
}
```

3. Restart Claude Code. The status bar will appear at the top of the terminal.

## Customization

All configurable variables are declared at the top of `statusline.py`:

```python
# ── User Configuration ──────────────────────────────────────
CWD_SEGMENTS = 2            # number of trailing path segments to display
PROGRESS_BAR_WIDTH = 10     # character width of the context progress bar
COLUMN_GAP = 2              # extra spaces between columns

PRICING = {
    #           (input,  cache_write,  cache_read,  output)  $/M tokens
    'opus':   (  5.00,     6.25,        0.50,       25.00),
    'sonnet': (  3.00,     3.75,        0.30,       15.00),
    'haiku':  (  1.00,     1.25,        0.10,        5.00),
}
```

| Variable | Default | Description |
|----------|---------|-------------|
| `CWD_SEGMENTS` | `2` | How many trailing path segments to show (e.g. `2` → `myproject/src`) |
| `PROGRESS_BAR_WIDTH` | `10` | Character width of the context usage progress bar |
| `COLUMN_GAP` | `2` | Extra spaces between columns for visual separation |
| `PRICING` | Official rates | Per-model token pricing ($/M tokens), update when Anthropic changes pricing |

### Swap or reorder sections

Each line is defined as a list of columns (`cols1` and `cols2`). Rearrange the items to change the display order:

```python
cols1 = [
    f"🧠 {model_name}",       # column 1
    f"📂 {cwd_short}",         # column 2
    f"📝 +{lines_added}/...",  # column 3
    f"💾 {fmt(ctx_size)} ...", # column 4 (last, no padding)
]
```

## License

MIT
