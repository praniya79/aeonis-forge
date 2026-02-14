import os
from datetime import datetime


def today_path(workspace: str) -> str:
    d = datetime.now()
    return os.path.join(workspace, "memory", f"{d:%Y-%m-%d}.md")


def append_line(workspace: str, section: str, line: str) -> None:
    """Append a bullet under a section in today's memory file (if the file exists).

    This is intentionally conservative: it will not create the daily file automatically.
    (You can choose to create it in your workflow.)
    """
    mem = today_path(workspace)
    if not os.path.exists(mem):
        return

    with open(mem, "r", encoding="utf-8") as f:
        txt = f.read()

    if f"## {section}" not in txt:
        txt = txt.rstrip() + f"\n\n## {section}\n\n"

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt = txt.rstrip() + f"\n- {stamp} — {line}\n"

    with open(mem, "w", encoding="utf-8") as f:
        f.write(txt)
