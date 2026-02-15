from __future__ import annotations

import subprocess
from pathlib import Path


def export_7z(src_dir: Path, out_path: Path, password: str) -> None:
    """Create an encrypted 7z archive from src_dir.

    Requires 7-Zip installed (7z.exe on PATH).
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # -mhe=on encrypts file names too
    cmd = [
        "7z",
        "a",
        str(out_path),
        str(src_dir),
        f"-p{password}",
        "-mhe=on",
        "-mx=9",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"7z failed ({p.returncode}):\n{p.stdout}\n{p.stderr}")
