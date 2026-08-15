import os
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def create_topic_image(topic: str, save_path: str = "daily_image.jpg", category: str = None) -> str:
    """
    Gemini (Nano Banana) orqali mavzuga mos AI-rasm generatsiya qiladi.
    Muvaffaqiyatsiz bo'lsa None qaytaradi (main.py fallback qiladi).
    """
    prompt = (
        f"Create a modern, professional flat-design illustration representing the concept of "
        f"'{topic}'. Style: minimalist tech illustration, vibrant gradient background "
        f"(purple, blue, or teal tones), clean geometric shapes, no text or letters in the image, "
        f"square format, high quality, suitable for a tech/AI social media post."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"]
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image = image.convert("RGB")
                image.save(save_path, quality=95)
                print(f"✅ Gemini rasm yaratildi: {save_path}")
                return save_path

        print("⚠️ Gemini javobida rasm topilmadi")
        return None

    except Exception as e:
        print(f"❌ Gemini rasm generatsiya xatolik: {e}")
        return None


if __name__ == "__main__":
    create_topic_image("Claude AI imkoniyatlari", "test_gemini.jpg", category="AI/texnologiya")
