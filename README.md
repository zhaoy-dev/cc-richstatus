# cc-richstatus

A rich, two-line status bar for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that shows model info, token usage, cost estimation, context window progress, and more — all column-aligned in your terminal.

## Preview

```
🧠 Opus 4.6 (1M context)       📂 myproject/src  📝 +70/-41            💾 1.0M ██░░░░░░░░ 20%
💬 ↓477.0k ↑3.5k (↓1.0k ↑254)  ⚡ ↓1.7k ↑32.1k   💰 $0.98 ($0.038 😊)  🕔 4.9min (API 1.9min)
```

## Quick Start

Paste this to Claude Code:

```
Configure the status line using https://raw.githubusercontent.com/zhaoy-dev/cc-richstatus/main/statusline.py
```

## Update

macOS / Linux:

```bash
python ~/.claude/statusline.py --update
```

Windows (cmd):

```bash
python %USERPROFILE%\.claude\statusline.py --update
```

Windows (PowerShell):

```bash
python "$env:USERPROFILE\.claude\statusline.py" --update
```

Restart Claude Code after updating.

## What's Displayed

| Icon | Field | Description |
|------|-------|-------------|
| 🧠 | Model | Active model name |
| 📂 | Directory | Last two segments of working directory |
| 📝 | Changes | Lines added / removed in this session |
| 💾 | Context | Context window size, usage progress bar, and percentage |
| 💬 | Tokens | Total and current-turn input/output tokens |
| ⚡ | Cache | Cache write (↓) and cache read (↑) tokens for current turn |
| 💰 | Cost | Total session cost and current-turn cost with indicator (😊🙂😐😮🤯💀) |
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

## License

MIT
