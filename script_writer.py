import json
import os
from dotenv import load_dotenv

load_dotenv()

# Rejim: "mock" (test, bepul) yoki "real" (Claude API, pullik)
MODE = "mock"  # Kalit kelganda shu yerni "real" ga o'zgartirasan


def generate_content_mock(topic: str, category: str) -> dict:
    """
    Bu funksiya Claude'ni CHAQIRMAYDI — faqat sinov uchun
    qo'lda tayyorlangan namuna javob qaytaradi.
    Real funksiya bilan bir xil JSON tuzilmasini beradi,
    shuning uchun qolgan kod (Telegram, Video) buni farqlamaydi.
    """
    return {
        "telegram_post": f"🤖 {topic} haqida qiziqarli fakt! Bu — {category} sohasidagi eng so'nggi yangilik. #AI #Texnologiya #Uzbekistan",
        "shorts_hook": f"Bilasizmi, {topic} butunlay o'zgartirib yubordi!",
        "shorts_main": f"{topic} qanday ishlashini va nima uchun bu muhimligini tushuntiramiz. Bu texnologiya kelajakda yanada rivojlanadi.",
        "shorts_outro": "Ko'proq bilish uchun kanalga obuna bo'ling!",
        "youtube_title": f"{topic} — Bilishingiz kerak bo'lgan narsa",
        "youtube_description": f"{topic} haqida qisqa va tushunarli video. #AI #Tech",
        "youtube_tags": ["AI", "texnologiya", "uzbekistan", topic.lower()]
    }


def generate_content_real(topic: str, category: str) -> dict:
    """
    Bu — HAQIQIY Claude API chaqiruvi.
    Faqat API kalit tayyor bo'lgach ishlatiladi.
    """
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""
'{topic}' mavzusida ({category} sohasida) quyidagilarni yoz:
1. Telegram post (300 belgidan kam, emoji va hashtag bilan)
2. YouTube Shorts skripti (40-45 soniyalik, HOOK/MAIN/OUTRO qismlarga bo'lingan, o'zbek tilida)
3. YouTube video sarlavhasi va tavsifi

Javobni FAQAT JSON formatida qaytar, boshqa hech narsa yozma:
{{
  "telegram_post": "...",
  "shorts_hook": "...",
  "shorts_main": "...",
  "shorts_outro": "...",
  "youtube_title": "...",
  "youtube_description": "...",
  "youtube_tags": ["tag1", "tag2"]
}}
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)


def generate_content(topic: str, category: str) -> dict:
    """
    Asosiy funksiya — MODE ga qarab mock yoki real ishlatadi.
    Boshqa kodlar (Telegram, Video) faqat shu funksiyani chaqiradi,
    ichida nima bo'layotgani bilan ishlari yo'q.
    """
    if MODE == "mock":
        return generate_content_mock(topic, category)
    else:
        return generate_content_real(topic, category)


if __name__ == "__main__":
    result = generate_content("Claude AI'ning yangi imkoniyatlari", "AI/texnologiya")
    print(json.dumps(result, indent=2, ensure_ascii=False))

TOPICS_ROTATION = [
    ("Yangi AI modellar va vositalar", "AI/texnologiya"),
    ("AI yordamida pul topish usullari", "AI/texnologiya"),
    ("Python dasturlash maslahatlari", "AI/texnologiya"),
    ("AI vositalar sharhi", "AI/texnologiya"),
    ("Kelajak texnologiyalari", "AI/texnologiya"),
]

def get_today_content(day_index: int) -> dict:
    topic, category = TOPICS_ROTATION[day_index % len(TOPICS_ROTATION)]
    return generate_content(topic, category)