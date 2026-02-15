from __future__ import annotations

import argparse
from pathlib import Path

from rich import print

from aeonis_mail.gmail_client import get_gmail_service


def cmd_auth(creds: Path, token: Path) -> int:
    _ = get_gmail_service(creds, token)
    print("[green]OK[/green] Authenticated and token saved:", str(token))
    return 0


def cmd_inbox(creds: Path, token: Path, max_results: int) -> int:
    svc = get_gmail_service(creds, token)
    res = svc.users().messages().list(userId="me", maxResults=max_results, q="in:inbox").execute()
    msgs = res.get("messages", [])
    print(f"Inbox messages: {len(msgs)}")
    for m in msgs:
        mid = m["id"]
        msg = svc.users().messages().get(userId="me", id=mid, format="metadata", metadataHeaders=["From","Subject","Date"]).execute()
        headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
        print(f"- {mid} | {headers.get('Date','')} | {headers.get('From','')} | {headers.get('Subject','')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="aeonis-mail")
    ap.add_argument("--creds", type=Path, default=Path("data") / "client_secret.json")
    ap.add_argument("--token", type=Path, default=Path("data") / "token.json")

    sub = ap.add_subparsers(dest="cmd", required=True)

    p_auth = sub.add_parser("auth")
    p_inbox = sub.add_parser("inbox")
    p_inbox.add_argument("--max", type=int, default=10)

    args = ap.parse_args()

    if args.cmd == "auth":
        return cmd_auth(args.creds, args.token)
    if args.cmd == "inbox":
        return cmd_inbox(args.creds, args.token, args.max)

    raise SystemExit("unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
