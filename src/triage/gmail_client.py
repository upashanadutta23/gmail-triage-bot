# src/triage/gmail_client.py
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

def get_unread_emails(creds, max_results=20):
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", q="is:unread", maxResults=max_results).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No unread messages found.")
        return []

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        
        email_data = {
            "id": msg_data.get("id"),
            "subject": next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject"),
            "sender": next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender"),
            "body": ""
        }
        
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    encoded_body = part.get("body", {}).get("data", "")
                    if encoded_body:
                        email_data["body"] = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
                        break
                elif part["mimeType"] == "text/html":
                    encoded_body = part.get("body", {}).get("data", "")
                    if encoded_body:
                        html_content = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
                        soup = BeautifulSoup(html_content, "html.parser")
                        email_data["body"] = soup.get_text(separator='\n').strip()
        else:
            encoded_body = payload.get("body", {}).get("data", "")
            if encoded_body:
                email_data["body"] = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
        
        emails.append(email_data)
        
    return emails

def mark_email_as_read(creds, msg_id):
    service = build("gmail", "v1", credentials=creds)
    try:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"  -> Marked email {msg_id[:10]}... as read.")
    except Exception as e:
        print(f"  -> Error marking email as read: {e}")
