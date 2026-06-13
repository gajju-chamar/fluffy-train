# Shinobu Music Bot
# Owner: @Sanji_fr

import os
from PIL import Image, ImageDraw, ImageFont

THUMBNAIL_BASE = "assets/thumbnail.jpeg"
FONT_PRIMARY = "assets/font.ttf"
FONT_SECONDARY = "assets/font2.ttf"

# Text colors
COLOR_TITLE = (216, 180, 254)       # soft purple #D8B4FE
COLOR_META = (192, 132, 252)        # dimmer purple #C084FC


async def gen_thumb(title: str, duration: str, user: str) -> str:
    output_path = f"cache/thumb_{user}_{int(__import__('time').time())}.png"

    img = Image.open(THUMBNAIL_BASE).convert("RGBA")
    width, height = img.size  # expects 1280x720

    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(FONT_PRIMARY, size=42)
        font_meta = ImageFont.truetype(FONT_SECONDARY, size=26)
    except Exception:
        font_title = ImageFont.load_default()
        font_meta = ImageFont.load_default()

    # Truncate long titles
    if len(title) > 40:
        title = title[:38] + "…"

    meta_text = f"⏱ {duration}  •  By {user}"

    # Position — bottom-right block, slightly above corner
    margin_right = 60
    margin_bottom = 110

    # Measure text widths to right-align
    title_bbox = draw.textbbox((0, 0), f"🎵 {title}", font=font_title)
    meta_bbox = draw.textbbox((0, 0), meta_text, font=font_meta)

    title_w = title_bbox[2] - title_bbox[0]
    meta_w = meta_bbox[2] - meta_bbox[0]

    title_x = width - title_w - margin_right
    meta_x = width - meta_w - margin_right

    title_y = height - margin_bottom - 52
    meta_y = height - margin_bottom

    # Soft shadow for readability
    shadow_offset = 2
    draw.text(
        (title_x + shadow_offset, title_y + shadow_offset),
        f"🎵 {title}",
        font=font_title,
        fill=(0, 0, 0, 160),
    )
    draw.text(
        (meta_x + shadow_offset, meta_y + shadow_offset),
        meta_text,
        font=font_meta,
        fill=(0, 0, 0, 160),
    )

    # Main text
    draw.text((title_x, title_y), f"🎵 {title}", font=font_title, fill=COLOR_TITLE)
    draw.text((meta_x, meta_y), meta_text, font=font_meta, fill=COLOR_META)

    os.makedirs("cache", exist_ok=True)
    img.save(output_path, "PNG")

    return output_path