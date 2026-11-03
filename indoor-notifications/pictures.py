"""Offline JPEG normalisation and status cards. Requires optional Pillow."""
import argparse
import io
import json
from pathlib import Path
import warnings

from PIL import Image, ImageDraw, ImageFont
from indoor_notice import MAX_JPEG_BYTES, NoticeError, jpeg_info

Image.MAX_IMAGE_PIXELS = 2500000


def encode(image):
    # A fresh RGB canvas strips EXIF, ICC, comments and other inherited metadata.
    image = image.convert("RGB")
    clean = Image.new("RGB", image.size)
    clean.paste(image)
    for quality in (76, 64, 52, 40, 30):
        output = io.BytesIO()
        clean.save(output, format="JPEG", quality=quality, optimize=True, progressive=False)
        raw = output.getvalue()
        if len(raw) <= MAX_JPEG_BYTES:
            jpeg_info(raw)
            return raw
    raise NoticeError("image_cannot_fit_24kib")


def normalise(raw):
    if type(raw) is not bytes or not 4 <= len(raw) <= 512000:
        raise NoticeError("input_image_size_invalid")
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(raw)) as image:
            if image.format != "JPEG" or image.width > 1920 or image.height > 1080:
                raise NoticeError("input_image_dimensions_or_format_invalid")
            image.load()
            image = image.convert("RGB")
            image.thumbnail((640, 360))
            return encode(image)


def card(data, font_path):
    if type(data) is not dict or set(data) != {"title", "time", "lines"}:
        raise NoticeError("card_fields_invalid")
    if type(data["lines"]) is not list or len(data["lines"]) > 7:
        raise NoticeError("card_lines_invalid")
    values = [data["title"], data["time"], *data["lines"]]
    if any(type(s) is not str or len(s) > 100 or any(ord(c) < 32 for c in s) for s in values):
        raise NoticeError("card_text_invalid")
    image = Image.new("RGB", (640, 360), (16, 26, 37))
    draw = ImageDraw.Draw(image)
    # Reject overflow rather than publishing a clipped status or a broken glyph.
    def text(value, y, size, colour):
        font = ImageFont.truetype(str(font_path), size)
        while draw.textlength(value, font=font) > 592 and size > 14:
            size -= 1
            font = ImageFont.truetype(str(font_path), size)
        if draw.textlength(value, font=font) > 592:
            raise NoticeError("card_line_too_wide")
        draw.text((24, y), value, font=font, fill=colour)
    text(data["title"], 18, 28, (238, 243, 249))
    text(data["time"], 57, 17, (157, 180, 197))
    draw.line((24, 87, 616, 87), fill=(54, 77, 96), width=2)
    for index, value in enumerate(data["lines"]):
        text(value, 101 + 32 * index, 22, (204, 230, 221) if index == 0 else (238, 243, 249))
    return encode(image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("normalise", "card"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--font", type=Path)
    args = parser.parse_args()
    with args.input.open("rb") as stream:
        raw = stream.read(512001 if args.mode == "normalise" else 8193)
    if args.mode == "card":
        if len(raw) > 8192 or args.font is None:
            parser.error("card requires JSON <=8192 bytes and --font with Cyrillic support")
        output = card(json.loads(raw), args.font)
    else:
        output = normalise(raw)
    # Explicit output path, no network transfer or automatic sending.
    with args.output.open("xb") as stream:
        stream.write(output)
    print(json.dumps(jpeg_info(output)))


if __name__ == "__main__":
    main()
