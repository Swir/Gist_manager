from pathlib import Path

from PIL import Image, ImageDraw


SIZES = (16, 24, 32, 48, 64, 128, 256)
OUT = Path("build/gist-manager.ico")


def make_icon(size=256):
    scale = size / 256.0
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    def box(coords, radius, fill, outline=None, width=1):
        xy = tuple(int(v * scale) for v in coords)
        draw.rounded_rectangle(
            xy,
            radius=max(1, int(radius * scale)),
            fill=fill,
            outline=outline,
            width=max(1, int(width * scale)),
        )

    box((8, 8, 248, 248), 52, "#08101D", "#1E3154", 8)
    box((53, 77, 203, 189), 16, "#0D1426", "#1F8FFF", 8)

    r = max(2, int(7 * scale))
    for x, color in ((76, "#55B8FF"), (100, "#1F8FFF")):
        cx, cy = int(x * scale), int(103 * scale)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)

    stroke = max(2, int(10 * scale))
    left = [(92, 129), (72, 145), (92, 161)]
    right = [(164, 129), (184, 145), (164, 161)]
    slash = [(143, 120), (113, 171)]
    draw.line([(int(x * scale), int(y * scale)) for x, y in left], fill="#EAF2FF", width=stroke, joint="curve")
    draw.line([(int(x * scale), int(y * scale)) for x, y in right], fill="#EAF2FF", width=stroke, joint="curve")
    draw.line([(int(x * scale), int(y * scale)) for x, y in slash], fill="#EAF2FF", width=stroke)

    box((77, 201, 179, 209), 4, "#1F8FFF")
    return image


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base = make_icon(256)
    base.save(OUT, format="ICO", sizes=[(s, s) for s in SIZES])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
