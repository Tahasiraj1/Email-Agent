from email.mime.text import MIMEText
from googleapiclient.discovery import build
from services.auth import authenticate
from models.interfaces import Email
from fetcher import EmailFetcher
from tools.reply_generator import generate_email_content
from tools.summarize import summarize_email
import base64


class EmailDrafter:
    @authenticate
    def draft_email(self, email_id: str, draft_text: Email, creds=None) -> str:
        """Draft an email."""
        service = build('gmail', 'v1', credentials=creds)

        email = service.users().messages().get(
            userId='me', id=email_id, format='metadata').execute()
        headers = {h['name']: h['value'] for h in email['payload']['headers']}

        to = headers.get('From')
        subject = headers.get('Subject', '(No Subject)')
        message_id = headers.get('Message-ID')
        thread_id = email['threadId']

        # Step 2: Create MIME reply
        draft = MIMEText(draft_text)
        draft['To'] = to
        draft['Subject'] = f"Re: {subject}"
        draft['In-Reply-To'] = message_id
        draft['References'] = message_id

        # Step 3: Encode and send
        raw_message = base64.urlsafe_b64encode(draft.as_bytes()).decode()

        draft_body = {
            'message': {
                'raw': raw_message
            }
        }

        draft = service.users().drafts().create(
            userId='me',
            body=draft_body
        ).execute()

        return draft

    @authenticate
    def draft_new_email(self, to: str, subject: str, draft_text: str, creds=None):
        service = build('gmail', 'v1', credentials=creds)
        draft = MIMEText(draft_text)
        draft['To'] = to
        draft['Subject'] = subject
        raw_message = base64.urlsafe_b64encode(draft.as_bytes()).decode()
        draft_body = {'message': {'raw': raw_message}}
        return service.users().drafts().create(userId='me', body=draft_body).execute()

if __name__ == '__main__':
    fetcher = EmailFetcher()
    emails = fetcher.fetch_emails()

    for email in emails:
        print(email)

        summary = summarize_email(email)

        reply = generate_email_content(email=email, summary=summary)
        print("\nReply: ", reply)

        drafter = EmailDrafter()
        draft = drafter.draft_email(email["email_id"], reply)
        print("\nDraft: ", draft)

        new_draft = drafter.draft_new_email(to='tahasiraj200@gmail.com', draft_text=reply, subject=email["subject"])
        print("\nNew Draft: ", new_draft)
