from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from services.auth import authenticate
from models.interfaces import Email
from .categorizer import EmailCategorizer
from typing import List
import base64

class EmailFetcher:
    def __init__(self, max_results=1):
        self.max_results = max_results

    @staticmethod
    def _decode_base64(data: str) -> str:
        return base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')

    @staticmethod
    def _extract_email_body(msg_payload: dict) -> str:
        """Extract full email body text from Gmail message payload."""

        # Case 1: Email is plain text
        if msg_payload.get("body", {}).get("data"):
            return EmailFetcher._decode_base64(msg_payload["body"]["data"])

        # Case 2: Email has multiple parts (e.g. HTML + plain text)
        parts = msg_payload.get("parts", [])
        for part in parts:
            mime_type = part.get("mimeType", "")
            if mime_type == ("text/plain") and "data" in part.get("body", {}):
                return EmailFetcher._decode_base64(part["body"]["data"]).replace('\r\n', ' ').strip()
            elif mime_type == "text/html" and "data" in part.get("body", {}):
                return EmailFetcher._decode_base64(part["body"]["data"]).replace('\r\n', ' ').strip()

        return "[Could not extract body]"

    @authenticate
    def _list_latest_emails(self, creds=None) -> List[Email]:
        try:
            service = build('gmail', 'v1', credentials=creds)

            results = service.users().messages().list(
                userId='me', maxResults=self.max_results, q="is:unread").execute()
            messages = results.get('messages', [])

            emails_list = []

            if not messages:
                print("No messages found.")
                return

            for msg in messages:
                msg_id = msg['id']
                msg_data = service.users().messages().get(
                    userId='me', id=msg_id, format='full').execute()

                email_id = msg_data.get("id", "")
                thread_id = msg_data.get("threadId", "")
                labels_id = msg_data.get("labelIds", [])
                payload = msg_data.get("payload", {})
                headers = payload.get("headers", [])

                timestamp = msg_data.get("internalDate", "")
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
                sender = next(
                    (h["value"] for h in headers if h["name"] == "From"), "(No Sender)")
                to = next((h['value']
                        for h in headers if h['name'] == 'Delivered-To'), None)
                snippet = msg_data.get("snippet", "").replace('\u200c', '').replace(
                    '\u034f', '').replace('\u200f', '').replace('\xa0', '').replace('\ufeff', '').strip()
                body = EmailFetcher._extract_email_body(payload)

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

                categorizer = EmailCategorizer(email_data)

                category = categorizer.categorize()

                email_data["category"] = category

                emails_list.append(email_data)

                service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()

            return emails_list
        
        except HttpError as e:
            raise Exception(f"Error fetching emails: {e}")

    def fetch_emails(self) -> List[Email]:
        return self._list_latest_emails()
