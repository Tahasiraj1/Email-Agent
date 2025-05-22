import os.path
import json
from services.auth import authenticate
from googleapiclient.discovery import build

from agents import function_tool

import base64
from bs4 import BeautifulSoup  # Optional but recommended

def extract_email_body(msg_payload: dict) -> str:
    """Extract full email body text from Gmail message payload."""

    def decode_base64(data: str) -> str:
        return base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')

    # Case 1: Email is plain text
    if msg_payload.get("body", {}).get("data"):
        return decode_base64(msg_payload["body"]["data"])

    # Case 2: Email has multiple parts (e.g. HTML + plain text)
    parts = msg_payload.get("parts", [])
    for part in parts:
        mime_type = part.get("mimeType", "")
        if mime_type == "text/plain" and "data" in part.get("body", {}):
            return decode_base64(part["body"]["data"])
        elif mime_type == "text/html" and "data" in part.get("body", {}):
            html = decode_base64(part["body"]["data"])
            
            soup = BeautifulSoup(html, 'html.parser')
            plain_text = soup.get_text(separator=' ', strip=True)

            return plain_text

    return "[Could not extract body]"

def list_latest_emails(service, max_results=1):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    emails_list = []

    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        email_id = msg_data.get("id", "")
        thread_id = msg_data.get("threadId", "")
        labels_id = msg_data.get("labelIds", [])
        headers = msg_data.get("payload", {}).get("headers", [])
        to = next((h['value'] for h in headers if h['name'] == 'Delivered-To'), None)
        timestamp = msg_data.get("internalDate", "")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(No Sender)")
        # snippet = msg_data.get("snippet", "").replace('\u200c', '').replace('\u034f', '').replace('\u200f', '').replace('\xa0', '').replace('\ufeff', '').strip()
        payload = msg_data['payload']
        body = extract_email_body(payload)

        email_data = {
                "email_id": email_id,
                "thread_id": thread_id,
                "labels_id": labels_id,
                "sender": sender,
                "to": to,
                'timestamp': timestamp,
                "subject": subject,
                "body": body
        }

        emails_list.append(json.dumps(email_data, indent=4))

    return emails_list

# @function_tool
def fetch_emails():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    emails = list_latest_emails(service)
    return emails


if __name__ == '__main__':
    result = fetch_emails()
    for i, email in enumerate(result):
        print(f"\n {i+1}. {email}")
