from .reply_generator import generate_email_content
from agents import function_tool
from drafter import EmailDrafter
import chainlit as cl

@function_tool
async def draft_new_email_pipeline(to: str, subject: str, user_query: str):
    """Draft a new email, based on the provided recipient and draft text.

    Args:
        to (str): The recipient's email address, from user_query.
        subject (str): The email subject, from user_query.
        user_query (str): The user's request, based on which the email content is generated; automatically.
    """
    reply = generate_email_content(user_query=user_query)
    drafter = EmailDrafter()
    new_draft = drafter.draft_new_email(to=to, draft_text=reply, subject=subject)
    await cl.Message(content=f"📧 New draft created to {to} with subject '{subject}':\n{reply}\n{new_draft}").send()

