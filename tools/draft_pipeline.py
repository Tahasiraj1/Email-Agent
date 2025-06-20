from .reply_generator import generate_email_content
from typing import List, Optional
from agents import function_tool
from email_modules.composer import NewEmailManager
from utils.message_collector import MessageCollector

@function_tool
async def draft_new_email_pipeline(to: str, subject: str, user_query: str, attachments: Optional[List[str]] = None):
    try:
        """Draft a new email, based on the provided recipient and draft text.

        Args:
            to (str): The recipient's email address, from user_query.
            subject (str): The email subject, from user_query.
            user_query (str): The user's request, based on which the email content is generated; automatically.
            attachments (list): A list of file paths to attach to the email. (Default: None)
        """
        reply = generate_email_content(user_query=user_query)
        drafter = NewEmailManager(to=to, subject=subject, body=reply, attachments=attachments)
        new_draft = drafter.draft()
        collector = MessageCollector()
        collector.collect(f"📧 New draft created to {to} with subject '{subject}':\n{reply}\n{new_draft}")
    except Exception as e:
        raise Exception(f"Error drafting email: {e}")