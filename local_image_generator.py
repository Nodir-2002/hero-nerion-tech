from PIL import Image, ImageDraw, ImageFont
import random
import os

COLOR_THEMES = [
    ((25, 25, 55), (90, 45, 130), (255, 200, 80)),   # accent: oltin
    ((10, 45, 75), (20, 130, 160), (255, 120, 90)),   # accent: korall
    ((55, 20, 40), (160, 45, 65), (255, 220, 100)),   # accent: sariq
    ((15, 55, 40), (35, 150, 110), (255, 240, 150)),  # accent: krem
    ((45, 15, 60), (130, 60, 150), (180, 255, 220)),  # accent: mint
    ((60, 40, 10), (180, 120, 30), (255, 255, 255)),  # accent: oq
]

ICONS_FOLDER = "icons"
ICON_FILES = ["robot.png", "brain.png", "rocket.png", "bulb.png", "chart.png", "gear.png"]


def get_font(size: int, bold: bool = True):
    bold_candidates = [
        "arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
    ]
    regular_candidates = [
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans.ttf",
    ]
    candidates = bold_candidates if bold else regular_candidates
    for path in candidates:
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
        # diagonalroq gradient — chapdan pastdan o'ngdan yuqoriga
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def add_decorative_circles(draw, width, height, accent_color, count=6):
    """Fonda subtle dekorativ doiralar — chuqurlik hissi uchun"""
    random.seed(hash(str(width) + str(height)) % 1000)
    for _ in range(count):
        r = random.randint(15, 60)
        x = random.randint(-30, width + 30)
        y = random.randint(-30, height + 30)
        alpha = random.randint(15, 35)
        overlay = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse([0, 0, r * 2, r * 2], fill=(*accent_color, alpha))
        draw._image.paste(overlay, (x - r, y - r), overlay)


def draw_category_badge(img, draw, text, width, accent_color, y=50):
    """Yuqorida kichik kategoriya yorlig'i (badge)"""
    font = get_font(32, bold=True)
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    padding_x, padding_y = 28, 14
    badge_w = text_w + padding_x * 2
    badge_h = text_h + padding_y * 2
    x = (width - badge_w) // 2

    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(badge)
    bdraw.rounded_rectangle([0, 0, badge_w, badge_h], radius=badge_h // 2,
                             fill=(*accent_color, 230))
    img.paste(badge, (x, y), badge)

    draw.text((x + padding_x, y + padding_y - 2), text.upper(),
               fill=(20, 20, 30), font=font)

    return y + badge_h


def paste_random_icon(img: Image, width: int, top_y: int, icon_size: int = 160):
    available_icons = [f for f in ICON_FILES if os.path.exists(os.path.join(ICONS_FOLDER, f))]
    if not available_icons:
        return top_y
    icon_name = random.choice(available_icons)
    icon_path = os.path.join(ICONS_FOLDER, icon_name)
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
    x = (width - icon_size) // 2
    img.paste(icon, (x, top_y), icon)
    return top_y + icon_size


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
                        category: str = None,
                        width: int = 1080, height: int = 1080):
    color1, color2, accent = random.choice(COLOR_THEMES)
    img = create_gradient_background(width, height, color1, color2).convert("RGBA")
    draw = ImageDraw.Draw(img)

    add_decorative_circles(draw, width, height, accent, count=8)

    current_y = 60
    if category:
        current_y = draw_category_badge(img, draw, category, width, accent, y=current_y)
        current_y += 30
    else:
        current_y = 90

    current_y = paste_random_icon(img, width, top_y=current_y, icon_size=160)
    current_y += 40

    max_text_width = width - 160
    font_size = 76
    while font_size > 30:
        font = get_font(font_size)
        lines = wrap_text(draw, text, font, max_text_width)
        total_height = len(lines) * (font_size + 22)
        if len(lines) <= 4 and current_y + total_height < height - 100:
            break
        font_size -= 4

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        y = current_y + i * (font_size + 22)
        draw.text((x + 3, y + 3), line, fill=(0, 0, 0, 160), font=font)
        draw.text((x, y), line, fill="white", font=font)

    # Pastki aksent chiziq
    line_y = height - 50
    draw.rectangle([width // 2 - 60, line_y, width // 2 + 60, line_y + 6],
                    fill=accent)

    img = img.convert("RGB")
    img.save(save_path, quality=95)
    print(f"✅ Rasm yaratildi: {save_path} (shrift: {font_size}px)")
    return save_path


if __name__ == "__main__":
    create_topic_image(
        "Claude AI imkoniyatlari haqida bilishingiz kerak bo'lgan narsalar",
        "test_generated.jpg",
        category="AI / Texnologiya"
    )