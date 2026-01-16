# JAM Catalogue × Artists Space Viewer

(Vibe-engineered)

A web-based viewer for the Just Above Midtown (JAM) Gallery catalogue that cross-references artists with the "5000 Artists Return to Artists Space" dataset.

## Overview

This tool displays scanned pages from the JAM catalogue alongside OCR-extracted text, automatically highlighting artists who also appeared in Artists Space exhibitions. It provides a visual timeline showing the density of artist matches across all 159 pages.

## Features

- **Page Viewer**: Side-by-side display of OCR text and original scanned page images
- **Artist Matching**: Automatically identifies Artists Space artists mentioned in the catalogue
- **Timeline Bar**: Visual histogram showing match density across all pages
- **Global Search**: Search across all pages with results shown as markers on timeline
- **Pan/Zoom**: Interactive image viewing with mouse wheel zoom and drag to pan
- **Artist Index**: Alphabetical list of all matched artists with page frequency bars
- **Persistent Selection**: Artist and search selections persist across page navigation

## File Structure

```
jam_viewer/
├── index.html           # Main application (single-file HTML/CSS/JS)
├── build_data.py        # Pre-generates match data from OCR text
├── artists_space.json   # Artists Space dataset with name variations
├── precomputed_data.json # Generated match data (run build_data.py)
├── pages/               # Scanned page images (page-001.jpg to page-159.jpg)
└── text/                # OCR text files (page-1.txt to page-159.txt)
```

## Setup

1. Ensure page images are in `pages/` directory (format: `page-001.jpg`)
2. Ensure OCR text files are in `text/` directory (format: `page-1.txt`)
3. Place `artists_space.json` in the root directory
4. Run the build script to generate precomputed data:
   ```bash
   python build_data.py
   ```
5. Serve the directory with any HTTP server:
   ```bash
   python -m http.server 8000
   ```
6. Open `http://localhost:8000` in a browser

## Usage

- **Navigate**: Use arrow buttons, keyboard arrows, or click on the timeline
- **Search**: Type in search box and press Enter; results appear as orange markers
- **Select Artist**: Click artist name in text or index panel; pages highlight in gold
- **Clear Selection**: Click × on the badge or select a different artist
- **Zoom Image**: Scroll wheel to zoom, drag to pan, double-click to reset

## Data Format

### artists_space.json
```json
[
  {
    "original": "Artist Name",
    "forms": ["artist name", "a name", "name artist"]
  }
]
```

### precomputed_data.json (generated)
```json
{
  "pageTexts": { "1": "text...", "2": "text..." },
  "pageMatchCounts": [3, 0, 5, ...],
  "artistToPages": { "artist name": [1, 45, 89] },
  "maxMatchCount": 12,
  "totalPages": 159
}
```

## Dependencies

- [Panzoom](https://github.com/timmywil/panzoom) v4.5.1 (loaded via CDN)

## About JAM

Just Above Midtown (JAM) was a pioneering New York gallery founded by Linda Goode Bryant in 1974, dedicated to exhibiting work by African American artists and artists of color. The gallery operated at three locations in Midtown, Tribeca, and SoHo until 1986.
