from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from tools.fetch_unread import fetch_emails
from tools.summarize import summarize_email
from tools.send_reply import reply_to_email
from tools.draft_reply import generate_reply
import os

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=provider,
)


email_agent = Agent(
    name="Email Assistant",
    instructions="You are an email assistant. Help users manage and understand their inbox. You can use the following tools to help you: fetch_emails, summarize_email, reply_to_email, generate_reply",
    model=model,
    tools=[fetch_emails, summarize_email, reply_to_email, generate_reply],
)

result = Runner.run_sync(email_agent, input="Fetch and Draft a reply to the latest email from my inbox.")
print("Summary: ", result.final_output)


