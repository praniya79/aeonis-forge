#!/usr/bin/env python
"""Seventh River ecosystem CLI.

Commands:
- new <name> --template fastapi
- run <name>
- pack <name>

Local-first, minimal dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES = os.path.join(ROOT, "river_ecosystem", "templates")
APPS = os.path.join(ROOT, "apps")
DIST = os.path.join(ROOT, "dist")


def die(msg: str, code: int = 2):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def cmd_new(args):
    name = args.name
    template = args.template

    src = os.path.join(TEMPLATES, f"{template}_app")
    if not os.path.isdir(src):
        die(f"Unknown template: {template}")

    os.makedirs(APPS, exist_ok=True)
    dst = os.path.join(APPS, name)
    if os.path.exists(dst):
        die(f"App already exists: {dst}")

    shutil.copytree(src, dst)

    # Substitute placeholders
    for root, _, files in os.walk(dst):
        for fn in files:
            if fn.endswith((".py", ".json", ".txt", ".md")):
                p = os.path.join(root, fn)
                with open(p, "r", encoding="utf-8") as f:
                    txt = f.read()
                txt = txt.replace("__APP_NAME__", name)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(txt)

    print(f"Created app: {dst}")


def _load_manifest(app_dir: str) -> dict:
    mf = os.path.join(app_dir, "manifest.json")
    if not os.path.isfile(mf):
        die(f"Missing manifest: {mf}")
    with open(mf, "r", encoding="utf-8") as f:
        return json.load(f)


def _pick_python() -> list[str]:
    """Prefer py -3.13 if available; fall back to python."""
    if os.name == "nt":
        try:
            r = subprocess.run(["py", "-3.13", "-c", "import sys; print(sys.version)"], capture_output=True, text=True)
            if r.returncode == 0:
                return ["py", "-3.13"]
        except Exception:
            pass
    return ["python"]


def cmd_run(args):
    name = args.name
    app_dir = os.path.join(APPS, name)
    if not os.path.isdir(app_dir):
        die(f"Missing app: {app_dir}")

    manifest = _load_manifest(app_dir)
    host = manifest.get("host", "127.0.0.1")
    port = int(args.port or manifest.get("port", 9997))

    req = os.path.join(app_dir, "requirements.txt")
    if not os.path.isfile(req):
        die(f"Missing requirements: {req}")

    py = _pick_python()

    # Install deps
    print(f"Installing deps for {name}...")
    subprocess.run(py + ["-m", "pip", "install", "-r", req], check=True)

    # Launch
    print(f"Starting {name} on http://{host}:{port} ...")
    env = os.environ.copy()
    env.setdefault("OPENCLAW_WORKSPACE", ROOT)

    # Uvicorn target: apps.<name>.app:app
    target = f"apps.{name}.app:app"
    try:
        subprocess.run(py + ["-m", "uvicorn", target, "--host", host, "--port", str(port)], check=True, env=env)
    except subprocess.CalledProcessError as e:
        # Common case on Windows: port already in use
        msg = str(e)
        if "10048" in msg or "address already in use" in msg.lower():
            die(f"Port {port} is already in use. Stop the other server or rerun with --port <freeport>.")
        raise


def cmd_pack(args):
    name = args.name
    app_dir = os.path.join(APPS, name)
    if not os.path.isdir(app_dir):
        die(f"Missing app: {app_dir}")

    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"{name}.zip")

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(app_dir):
            for fn in files:
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, os.path.dirname(app_dir))
                z.write(p, rel)

    print(f"Packed: {out}")


def main():
    ap = argparse.ArgumentParser(prog="river")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_new = sub.add_parser("new", help="Create a new app from a template")
    ap_new.add_argument("name")
    ap_new.add_argument("--template", default="fastapi", choices=["fastapi"], help="Template name")
    ap_new.set_defaults(fn=cmd_new)

    ap_run = sub.add_parser("run", help="Install deps (if needed) and run an app locally")
    ap_run.add_argument("name")
    ap_run.add_argument("--port", type=int, default=None, help="Override port (default: from manifest)")
    ap_run.set_defaults(fn=cmd_run)

    ap_pack = sub.add_parser("pack", help="Zip an app into dist/")
    ap_pack.add_argument("name")
    ap_pack.set_defaults(fn=cmd_pack)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
