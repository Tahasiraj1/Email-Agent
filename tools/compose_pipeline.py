from tools.reply_generator import generate_email_content
from composer import EmailComposer
from agents import function_tool
import chainlit as cl

@function_tool
async def compose_email_pipeline(to: str, subject: str, user_query: str):
    """Compose an email, based on the provided recipient, subject, and user_query.

    Args:
        to (str): The recipient's email address.
        subject (str): The email subject.
        user_query (str): The user's request, based on which the email content is generated.
    """
    composer = EmailComposer()
    reply = generate_email_content(user_query=user_query)
    composer.compose_email(to=to, subject=subject, body=reply)
    await cl.Message(content=f"📧 Email composed to {to} with subject '{subject}':\n{reply}").send()