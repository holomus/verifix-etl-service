from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

scheduler = AsyncIOScheduler(timezone=utc)