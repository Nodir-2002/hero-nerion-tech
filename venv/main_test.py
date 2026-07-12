import asyncio
from script_writer import generate_content
from telegram_publisher import send_text_post

async def run_daily_post():
    # Mock rejimda ishlaydi (hali API kalit yo'q)
    content = generate_content("Sun'iy intellekt yangiliklari", "AI/texnologiya")
    
    print("Tayyorlangan post:")
    print(content["telegram_post"])
    print("\nYuborilmoqda...")
    
    success = await send_text_post(content["telegram_post"])
    
    if success:
        print("🎉 Butun jarayon muvaffaqiyatli yakunlandi!")

if __name__ == "__main__":
    asyncio.run(run_daily_post())