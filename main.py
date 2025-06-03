from email_agents.email_agent import email_assistant
from agents import Runner
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    input_str = message.content

    if message.elements:
        attachment_paths = [el.path for el in message.elements if hasattr(el, 'path')]
        input_str += f"\n\nAttachments: {attachment_paths}"

    try:
        result = Runner.run_streamed(email_assistant, input=input_str)
        async for event in result.stream_events():
            if event.type == 'raw_response_event' and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)
        await msg.send()
    except Exception as e:
        msg = cl.Message(content=f"Error: {e}")
        await msg.send()
