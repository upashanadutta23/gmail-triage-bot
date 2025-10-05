from __future__ import annotations
import os, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
ROOT = Path(__file__).resolve().parent
TOKEN = ROOT / "token.json"
CREDS = ROOT / "credentials.json"

def get_service():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS.exists():
                print("❌ Missing credentials.json — please place it in the project root.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def list_unread(service, max_results=10):
    resp = service.users().messages().list(userId="me", q="is:unread", maxResults=max_results).execute()
    return resp.get("messages", [])

def main():
    svc = get_service()
    msgs = list_unread(svc, max_results=500)
    if not msgs:
        print("✅ No unread emails found.")
        return
    print(f"📬 Found {len(msgs)} unread messages:\n")
    for m in msgs:
        msg = svc.users().messages().get(
            userId="me", id=m["id"], format="metadata",
            metadataHeaders=["From","Subject","Date"]
        ).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(f"- {headers.get('Date','')} | {headers.get('From','')} | {headers.get('Subject','')}")

if __name__ == "__main__":
    main()

