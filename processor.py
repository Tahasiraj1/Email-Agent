from tools.summarize import summarize_email
from tools.reply_generator import generate_email_content

class EmailProcessor:
    def __init__(self, fetcher, replier, drafter, send_message=None):
        self.fetcher = fetcher
        self.replier = replier
        self.drafter = drafter
        self.send_message = send_message or (lambda msg: print(msg))
        self.emails = []

    async def process_emails(self):
        try:
            self.emails = self.fetcher.fetch_emails()

            if not self.emails:
                await self.send_message("✅ No unread emails found.")
                return

            for email in self.emails:
                try:
                    await self.send_message(f"📧 Processing email: {email['subject']} (Category: {email['category']})")

                    if 'Urgent'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.send_message(f"✅ Replied to email ID: {email['email_id']} with reply: {reply}")

                    elif 'Draft'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.send_message(f"✅ Drafted email ID: {email['email_id']} with reply: {reply}")

                    elif 'Important'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.send_message(f"✅ Drafted email ID: {email['email_id']} with reply: {reply}")

                    else:
                        await self.send_message(f"❌ Skipping email ID: {email['email_id']} with category: {email['category']}")
                        
                except Exception as e:
                    await self.send_message(f"❌ Failed to process email ID {email['email_id']}: {e}")

            else:
                await self.send_message("✅ Finished processing all emails.")
        except Exception as e:
            await self.send_message(f"❌ Critical Error during processing: {e}")
