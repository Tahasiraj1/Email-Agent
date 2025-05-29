from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool
from processor import EmailProcessor
from fetcher import EmailFetcher
from replier import EmailReplier
from drafter import EmailDrafter
from composer import EmailComposer
from tools.reply_generator import generate_email_content
from email_agents.instructions import COMPOSER_INSTRUCTIONS, EMAIL_ASSISTANT_INSTRUCTIONS
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

@function_tool
def compose_email_pipeline(to: str, subject: str, user_query: str):
    """Compose an email, based on the provided recipient, subject, and user_query.

    Args:
        to (str): The recipient's email address.
        subject (str): The email subject.
        user_query (str): The user's request, based on which the email content is generated.
    """
    composer = EmailComposer()
    reply = generate_email_content(user_query=user_query)
    composer.compose_email(to=to, subject=subject, body=reply)

composer_agent = Agent(
    name="Composer Agent",
    instructions=COMPOSER_INSTRUCTIONS,
    model=model,
    tools=[compose_email_pipeline]  # register the tool
)

email_assistant = Agent(
    name="Email Assistant",
    instructions=EMAIL_ASSISTANT_INSTRUCTIONS,
    model=model,
    tools=[process_emails_pipeline],
    handoffs=[composer_agent],
)

result = Runner.run_sync(email_assistant, input="Send an email to tahasiraj200@gmail.com, about the latest feature I added in my Email Agent Project, i.e Composing emails.")
print("Summary: ", result.final_output)