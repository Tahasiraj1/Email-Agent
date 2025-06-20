from email_modules.processor import EmailProcessor
from email_modules.fetcher import EmailFetcher
from email_modules.replier import EmailReplier
from email_modules.drafter import EmailDrafter
from agents import function_tool
from utils.message_collector import MessageCollector

@function_tool
async def process_emails_pipeline():
    try:
        fetcher = EmailFetcher()
        replier = EmailReplier()
        drafter = EmailDrafter()
        collector = MessageCollector()

        processor = EmailProcessor(fetcher, replier, drafter, collector)
        await processor.process_emails()
        
        return "\n".join(collector.get_messages())
    except Exception as e:
        raise Exception(f"Error processing emails: {e}")