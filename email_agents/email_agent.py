from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from tools.fetch_unread import list_emails
from tools.summarize import summarize_email
from tools.send_reply import reply_to_email
from tools.draft_reply import draft_reply_to_email
import os

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
    instructions="You are an email assistant. Help users manage and understand their inbox. You can use the following tools to help you: list_emails, summarize_email, reply_to_email, draft_reply_to_email",
    model=model,
    tools=[list_emails, summarize_email, reply_to_email, draft_reply_to_email],
)

result = Runner.run_sync(email_agent, input="Summarize the latest email from my inbox.")
print("Summary: ", result.final_output)


