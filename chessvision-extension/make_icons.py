from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT = Path("icons")
OUTPUT.mkdir(exist_ok=True)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]

font_path = next(
    (path for path in FONT_PATHS if Path(path).exists()),
    None,
)

if font_path is None:
    raise RuntimeError("Install a TrueType font before generating icons.")

for size in (16, 48, 128):
    image = Image.new("RGBA", (size, size), (12, 22, 35, 255))
    draw = ImageDraw.Draw(image)

    # Rounded dark background with a green outline.
    margin = max(1, size // 32)
    draw.rounded_rectangle(
        (margin, margin, size - margin - 1, size - margin - 1),
        radius=max(3, size // 5),
        fill=(12, 22, 35, 255),
        outline=(16, 210, 160, 255),
        width=max(1, size // 32),
    )

    # Green arc representing movement and analysis.
    draw.arc(
        (size * 0.13, size * 0.10, size * 0.83, size * 0.88),
        start=115,
        end=285,
        fill=(16, 220, 165, 255),
        width=max(1, size // 10),
    )

    # Chess knight symbol.
    font = ImageFont.truetype(font_path, int(size * 0.68))
    symbol = "♞"
    box = draw.textbbox((0, 0), symbol, font=font)
    text_width = box[2] - box[0]
    text_height = box[3] - box[1]

    draw.text(
        ((size - text_width) / 2 - box[0],
         (size - text_height) / 2 - box[1] + size * 0.04),
        symbol,
        font=font,
        fill=(245, 249, 255, 255),
    )

    image.save(OUTPUT / f"icon{size}.png")

print("Created icons/icon16.png, icon48.png and icon128.png")
