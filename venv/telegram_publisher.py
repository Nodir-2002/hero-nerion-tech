import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


async def send_text_post(text: str) -> bool:
    """
    Oddiy matnli post yuborish.
    Muvaffaqiyatli bo'lsa True, xato bo'lsa False qaytaradi.
    """
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        print("✅ Post muvaffaqiyatli yuborildi!")
        return True
    except TelegramError as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        return False


async def send_photo_post(text: str, image_path: str) -> bool:
    """
    Rasm bilan birga post yuborish (keyingi bosqichlarda kerak bo'ladi).
    """
    try:
        bot = Bot(token=BOT_TOKEN)
        with open(image_path, "rb") as img:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=text)
        print("✅ Rasmli post muvaffaqiyatli yuborildi!")
        return True
    except TelegramError as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        return False


if __name__ == "__main__":
    # Test uchun oddiy matn yuboramiz
    test_text = "🤖 Test post — Hero Nerion Tech tizimi ishga tushmoqda!"
    asyncio.run(send_text_post(test_text))