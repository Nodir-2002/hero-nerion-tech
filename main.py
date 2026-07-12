import asyncio
import datetime
from script_writer import generate_content, TOPICS_ROTATION
from local_image_generator import create_topic_image
from telegram_publisher import send_text_post, send_photo_post


async def run_daily_telegram_post():
    index = get_current_topic_index()
    topic, category = TOPICS_ROTATION[index % len(TOPICS_ROTATION)]
    
    # Bugungi kun tartib raqamiga qarab mavzu tanlanadi
    day_index = datetime.datetime.now().timetuple().tm_yday  # yilning nechanchi kuni
    topic, category = TOPICS_ROTATION[day_index % len(TOPICS_ROTATION)]

    print(f"📌 Bugungi mavzu: {topic}")

    # 1. Matn tayyorlash (hozircha mock rejimda)
    content = generate_content(topic, category)
    print(f"✍️ Post matni tayyor:\n{content['telegram_post']}\n")

    # 2. Mavzuga mos rasm yaratish (mahalliy, internetga bog'liq emas)
    image_path = create_topic_image(topic, "daily_image.jpg")

    # 3. Telegram'ga yuborish
    if image_path:
        success = await send_photo_post(content["telegram_post"], image_path)
    else:
        print("⚠️ Rasm yaratilmadi, faqat matn yuboriladi")
        success = await send_text_post(content["telegram_post"])

    if success:
        print("🎉 Kunlik post muvaffaqiyatli yuborildi!")
    else:
        print("❌ Post yuborishda xatolik yuz berdi")


if __name__ == "__main__":
    asyncio.run(run_daily_telegram_post())
import datetime

def get_current_topic_index():
    now = datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday
    hour_slot = 0 if now.hour < 8 else (1 if now.hour < 14 else 2)  # ertalab/kunduzi/kechqurun
    return day_of_year * 3 + hour_slot