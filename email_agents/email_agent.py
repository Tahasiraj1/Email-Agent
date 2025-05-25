from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, function_tool
from processor import EmailProcessor
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
    processor = EmailProcessor()
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

result = Runner.run_sync(email_assistant, 
input="""I'm interested in this job and I've expereince in FrontEnd Development, I specializes in TypeScript, React, Next.js, Node.js, Tailwind CSS, and MongoDB Atlas, I'm not graduate but I've made real-world projects. Their post: We're Hiring: Junior Frontend Developer (Fresh Graduates Welcome!)

Are you passionate about web development and ready to kickstart your tech career? We're looking for a Junior Frontend Developer to join our team and grow with us!

Experience: 0–6 months
Location: Karachi, Pakistan.
Employment Type: Contract/ Full -Time

Tech Stack:
- React.js (must have)
- MUI (Material UI)
- HTML5, CSS3

Nice to Have:
- Basic knowledge of Node.js or backend fundamentals 

What We’re Looking For:
- Strong eagerness to learn and adapt
- Good understanding of modern frontend development
- Team player with problem-solving attitude

Perks:
- Great mentorship and growth opportunities
- Flexible work environment
- Exposure to real-world projects from day one

How to Apply: Send your resume and portfolio (if any) to hr@webxsquare.com with the subject line “Junior Frontend Developer – Application.""")
print("Summary: ", result.final_output)