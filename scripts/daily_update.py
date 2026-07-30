import json
import sys
from datetime import datetime, timezone
from pathlib import Path

README = Path("README.md")
BOARD = Path("data/board.json")
START, END = "<!--DAILY:START-->", "<!--DAILY:END-->"

STAGE_ORDER = ["Decide & Sequence", "Engage", "Define",
               "Communicate", "Accelerate", "Ship", "Trust"]

def esc(v):
    return str(v).replace("|", "\\|").strip()

if not BOARD.exists():
    print(f"ERROR: {BOARD} missing.")
    sys.exit(1)

try:
    items = json.loads(BOARD.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"ERROR: invalid JSON in {BOARD}: {e}")
    sys.exit(1)

items.sort(key=lambda i: STAGE_ORDER.index(i["stage"])
           if i.get("stage") in STAGE_ORDER else len(STAGE_ORDER))

rows = ["| Stage | Item | Status | Notes |", "|---|---|---|---|"]
for i in items:
    rows.append(f"| {esc(i.get('stage',''))} | {esc(i.get('item',''))} "
                f"| {esc(i.get('status',''))} | {esc(i.get('notes',''))} |")

counts = {}
for i in items:
    s = i.get("status", "Unknown")
    counts[s] = counts.get(s, 0) + 1
summary = " · ".join(f"{n} {s}" for s, n in sorted(counts.items()))

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
block = (f"{START}\n## Delivery Board\n\n" + "\n".join(rows) +
         f"\n\n**{len(items)} items:** {summary}\n\n"
         f"_Auto-generated {now} — edit `data/board.json`, not this table._\n{END}")

text = README.read_text(encoding="utf-8") if README.exists() else "# Delivery Board\n"
if START in text and END in text:
    head, rest = text.split(START, 1)
    text = head + block + rest.split(END, 1)[1]
else:
    text = text.rstrip() + "\n\n" + block + "\n"

README.write_text(text, encoding="utf-8")
print(f"Published {len(items)} items, {now}")
