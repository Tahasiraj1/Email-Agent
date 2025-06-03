from email_agents.email_agent import email_assistant
from agents import Runner
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()
    try:
        result = Runner.run_streamed(email_assistant, input=message.content)
        async for event in result.stream_events():
            if event.type == 'raw_response_event' and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)
        await msg.send()
    except Exception as e:
        await msg.send(f"Error: {e}")