from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from app.services.price_monitor import check_watches

scheduler = AsyncIOScheduler()

async def run_check_job():
    print("🔍 Running scheduled price check...")
    try:
        await check_watches()
        print("✅ Price check completed.")
    except Exception as e:
        print(f"❌ Error while checking watches: {e}")

def start_scheduler():
    scheduler.add_job(run_check_job, IntervalTrigger(minutes=1))
    scheduler.start()
    print("🕒 Scheduler started (checks every 1 minutes).")