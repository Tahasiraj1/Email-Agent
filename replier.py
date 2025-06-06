from email_builder import ReplyDraftEmailBuilder
from googleapiclient.errors import HttpError
import base64

class EmailReplier:
    def reply_to_email(self, email_id: str, reply_text: str) -> str:
        """Send a proper reply to an email using the original message metadata."""
        try:
            builder = ReplyDraftEmailBuilder(email_id=email_id, reply_text=reply_text)
            reply, service, thread_id = builder.structure()

            raw_message = base64.urlsafe_b64encode(reply.as_bytes()).decode()
            sent_msg = service.users().messages().send(
                userId='me',
                body={
                    'raw': raw_message,
                    'threadId': thread_id
                }
            ).execute()

            return sent_msg
        
        except HttpError as e:
            raise Exception(f"Error Replying: {e}")
