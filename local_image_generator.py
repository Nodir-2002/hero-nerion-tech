from PIL import Image, ImageDraw, ImageFont
import random
import os

COLOR_THEMES = [
    ((25, 25, 55), (90, 45, 130)),
    ((10, 45, 75), (20, 130, 160)),
    ((55, 20, 40), (160, 45, 65)),
    ((15, 55, 40), (35, 150, 110)),
    ((45, 15, 60), (130, 60, 150)),
    ((60, 40, 10), (180, 120, 30)),
]

ICONS_FOLDER = "icons"
ICON_FILES = ["robot.png", "brain.png", "rocket.png", "bulb.png", "chart.png", "gear.png"]


def get_font(size: int):
    font_candidates = [
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "DejaVuSans-Bold.ttf",
    ]
    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()


def create_gradient_background(width: int, height: int, color1, color2) -> Image:
    base = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def paste_random_icon(img: Image, width: int, top_y: int = 90, icon_size: int = 180):
    """
    icons/ papkasidan tasodifiy ikonkani tanlab,
    rasmning yuqori-markaziy qismiga shaffof fon bilan joylashtiradi.
    """
    available_icons = [f for f in ICON_FILES if os.path.exists(os.path.join(ICONS_FOLDER, f))]

    if not available_icons:
        print("⚠️ icons/ papkasida ikonka topilmadi, dekoratsiyasiz davom etiladi")
        return

    icon_name = random.choice(available_icons)
    icon_path = os.path.join(ICONS_FOLDER, icon_name)

    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((icon_size, icon_size), Image.LANCZOS)

    x = (width - icon_size) // 2
    img.paste(icon, (x, top_y), icon)  # ikonkaning o'zi mask sifatida ishlatiladi (shaffoflik saqlanadi)


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > max_width:
            if current_line:
                lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def create_topic_image(text: str, save_path: str = "generated_image.jpg",
                        width: int = 1080, height: int = 1080):
    color1, color2 = random.choice(COLOR_THEMES)
    img = create_gradient_background(width, height, color1, color2).convert("RGBA")
    draw = ImageDraw.Draw(img)

    max_text_width = width - 160

    font_size = 80
    while font_size > 30:
        font = get_font(font_size)
        lines = wrap_text(draw, text, font, max_text_width)
        total_height = len(lines) * (font_size + 20)
        if len(lines) <= 4 and total_height < height - 380:
            break
        font_size -= 5

    # Ikonkani yuqoriga joylashtirish
    paste_random_icon(img, width, top_y=90, icon_size=180)

    total_text_height = len(lines) * (font_size + 20)
    y_start = 350

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        y = y_start + i * (font_size + 20)

        draw.text((x + 3, y + 3), line, fill=(0, 0, 0, 160), font=font)
        draw.text((x, y), line, fill="white", font=font)

    img = img.convert("RGB")
    img.save(save_path, quality=92)
    print(f"✅ Rasm yaratildi: {save_path} (shrift o'lchami: {font_size}px)")
    return save_path


if __name__ == "__main__":
    create_topic_image("Claude AI imkoniyatlari haqida bilishingiz kerak bo'lgan narsalar", "test_generated.jpg")