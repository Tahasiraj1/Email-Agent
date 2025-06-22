from .reply_generator import generate_email_content
from email_modules.composer import NewEmailManager
from agents import function_tool
from typing import List, Optional
from utils.redis_collector import RedisCollector

@function_tool
async def compose_email_pipeline(to: str, subject: str, user_query: str, attachments: Optional[List[str]] = None):
    try:
        """Compose an email, based on the provided recipient, subject, and user_query.

        Args:
            to (str): The recipient's email address.
            subject (str): The email subject.
            user_query (str): The user's request, based on which the email content is generated.
            attachments (list): A list of file paths to attach to the email. (Default: None)
        """    
        reply = generate_email_content(user_query=user_query) 
        composer = NewEmailManager(to=to, subject=subject, body=reply, attachments=attachments)
        composer.compose_email()
        collector = RedisCollector()
        await collector.collect(f"📧 Email composed to: {to} \nattachments: {attachments} \nwith subject: '{subject}'\n{reply}")
    except Exception as e:
        raise Exception(f"Error composing email: {e}")