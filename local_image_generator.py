from PIL import Image, ImageDraw, ImageFont
import random
import os

# Turli fon ranglari (gradient effekti uchun)
COLOR_THEMES = [
    ((30, 30, 60), (80, 40, 120)),      # ko'k-binafsha
    ((10, 50, 80), (20, 120, 150)),     # ko'k
    ((60, 20, 40), (150, 40, 60)),      # to'q qizil
    ((20, 60, 40), (40, 140, 100)),     # yashil
]


def create_gradient_background(width: int, height: int) -> Image:
    color1, color2 = random.choice(COLOR_THEMES)
    base = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def create_topic_image(text: str, save_path: str = "generated_image.jpg",
                        width: int = 1080, height: int = 1080):
    """
    Mavzu nomi asosida oddiy, chiroyli rasm yaratadi.
    Telegram post uchun kvadrat (1080x1080) format.
    """
    img = create_gradient_background(width, height)
    draw = ImageDraw.Draw(img)

    # Shrift — agar maxsus shrift bo'lmasa, standart shriftdan foydalanamiz
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        font = ImageFont.load_default()

    # Matnni markazga joylashtirish uchun so'zlarni qatorlarga bo'lamiz
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > width - 100:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)

    # Matnni vertikal markazga joylashtirish
    total_text_height = len(lines) * 90
    y_start = (height - total_text_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        y = y_start + i * 90
        draw.text((x, y), line, fill="white", font=font)

    img.save(save_path, quality=90)
    print(f"✅ Rasm yaratildi: {save_path}")
    return save_path


if __name__ == "__main__":
    create_topic_image("Sun'iy Intellekt Yangiliklari", "test_generated.jpg")