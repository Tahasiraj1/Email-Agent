from fetcher import EmailFetcher
from replier import EmailReplier
from drafter import EmailDrafter
from processor import EmailProcessor
from agents import function_tool
import chainlit as cl

@function_tool
async def process_emails_pipeline():
    fetcher = EmailFetcher()
    replier = EmailReplier()
    drafter = EmailDrafter()

    async def send_message_to_chat(message: str):
        await cl.Message(content=message).send()

    processor = EmailProcessor(fetcher, replier, drafter, send_message=send_message_to_chat)
    await processor.process_emails()