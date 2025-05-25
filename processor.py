from tools.summarize import summarize_email
from tools.reply_generator import generate_reply


class EmailProcessor:
    def __init__(self, fetcher, replier, drafter):
        self.fetcher = fetcher
        self.replier = replier
        self.drafter = drafter
        self.emails = []

    def process_emails(self):
        self.emails = self.fetcher.fetch_emails()

        for email in self.emails:
            if 'Urgent'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                print(f"Replying to email ID: {email['email_id']}")
                print(f"Reply content: {reply}")
                message = self.replier.reply_to_email(email["email_id"], reply)
                print("\nReply: ", reply, "\n Message: ", message)

            elif 'Draft'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                draft = self.drafter.draft_email(email["email_id"], reply)
                print("\Reply: ", reply, "\n Draft: ", draft)

            elif 'Important'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                message = self.drafter.draft_email(email["email_id"], reply)
                print("\nReply: ", reply, "\n Message: ", message)
            else:
                print("\Spam email: ", email)

        else:
            print("No emails found.")
