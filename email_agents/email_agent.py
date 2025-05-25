from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool
from processor import EmailProcessor
from fetcher import EmailFetcher
from replier import EmailReplier
from drafter import EmailDrafter
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

@function_tool
def process_emails_pipeline():
    fetcher = EmailFetcher()
    replier = EmailReplier()
    drafter = EmailDrafter()
    processor = EmailProcessor(fetcher, replier, drafter)
    processor.process_emails()

email_assistant = Agent(
    name="Email Assistant",
    instructions="""
    You are a professional Email Assistant tasked with automating Gmail inbox management. 
    Your objective is to efficiently process unread emails using the following procedure:
    
    1. Fetch all unread emails from the user's inbox.
    2. For each email:
       - Determine its category (e.g., Urgent, Draft, or Other).
       - If the email category is "Urgent":
         a. Generate a concise summary of the email.
         b. Compose an appropriate reply based on the summary and email content.
         c. Immediately send the reply using the provided tools.
       - If the email category is "Draft":
         a. Generate a concise summary of the email.
         b. Compose a suitable reply draft based on the summary and email content.
         c. Save the draft reply using the provided tools.
       - If the email category is neither "Urgent" nor "Draft", skip it or notify the user.
    
    You must use the `process_emails_pipeline` tool to handle the entire workflow, including fetching emails, summarizing, determining categories, generating replies, and either sending or drafting them as appropriate. Always prioritize accuracy, conciseness, and professionalism in your communication.
    
    Do not perform redundant actions. Do not summarize, reply, or draft for emails that do not meet the "Urgent" or "Draft" criteria.
    """,
    model=model,
    tools=[process_emails_pipeline],
)

result = Runner.run_sync(email_assistant, input="Fetch latest email, and act accordingly.")
print("Summary: ", result.final_output)