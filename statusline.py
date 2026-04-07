#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import unicodedata

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# ── User Configuration ──────────────────────────────────────
CWD_SEGMENTS = 2            # number of trailing path segments to display
PROGRESS_BAR_WIDTH = 10     # character width of the context progress bar
COLUMN_GAP = 2              # extra spaces between columns

# (input, cache_write, cache_read, output) $/M tokens
# https://platform.claude.com/docs/en/about-claude/pricing
# Cache rules: cache_write = input * 1.25, cache_read = input * 0.1
# Updated: 2026-03-26
PRICING = {
    'opus':   (  5.00,     6.25,        0.50,       25.00),
    'sonnet': (  3.00,     3.75,        0.30,       15.00),
    'haiku':  (  1.00,     1.25,        0.10,        5.00),
}
# ─────────────────────────────────────────────────────────────

try:
    data = json.load(sys.stdin)
except Exception:
    print("statusline error")
    sys.exit(0)

# ── Model & Working Directory ────────────────────────────────
model_name = data.get('model', {}).get('display_name', '?')
cwd_full = data.get('cwd', '')
cwd_parts = cwd_full.replace('\\', '/').rstrip('/').rsplit('/', CWD_SEGMENTS)
cwd_short = '/'.join(cwd_parts[-CWD_SEGMENTS:]) if len(cwd_parts) >= CWD_SEGMENTS else cwd_parts[-1]

# ── Code Changes & Duration ──────────────────────────────────
cost_data = data.get('cost', {})
lines_added = cost_data.get('total_lines_added', 0) or 0
lines_removed = cost_data.get('total_lines_removed', 0) or 0
total_mins = round((cost_data.get('total_duration_ms', 0) or 0) / 60000, 1)
api_mins = round((cost_data.get('total_api_duration_ms', 0) or 0) / 60000, 1)

# ── Context Window ───────────────────────────────────────────
ctx_window = data.get('context_window', {})
ctx_size = ctx_window.get('context_window_size', 0) or 0
ctx_used_pct = ctx_window.get('used_percentage', 0) or 0
total_input_tokens = ctx_window.get('total_input_tokens', 0) or 0
total_output_tokens = ctx_window.get('total_output_tokens', 0) or 0

# ── Current Turn Tokens ──────────────────────────────────────
current = ctx_window.get('current_usage', {}) or {}
cur_input = current.get('input_tokens', 0) or 0
cur_output = current.get('output_tokens', 0) or 0
cur_cache_read = current.get('cache_read_input_tokens', 0) or 0
cur_cache_create = current.get('cache_creation_input_tokens', 0) or 0

# ── Cost Calculation ─────────────────────────────────────────

model_id = data.get('model', {}).get('id', '').lower()
price = PRICING['haiku']
for key in PRICING:
    if key in model_id:
        price = PRICING[key]
        break
p_in, p_cache_write, p_cache_read, p_out = price

total_cost = round(cost_data.get('total_cost_usd', 0) or 0, 2)
cur_cost = round(
    cur_input * p_in / 1e6
    + cur_cache_create * p_cache_write / 1e6
    + cur_cache_read * p_cache_read / 1e6
    + cur_output * p_out / 1e6,
    4,
)

# ── Formatting Helpers ───────────────────────────────────────
def fmt(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)

def progress_bar(pct, width=PROGRESS_BAR_WIDTH):
    filled = round(width * pct / 100)
    return '█' * filled + '░' * (width - filled)

def cost_indicator(cost):
    if cost < 0.05:
        return '\U0001f60a'  # 😊
    if cost < 0.10:
        return '\U0001f642'  # 🙂
    if cost < 0.20:
        return '\U0001f610'  # 😐
    if cost < 0.50:
        return '\U0001f62e'  # 😮
    if cost < 1.00:
        return '\U0001f92f'  # 🤯
    return '\U0001f480'      # 💀

def display_width(s):
    """Estimate the terminal display width of a string."""
    w = 0
    chars = list(s)
    for i, ch in enumerate(chars):
        cp = ord(ch)
        if cp in (0xFE0F, 0xFE0E):
            continue
        cat = unicodedata.category(ch)
        if cat in ('Mn', 'Me', 'Cf'):
            continue
        has_fe0f = (i + 1 < len(chars) and ord(chars[i + 1]) == 0xFE0F)
        if cp > 0xFFFF or has_fe0f or unicodedata.east_asian_width(ch) in ('W', 'F'):
            w += 2
        else:
            w += 1
    return w

def pad(s, width):
    return s + ' ' * max(0, width - display_width(s))

# ── Output (column-aligned) ──────────────────────────────────
cols1 = [
    f"\U0001f9e0 {model_name}",
    f"\U0001f4c2 {cwd_short}",
    f"\U0001f4dd +{lines_added}/-{lines_removed}",
    f"\U0001f4be {fmt(ctx_size)} {progress_bar(ctx_used_pct)} {ctx_used_pct}%",
]

cols2 = [
    f"\U0001f4ac \u2193{fmt(total_input_tokens)} \u2191{fmt(total_output_tokens)}"
    f" (\u2193{fmt(cur_input)} \u2191{fmt(cur_output)})",
    f"\u26a1 \u2193{fmt(cur_cache_create)} \u2191{fmt(cur_cache_read)}",
    f"\U0001f4b0 ${total_cost} (${cur_cost} {cost_indicator(cur_cost)})",
    f"\U0001f554 {total_mins}min (API {api_mins}min)",
]

ncols = min(len(cols1), len(cols2)) - 1
widths = [max(display_width(cols1[i]), display_width(cols2[i])) + COLUMN_GAP for i in range(ncols)]

line1 = ''.join(pad(s, w) for s, w in zip(cols1[:ncols], widths)) + cols1[-1]
line2 = ''.join(pad(s, w) for s, w in zip(cols2[:ncols], widths)) + cols2[-1]

print(f"{line1}\n{line2}")
