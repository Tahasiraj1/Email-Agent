from googleapiclient.errors import HttpError
from .email_builder import NewEmailBuilder
from dataclasses import dataclass
import base64

@dataclass
class NewEmailManager:
    to: str
    subject: str
    body: str
    attachments: list = None

    def __post_init__(self):
        self.builder = NewEmailBuilder(
            to=self.to, 
            subject=self.subject, 
            reply_text=self.body, 
            attachments=self.attachments
        )

    def compose_email(self) -> str:
        """Compose an email."""
        try:
            email, service = self.builder.structure()
            
            raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode()

            sent_msg = service.users().messages().send(
                userId='me',
                body={
                    'raw': raw_message
                }
            ).execute()

            return sent_msg
        except HttpError as e:
            raise Exception(f"Error sending email: {e}")
        

    def draft(self):
        try:
            email, service = self.builder.structure()

            raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode()
            draft_body = {'message': {'raw': raw_message}}
            return service.users().drafts().create(userId='me', body=draft_body).execute()
        except HttpError as e:
            raise Exception(f"Error Drafting New Email: {e}")