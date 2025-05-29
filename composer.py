from googleapiclient.discovery import build
from email.mime.text import MIMEText
from services.auth import authenticate
import base64

class EmailComposer:
    @authenticate
    def compose_email(self, to: str, subject: str, body: str, creds=None) -> str:
        """Compose an email."""
        service = build('gmail', 'v1', credentials=creds)

        # Step 1: Create MIME reply
        email = MIMEText(body)
        email['To'] = to
        email['from'] = 'tahasiraj242@gmail.com'    # Default sender
        email['Subject'] = subject

        # Step 2: Encode and send
        raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode()

        sent_msg = service.users().messages().send(
            userId='me',
            body={
                'raw': raw_message
            }
        ).execute()

        return sent_msg