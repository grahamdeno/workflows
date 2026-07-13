from datetime import datetime, timezone
from pathlib import Path

README = Path("README.md")
START, END = "<!--DAILY:START-->", "<!--DAILY:END-->"

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
block = f"{START}\n_Last automated review: {now}_\n{END}"

text = README.read_text(encoding="utf-8") if README.exists() else "# Daily Automation\n"
if START in text and END in text:
    head, rest = text.split(START, 1)
    text = head + block + rest.split(END, 1)[1]
else:
    text = text.rstrip() + "\n\n" + block + "\n"

README.write_text(text, encoding="utf-8")
print("Updated:", now)

