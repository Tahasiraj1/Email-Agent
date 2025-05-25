from tools.fetch_unread import fetch_emails
from tools.summarize import summarize_email
from tools.reply_generator import generate_reply
from tools.send_reply import reply_to_email
from tools.draft_reply import draft_email

class EmailProcessor:
    def __init__(self):
        self.emails = fetch_emails()

    def process_emails(self):
        for email in self.emails:
            if 'Urgent'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                message = reply_to_email(email["email_id"], reply)
                print("\nReply: ", reply, "\n Message: ", message)
            
            elif 'Draft'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                draft = draft_email(email["email_id"], reply)
                print("\Reply: ", reply, "\n Draft: ", draft)

            elif 'Important'.lower() in email['category'].lower():
                summary = summarize_email(email)
                reply = generate_reply(email, summary)
                message = draft_email(email["email_id"], reply)
                print("\nReply: ", reply, "\n Message: ", message)
            else:
                print("\Spam email: ", email)
        
        else:
            print("No emails found.")