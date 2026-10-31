from PIL import Image
from pathlib import Path

source = Path("chessvision-extension/icons/icon128.png")
destination = Path("games/static/games/icons")

destination.mkdir(parents=True, exist_ok=True)

with Image.open(source) as image:
    image = image.convert("RGBA")

    for size in [192, 512]:
        resized = image.resize(
            (size, size),
            Image.Resampling.LANCZOS
        )

        resized.save(destination / f"icon{size}.png")

print("PWA icons generated successfully!")
