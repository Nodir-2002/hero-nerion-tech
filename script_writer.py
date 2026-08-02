import json
import os
from dotenv import load_dotenv

load_dotenv()

# Rejim: "mock" (test, bepul) yoki "real" (Claude API, pullik)
MODE = "real"  # Kalit kelganda shu yerni "real" ga o'zgartirasan


import random

HOOK_TEMPLATES = [
    "Bilasizmi, {topic} sohasida hammani hayratda qoldirgan narsa bor?",
    "{topic} — bu mavzuni 90% odam noto'g'ri tushunadi!",
    "Agar siz {topic} bilan qiziqsangiz, buni albatta bilishingiz kerak.",
    "Nega hammada {topic} haqida gap ketmoqda? Keling, bilib olamiz.",
    "{topic} — kelajakni o'zgartirayotgan mavzu!",
]

MAIN_TEMPLATES = [
    "{topic} sohasida so'nggi paytda katta o'zgarishlar bo'lmoqda. Mutaxassislar bu yo'nalish yaqin kelajakda yanada rivojlanishini bashorat qilishmoqda. Buni o'rganish — hoziroq boshlash uchun ajoyib fursat.",
    "Ko'pchilik {topic} bilan tanishishni murakkab deb o'ylaydi, lekin aslida to'g'ri yondashuv bilan buni har kim o'zlashtira oladi. Asosiysi — muntazam mashq qilish va amaliyotda qo'llash.",
    "{topic} nafaqat texnologik, balki iqtisodiy jihatdan ham katta imkoniyatlar ochmoqda. Ko'plab kompaniyalar va frilanserlar bu sohadan daromad topmoqda.",
]

OUTRO_TEMPLATES = [
    "Ko'proq foydali kontent uchun kanalga obuna bo'ling! 🚀",
    "Fikringizni izohlarda yozing, muhokama qilamiz! 💬",
    "Do'stlaringiz bilan ulashing, bilim tarqatish — savob! 🙌",
]

HASHTAG_SETS = [
    "#AI #Texnologiya #Uzbekistan",
    "#SunIyIntellekt #IT #Kelajak",
    "#Python #Dasturlash #AI",
    "#Freelance #AI #Daromad",
]


def generate_content_mock(topic: str, category: str) -> dict:
    hook = random.choice(HOOK_TEMPLATES).format(topic=topic)
    main = random.choice(MAIN_TEMPLATES).format(topic=topic)
    outro = random.choice(OUTRO_TEMPLATES)
    hashtags = random.choice(HASHTAG_SETS)

    telegram_post = f"🤖 {hook}\n\n{main}\n\n{outro}\n\n{hashtags}"

    return {
        "telegram_post": telegram_post,
        "shorts_hook": hook,
        "shorts_main": main,
        "shorts_outro": outro,
        "youtube_title": f"{topic} — Bilishingiz kerak bo'lgan narsa",
        "youtube_description": f"{topic} haqida qisqa va tushunarli video. {hashtags}",
        "youtube_tags": [topic.lower(), "AI", "texnologiya", "uzbekistan"]
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

    try:
        msg = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        text_blocks = [block.text for block in msg.content if block.type == "text"]
        if not text_blocks:
            raise ValueError("Javobda matn bloki topilmadi (faqat thinking bo'lishi mumkin)")

        text = text_blocks[0].strip().replace("```json", "").replace("```", "")

        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]

        return json.loads(json_text)

    except Exception as e:
        print(f"⚠️ Claude API xatolik: {e}")
        print("Mock rejimga o'tilmoqda...")
        return generate_content_mock(topic, category)


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
    ("Claude AI imkoniyatlari", "AI/texnologiya"),
    ("ChatGPT vs Claude taqqoslash", "AI/texnologiya"),
    ("AI orqali frilanserlik", "AI/texnologiya"),
    ("Python o'rganish yo'llari", "AI/texnologiya"),
    ("Machine Learning asoslari", "AI/texnologiya"),
    ("AI vositalar bilan pul topish", "AI/texnologiya"),
    ("ChatGPT prompting sirlar", "AI/texnologiya"),
    ("AI va kelajak kasblar", "AI/texnologiya"),
    ("No-code AI vositalar", "AI/texnologiya"),
    ("AI agentlar nima va qanday ishlaydi", "AI/texnologiya"),
    ("Data Science boshlang'ich qadamlar", "AI/texnologiya"),
    ("AI bilan video yaratish", "AI/texnologiya"),
    ("GitHub Copilot va AI kod yozish", "AI/texnologiya"),
    ("AI etikasi va xavfsizligi", "AI/texnologiya"),
    ("Startaplar va AI investitsiyalar", "AI/texnologiya"),
]

def get_today_content(day_index: int) -> dict:
    topic, category = TOPICS_ROTATION[day_index % len(TOPICS_ROTATION)]
    return generate_content(topic, category)

def generate_content_real(topic: str, category: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""..."""  # o'zgarishsiz qoladi

    try:
        msg = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        text = msg.content[0].text.strip()
        # JSON qismini xavfsiz ajratib olish
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]
        return json.loads(json_text)
    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️ Claude javobini parse qilishda xatolik: {e}")
        print("Mock rejimga o'tilmoqda...")
        return generate_content_mock(topic, category)  # fallback


