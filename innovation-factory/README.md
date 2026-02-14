# Innovation Factory (MVP)

A continuous "agentic civilization sim" → blueprint harvester that:

- generates innovation candidates (structured JSON)
- critiques + scores + safety-flags them
- converts approved items into:
  - Hugo blog posts (Markdown)
  - beautiful PDFs (Typst)
- archives everything with dedupe + metadata (SQLite)

## Folder layout

- `innovation_factory/` — Python package
- `templates/` — Typst + Markdown templates
- `artifacts/` — generated outputs (posts, pdfs)
- `data/` — SQLite DB, run logs

## Run (local)

> Prereqs: Python 3.11+ (recommended), Typst (optional until PDF step)

Create venv + install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Generate a single sample blueprint end-to-end:

```powershell
python -m innovation_factory.cli demo --out artifacts
```

## Publish flow (recommended)

- Factory runs continuously and fills an **Approval Queue** in the DB.
- You approve items (CLI or small local UI).
- Approved items are rendered to `site/content/posts/*.md` + PDFs.
- Hugo builds + deploys (later: git push / Netlify / Cloudflare Pages).

## Safety

This project is designed to **never auto-publish raw agent output**.
Start with manual approval.
