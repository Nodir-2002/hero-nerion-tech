from apscheduler.schedulers.blocking import BlockingScheduler
import asyncio
from main import run_daily_telegram_post


def job():
    print("⏰ Rejalashtirilgan vaqt keldi — post yuborilmoqda...")
    asyncio.run(run_daily_telegram_post())


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=18, minute=0)  # Har kuni soat 18:00

if __name__ == "__main__":
    print("🚀 Scheduler ishga tushdi.")
    print("📅 Har kuni soat 18:00 da avtomatik post yuboriladi.")
    print("To'xtatish uchun Ctrl+C bosing.\n")
    scheduler.start()