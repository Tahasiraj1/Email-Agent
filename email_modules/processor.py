from tools.summarize import summarize_email
from tools.reply_generator import generate_email_content

class EmailProcessor:
    def __init__(self, fetcher, replier, drafter, collector):
        self.fetcher = fetcher
        self.replier = replier
        self.drafter = drafter
        self.collector = collector
        self.emails = []

    async def log(self, message: str):
        await self.collector.collect(message)
        print(message)

    async def process_emails(self):
        try:
            self.emails = self.fetcher.fetch_emails()

            if not self.emails:
                await self.log("✅ No unread emails found.")
                return

            for email in self.emails:
                try:
                    await self.log(f"📧 Processing email: {email['subject']} (Category: {email['category']})")

                    if 'Urgent'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.log(f"✅ Replied to email ID: {email['email_id']} with reply: {reply}")

                    elif 'Draft'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.log(f"✅ Drafted email ID: {email['email_id']} with reply: {reply}")

                    elif 'Important'.lower() in email['category'].lower():
                        summary = summarize_email(email)
                        reply = generate_email_content(email=email, summary=summary)
                        self.drafter.draft_email(email["email_id"], reply)
                        await self.log(f"✅ Drafted email ID: {email['email_id']} with reply: {reply}")

                    else:
                        await self.log(f"❌ Skipping email ID: {email['email_id']} with category: {email['category']}")
                        
                except Exception as e:
                    await self.log(f"❌ Failed to process email ID {email['email_id']}: {e}")

            else:
                await self.log("✅ Finished processing all emails.")
        except Exception as e:
            await self.log(f"❌ Critical Error during processing: {e}")
