from email_agents.email_agent import email_assistant
from agents import Runner
import chainlit as cl

async def run_agent(user_input: str):
    result = await Runner.run(email_assistant, input=user_input)
    final_output = result.final_output
    print(final_output)
    return final_output

@cl.on_message
async def on_message(message: cl.Message):
    try:
        result = await run_agent(message.content)
        await cl.Message(content=result).send()
    except Exception as e:
        await cl.Message(content=f"Error: {e}").send()