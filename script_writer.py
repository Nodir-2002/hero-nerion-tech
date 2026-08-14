import json
import os
import random
from dotenv import load_dotenv

load_dotenv()

MODE = "real"

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

# Har bir post turi uchun turli "burchak" (angle) — takrorlanishni kamaytirish uchun
CONTENT_ANGLES = [
    "amaliy maslahat va qadamlar bilan",
    "statistika va real raqamlar bilan",
    "keng tarqalgan xato/noto'g'ri tushuncha va uni tuzatish orqali",
    "kelajakdagi tendensiya va bashorat sifatida",
    "boshlang'ich uchun sodda tushuntirish orqali",
    "real hayotiy misol yoki case-study orqali",
]





def generate_content_real(topic: str, category: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    angle = random.choice(CONTENT_ANGLES)

    system_prompt = """Sen O'zbekistondagi eng mashhur IT/texnologiya Telegram kanali uchun professional kontent yozuvchisan. 

Sening auditoriyang: 18-35 yoshli, IT sohasiga qiziquvchi, dasturchi bo'lish yoki frilanserlikda pul topishni xohlaydigan o'zbek yoshlari.

Qoidalaring:
- Har doim ANIQ faktlar, raqamlar yoki real misollar bilan yoz — umumiy gaplardan qoch
- Tabiiy, jonli o'zbek tilida yoz (rasmiy-kitobiy til emas, lekin professional)
- Har bir post o'quvchiga YANGI narsa o'rgatsin — "hamma biladigan" gaplarni takrorlama
- Clickbait emas, lekin qiziqarli va e'tiborni tortadigan sarlavha/hook yoz
- Texnik atamalarni ishlatsang, qisqacha tushuntirib ket (auditoriya boshlang'ich bo'lishi mumkin)
"""

    user_prompt = f"""Mavzu: {topic}
Kategoriya: {category}
Post uslubi: {angle}

Quyidagilarni yoz:

1. TELEGRAM POST (250-400 belgi):
   - Diqqatni tortadigan ochilish jumlasi
   - 1-2 ta ANIQ fakt, raqam yoki misol (o'ylab topma, umumiy ma'lumotlarga tayan)
   - Qisqa, kuchli xulosa yoki chaqiruv
   - 2-3 ta mos emoji (ortiqcha emas)
   - Oxirida 3-4 ta hashtag

2. YOUTUBE SHORTS SKRIPTI (40-45 soniya, taxminan 100-120 so'z):
   - HOOK (birinchi 3 soniya — juda kuchli, tomoshabinni to'xtatadigan)
   - MAIN (asosiy qism — 1 ta aniq g'oya, chuqur emas lekin foydali)
   - OUTRO (chaqiruv — obuna, izoh, ulashish)

3. YOUTUBE METADATA:
   - Sarlavha (60 belgidan kam, qiziqarli, lekin aniq)
   - Tavsif (2-3 jumla + hashtag)
   - Teglar (5-7 ta, izlash uchun qulay so'zlar)

Javobni FAQAT quyidagi JSON formatida qaytar, boshqa hech qanday matn, izoh yoki markdown belgisi qo'shma:
{{
  "telegram_post": "...",
  "shorts_hook": "...",
  "shorts_main": "...",
  "shorts_outro": "...",
  "youtube_title": "...",
  "youtube_description": "...",
  "youtube_tags": ["tag1", "tag2", "..."]
}}"""


       
        )

        text_blocks = [block.text for block in msg.content if block.type == "text"]
        if not text_blocks:
            raise ValueError("Javobda matn bloki topilmadi")

        text = text_blocks[0].strip().replace("```json", "").replace("```", "")
        start = text.find("{")
        end = text.rfind("}") + 1
        json_text = text[start:end]

        result = json.loads(json_text)

        # Minimal validatsiya — bo'sh maydonlar bo'lsa fallback
        required_keys = ["telegram_post", "shorts_hook", "shorts_main", "shorts_outro"]
        if not all(result.get(k) for k in required_keys):
            raise ValueError("Javobda kerakli maydonlar to'liq emas")

        return result

    except Exception as e:
        print(f"⚠️ Claude API xatolik: {e}")
        print("Mock rejimga o'tilmoqda...")
        return generate_content_mock(topic, category)


def generate_content(topic: str, category: str) -> dict:
    if MODE == "mock":
        return generate_content_mock(topic, category)
    else:
        return generate_content_real(topic, category)


def get_today_content(day_index: int) -> dict:
    topic, category = TOPICS_ROTATION[day_index % len(TOPICS_ROTATION)]
    return generate_content(topic, category)


if __name__ == "__main__":
    result = generate_content("Claude AI'ning yangi imkoniyatlari", "AI/texnologiya")
    print(json.dumps(result, indent=2, ensure_ascii=False))
