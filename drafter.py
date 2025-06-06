from email_builder import ReplyDraftEmailBuilder
from googleapiclient.errors import HttpError
import base64


class EmailDrafter:
    def draft_email(self, email_id: str, reply_text: str) -> str:
        """Draft an email."""
        try:
            builder = ReplyDraftEmailBuilder(email_id=email_id, reply_text=reply_text)
            draft, service, _ = builder.structure()

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
        except HttpError as e:
            raise Exception(f"Error Drafting: {e}")