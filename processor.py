from tools.summarize import summarize_email
from tools.reply_generator import generate_email_content
import time


class EmailProcessor:
    def __init__(self, fetcher, replier, drafter, time_interval=60):
        self.fetcher = fetcher
        self.replier = replier
        self.drafter = drafter
        self.time_interval = time_interval
        self.emails = []

    def process_emails(self):
        try:
            self.emails = self.fetcher.fetch_emails()

            for email in self.emails:
                if 'Urgent'.lower() in email['category'].lower():
                    summary = summarize_email(email)
                    reply = generate_email_content(email=email, summary=summary)
                    print(f"Replying to email ID: {email['email_id']}")
                    print(f"Reply content: {reply}")
                    message = self.replier.reply_to_email(
                        email["email_id"], reply)
                    print("\nReply: ", reply, "\n Message: ", message)

                elif 'Draft'.lower() in email['category'].lower():
                    summary = summarize_email(email)
                    reply = generate_email_content(email=email, summary=summary)
                    draft = self.drafter.draft_email(email["email_id"], reply)
                    print("\Reply: ", reply, "\n Draft: ", draft)

                elif 'Important'.lower() in email['category'].lower():
                    summary = summarize_email(email)
                    reply = generate_email_content(email=email, summary=summary)
                    message = self.drafter.draft_email(
                        email["email_id"], reply)
                    print("\nReply: ", reply, "\n Message: ", message)
                else:
                    print("\Spam email: ", email)

            else:
                print("No emails found.")
        except Exception as e:
            print(f"Error: {e}")
