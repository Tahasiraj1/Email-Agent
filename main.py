from fetcher import EmailFetcher
from tools.summarize import summarize_email
from tools.reply_generator import generate_reply

if __name__ == "__main__":
    fetcher = EmailFetcher()
    emails = fetcher.fetch_emails()

    for email in emails:
        summary = summarize_email(email)
        reply = generate_reply(email, summary)
        print(f"Email: {email}")
        print(f"Summary: {summary}")
        print(f"Reply: {reply}")
