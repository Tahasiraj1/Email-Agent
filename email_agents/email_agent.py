from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from tools.fetch_unread import fetch_emails
from tools.summarize import summarize_email
from tools.send_reply import reply_to_email
from tools.draft_reply import generate_reply, draft_email
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

fetch_agent = Agent(
    name="Fetch Emails",
    instructions="You are an email assistant, you can fetch emails from my inbox.",
    model=model,
    tools=[fetch_emails],
)

summarize_agent = Agent(
    name="Summarize Email",
    instructions="You are an email assistant, you can summarize emails from my inbox.",
    model=model,
    tools=[summarize_email],
)

reply_agent = Agent(
    name="Reply to Email",
    instructions="You are an email assistant, you can reply to emails from my inbox.",
    model=model,
    tools=[reply_to_email],
)

draft_reply = Agent(
    name="Draft Reply",
    instructions="You are an email assistant, you can generate and draft a reply to emails from my inbox.",
    model=model,
    tools=[generate_reply, draft_email],
)


triage_agent = Agent(
    name="Email Assistant",
    instructions="You are an email assistant. Help users manage and understand their inbox. You can handoff to following agents to help you: fetch_emails, summarize_email, reply_to_email, generate_reply",
    model=model,
    handoffs=[]
)

result = Runner.run_sync(triage_agent, input="Fetch and Draft a reply to the latest email from my inbox.")
print("Summary: ", result.final_output)


