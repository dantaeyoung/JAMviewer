#!/usr/bin/env python3
"""
OCR pages using Google Cloud Vision API to get text with bounding box coordinates.
Outputs JSON files with word-level coordinates for highlighting on images.

Setup:
1. pip install google-cloud-vision python-dotenv
2. Create a .env file with: GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-key.json
3. Run: python ocr_with_coords.py
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from google.cloud import vision


def ocr_page(client, image_path):
    """OCR a single page and return structured data with coordinates."""

    with open(image_path, 'rb') as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    # Get full text
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""

    # Extract word-level data with bounding boxes
    words = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])

                    # Get bounding box vertices
                    vertices = word.bounding_box.vertices
                    bbox = {
                        'x': vertices[0].x,
                        'y': vertices[0].y,
                        'width': vertices[1].x - vertices[0].x,
                        'height': vertices[2].y - vertices[0].y,
                        # Also store all 4 corners for rotated text
                        'vertices': [{'x': v.x, 'y': v.y} for v in vertices]
                    }

                    words.append({
                        'text': word_text,
                        'bbox': bbox,
                        'confidence': word.confidence
                    })

    return {
        'full_text': full_text,
        'words': words,
        'width': response.full_text_annotation.pages[0].width if response.full_text_annotation.pages else 0,
        'height': response.full_text_annotation.pages[0].height if response.full_text_annotation.pages else 0
    }


def main():
    # Check for credentials
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        print("Run: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your-key.json'")
        return

    client = vision.ImageAnnotatorClient()

    pages_dir = Path('pages')
    output_dir = Path('ocr_coords')
    output_dir.mkdir(exist_ok=True)

    # Get all page images
    page_files = sorted(pages_dir.glob('page-*.jpg'))
    total = len(page_files)

    print(f"Found {total} pages to process")

    for i, page_file in enumerate(page_files, 1):
        # Extract page number from filename (page-001.jpg -> 1)
        page_num = int(page_file.stem.split('-')[1])
        output_file = output_dir / f'page-{page_num}.json'

        # Skip if already processed
        if output_file.exists():
            print(f"[{i}/{total}] Page {page_num} already processed, skipping")
            continue

        print(f"[{i}/{total}] Processing page {page_num}...")

        try:
            result = ocr_page(client, page_file)

            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)

            word_count = len(result['words'])
            print(f"         → {word_count} words extracted")

        except Exception as e:
            print(f"         → Error: {e}")

    print("\nDone! OCR data saved to ocr_coords/")
    print("Next step: Run build_data.py to regenerate precomputed data with coordinates")


if __name__ == '__main__':
    main()
