# Aeonis Forge — Email Integration (Gmail API)

Goal: integrate a professional mailbox (e.g. `hello@aeonisforge.com`) into the OpenClaw TUI so Prana can:

- fetch inbox summaries
- triage/label
- draft replies for approval
- send approved replies
- trigger workflows (e.g. publish-digest emails)

## Strategy

- Provider: **Google Workspace** (recommended for automation + deliverability)
- Integration: **Gmail API** via OAuth (user-approved)
- Secrets: stored locally under `email-integration/data/` (gitignored)

## Setup checklist (human steps)

1. Create Google Workspace for `aeonisforge.com`
2. Verify domain ownership (Google will give TXT record)
3. Set MX records for Gmail
4. Create mailboxes/aliases:
   - `hello@aeonisforge.com`
   - `praneeth@aeonisforge.com`

## Developer checklist (agent steps)

1. Create a Google Cloud project + OAuth client (Desktop app)
2. Download `client_secret.json` into `email-integration/data/`
3. Run auth:

```powershell
cd email-integration
.\.venv\Scripts\python -m aeonis_mail.cli auth --creds .\data\client_secret.json --token .\data\token.json
```

4. Test inbox:

```powershell
.\.venv\Scripts\python -m aeonis_mail.cli inbox --max 20
```

## Notes

- This repo should never commit tokens or client secrets.
- We’ll add OpenClaw cron once auth works.
