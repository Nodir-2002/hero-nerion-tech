import asyncio
import datetime
from script_writer import generate_content, TOPICS_ROTATION
from local_image_generator import create_topic_image
from telegram_publisher import send_text_post, send_photo_post


def get_current_topic_index():
    """
    Kun va soatga qarab, aylanma tarzda mavzu indeksini hisoblaydi.
    Kuniga bir necha marta post qilinganda, har biri boshqa mavzuda bo'lishi uchun.
    """
    now = datetime.datetime.now()
    day_of_year = now.timetuple().tm_yday
    hour_slot = 0 if now.hour < 8 else (1 if now.hour < 14 else 2)
    return day_of_year * 3 + hour_slot


async def run_daily_telegram_post():
    index = get_current_topic_index()
    topic, category = TOPICS_ROTATION[index % len(TOPICS_ROTATION)]

    print(f"📌 Bugungi mavzu: {topic}")

    content = generate_content(topic, category)
    print(f"✍️ Post matni tayyor:\n{content['telegram_post']}\n")

    image_path = create_topic_image(topic, "daily_image.jpg")

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