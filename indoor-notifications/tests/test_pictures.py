import io
import json
from pathlib import Path
import unittest
from PIL import Image
from indoor_notice import NoticeError, jpeg_info
from pictures import card, normalise


class PictureTests(unittest.TestCase):
    def test_normalise_fully_decodes_and_strips_metadata(self):
        image = Image.new("RGB", (1280, 720), (20, 90, 150))
        output = io.BytesIO()
        exif = Image.Exif()
        exif[270] = "private description"
        image.save(output, "JPEG", exif=exif, progressive=True)
        raw = normalise(output.getvalue())
        self.assertLessEqual(len(raw), 24576)
        self.assertEqual(jpeg_info(raw)["width"], 640)
        with Image.open(io.BytesIO(raw)) as result:
            result.load()
            self.assertEqual(result.size, (640, 360))
            self.assertEqual(dict(result.getexif()), {})
            self.assertNotIn("icc_profile", result.info)
            self.assertNotIn("comment", result.info)

    def test_invalid_oversize_or_non_jpeg_fails(self):
        output = io.BytesIO()
        Image.new("RGB", (10, 10)).save(output, "PNG")
        for raw in (b"bad", b"x" * 512001, output.getvalue()):
            with self.assertRaises((NoticeError, OSError)):
                normalise(raw)

    def test_card_uses_synthetic_data_and_fits(self):
        font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        if not font.exists():
            self.skipTest("Cyrillic test font unavailable")
        source = Path(__file__).resolve().parents[1] / "examples" / "card.json"
        result = card(json.loads(source.read_text()), font)
        self.assertEqual((jpeg_info(result)["width"], jpeg_info(result)["height"]), (640, 360))
        with Image.open(io.BytesIO(result)) as image:
            image.load()
        for data in ({}, {"title": "Title", "time": "now", "lines": ["x"] * 8},
                     {"title": "Title", "time": "now", "lines": ["W"] * 100}):
            with self.assertRaises(NoticeError):
                card(data, font)


if __name__ == "__main__":
    unittest.main()
