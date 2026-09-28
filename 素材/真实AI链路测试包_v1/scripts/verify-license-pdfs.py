from __future__ import annotations

import os
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from pypdf import PdfReader


root = Path(os.environ["WASHCUT_PACKAGE_ROOT"])
evidence = root / "sources" / "license-evidence"
output = root / "reports" / "pdf-qa"
output.mkdir(parents=True, exist_ok=True)

names = [
    "pexels-license.pdf",
    "pexels-terms.pdf",
    "source-4822916-interior.pdf",
    "source-4822552-white-polish.pdf",
    "source-6161632-black-polish.pdf",
    "source-4243807-wide-foam.pdf",
    "source-6873499-foam.pdf",
    "source-4863265-pov.pdf",
    "source-6872072-rinse.pdf",
    "source-8469669-glass.pdf",
    "source-6873496-wheel.pdf",
]

thumbnails: list[Image.Image] = []
for name in names:
    path = evidence / name
    reader = PdfReader(str(path))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    if len(reader.pages) != 1 or len(text) < 300:
        raise RuntimeError(f"Invalid review PDF: {name}; pages={len(reader.pages)}; chars={len(text)}")

    pdf = pdfium.PdfDocument(str(path))
    image = pdf[0].render(scale=0.75).to_pil().convert("RGB")
    image.thumbnail((310, 438))
    canvas = Image.new("RGB", (330, 480), "white")
    canvas.paste(image, ((330 - image.width) // 2, 10))
    ImageDraw.Draw(canvas).text((10, 455), name, fill="black")
    thumbnails.append(canvas)

sheet = Image.new("RGB", (1320, 1440), (225, 228, 234))
for index, thumbnail in enumerate(thumbnails):
    sheet.paste(thumbnail, ((index % 4) * 330, (index // 4) * 480))

montage_path = output / "all-pexels-review-pdfs.jpg"
sheet.save(montage_path, quality=90)
print(f"verified={len(names)} montage={montage_path}")
