#!/usr/bin/env python3
"""
Pre-generates match data for the JAM viewer to avoid client-side computation.
Run this after OCR-ing pages or updating the artists_space.json file.
"""

import json
import os
import re
from pathlib import Path

def normalize(s):
    """Normalize text for matching."""
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9\s]', '', s.lower())).strip()

def main():
    # Load artists space data
    with open('artists_space.json', 'r') as f:
        artists_data = json.load(f)

    print(f"Loaded {len(artists_data)} Artists Space entries")

    # Blocklist for false positives
    blocklist = {
        'artist', 'artists', 'young', 'black', 'white', 'brown', 'green',
        'art', 'arts', 'film', 'video', 'music', 'dance', 'space', 'gallery',
        'museum', 'project', 'group', 'exhibition', 'work', 'works', 'series'
    }

    # Result structures
    page_texts = {}
    page_match_counts = []
    artist_to_pages = {}

    # Process each page
    text_dir = Path('text')
    total_pages = 159

    for i in range(1, total_pages + 1):
        text_file = text_dir / f'page-{i}.txt'

        if not text_file.exists():
            page_texts[i] = ''
            page_match_counts.append(0)
            continue

        with open(text_file, 'r') as f:
            text = f.read()

        page_texts[i] = text
        normalized_text = normalize(text)

        # Find matches
        matches = []
        seen = set()

        for entry in artists_data:
            for form in entry['forms']:
                # Skip short forms
                if len(form) < 8:
                    continue

                # Skip if form is just blocklisted words
                words = form.split(' ')
                if all(w in blocklist for w in words):
                    continue

                # Use word boundary matching
                pattern = r'\b' + re.escape(form) + r'\b'
                if re.search(pattern, normalized_text, re.IGNORECASE):
                    if entry['original'] not in seen:
                        seen.add(entry['original'])
                        matches.append({
                            'original': entry['original'],
                            'matchedForm': form
                        })

                        # Track which pages each artist appears on
                        if form not in artist_to_pages:
                            artist_to_pages[form] = []
                        artist_to_pages[form].append(i)
                        break

        page_match_counts.append(len(matches))

        if i % 20 == 0:
            print(f"Processed {i}/{total_pages} pages...")

    # Calculate max match count
    max_match_count = max(page_match_counts) if page_match_counts else 1

    # Create output data
    output = {
        'pageTexts': page_texts,
        'pageMatchCounts': page_match_counts,
        'artistToPages': artist_to_pages,
        'maxMatchCount': max_match_count,
        'totalPages': total_pages
    }

    # Write output
    with open('precomputed_data.json', 'w') as f:
        json.dump(output, f)

    # Calculate size
    size_mb = os.path.getsize('precomputed_data.json') / (1024 * 1024)
    print(f"\nGenerated precomputed_data.json ({size_mb:.2f} MB)")
    print(f"Max matches on a single page: {max_match_count}")
    print(f"Total artist forms with matches: {len(artist_to_pages)}")

if __name__ == '__main__':
    main()
