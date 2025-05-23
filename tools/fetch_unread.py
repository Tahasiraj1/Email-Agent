from services.auth import authenticate
from googleapiclient.discovery import build
import google.generativeai as genai
from agents import function_tool
import base64
import os
from typing import List
from models.interfaces import Email

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

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
        if mime_type == ("text/plain") and "data" in part.get("body", {}):
            return decode_base64(part["body"]["data"]).replace('\r\n', ' ').strip()
        elif mime_type == "text/html" and "data" in part.get("body", {}):
            return decode_base64(part["body"]["data"]).replace('\r\n', ' ').strip()
            
    return "[Could not extract body]"

def list_latest_emails(max_results=1):

    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

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
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        
        timestamp = msg_data.get("internalDate", "")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(No Sender)")
        to = next((h['value'] for h in headers if h['name'] == 'Delivered-To'), None)
        snippet = msg_data.get("snippet", "").replace('\u200c', '').replace('\u034f', '').replace('\u200f', '').replace('\xa0', '').replace('\ufeff', '').strip()
        body = extract_email_body(payload)

        email_data = {
                "email_id": email_id,
                "thread_id": thread_id,
                "labels_id": labels_id,
                "sender": sender,
                "to": to,
                'timestamp': timestamp,
                "subject": subject,
                "body": snippet
        }


        # Generate email category
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
        DO NOT provide explanations or additional information.
        JUST return the category name, from the following categories:

        - Urgent (immediately respond)
        - Important (requires attention)
        - Draft (draft email)
        - Spam (Ignore)

        Categorize the following emails or email:
        {email_data}
        """

        response = model.generate_content(prompt)
        print(response.text)
        email_data["category"] = response.text

        emails_list.append(email_data)

    return emails_list

@function_tool
def fetch_emails() -> List[Email]:
    return list_latest_emails()


if __name__ == '__main__':
    result = fetch_emails()
    for i, email in enumerate(result):
        print(f"\n {i+1}. {email}")
