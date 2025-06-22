from email_modules.processor import EmailProcessor
from email_modules.fetcher import EmailFetcher
from email_modules.replier import EmailReplier
from email_modules.drafter import EmailDrafter
from utils.redis_collector import RedisCollector
from agents import function_tool

@function_tool
async def process_emails_pipeline():
    try:
        collector = RedisCollector()
        fetcher = EmailFetcher()
        replier = EmailReplier()
        drafter = EmailDrafter()

        processor = EmailProcessor(fetcher, replier, drafter, collector)
        await processor.process_emails()
        
        return "\n".join(await collector.get_messages())
    except Exception as e:
        raise Exception(f"Error processing emails: {e}")