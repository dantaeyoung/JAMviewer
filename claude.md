# Claude Instructions for JAM Viewer

## Project Overview

This is a single-page web application for viewing the JAM (Just Above Midtown) Gallery catalogue with artist cross-referencing. The entire application lives in `index.html` with embedded CSS and JavaScript.

## Architecture

- **Single file**: All HTML, CSS, and JS in `index.html` (~1200 lines)
- **No build step**: Plain vanilla JS, no frameworks or bundlers
- **External dependency**: Panzoom library loaded via CDN for image pan/zoom
- **Data files**: JSON for artist data, pre-computed matches, and text files for OCR

## Key State Variables

```javascript
currentPage          // Current page number (1-159)
currentSearchTerm    // Active search term
selectedArtistForm   // Currently selected artist (by matched form)
searchResultPages    // Set of pages matching current search
artistToPages        // Map: artist form -> [page numbers]
pageMatchCounts      // Array of match counts per page
allPageTexts         // Cache of all OCR text
```

## Important Functions

- `loadPage(pageNum, instantScroll)` - Main page loading, handles all highlighting
- `renderPageBars()` - Renders timeline histogram
- `renderSearchMarkers()` - Adds orange search result markers
- `renderIndexList()` - Renders the All Matches sidebar
- `scrollToTargetInTextPanel(target, behavior)` - Custom scroll that doesn't affect parent containers
- `highlightArtistMatchesWithSelection()` - Highlights artists with selected one in gold

## UI Patterns

### Badges
Artist and search selections use a consistent badge pattern:
- Badge appears when selection is active
- Shows name/term with × to clear
- Uses `visibility: hidden/visible` to prevent layout shift

### Timeline Bar
- Green bars show match density (height proportional to count)
- Gold bars indicate pages with selected artist
- Orange vertical markers show search results
- White indicator shows current page

### Color Scheme
- Green (`#2d5a2d`, `#8f8`): Artist matches
- Gold (`#5a4a00`, `#da0`, `#ffd`): Selected artist
- Orange (`#5a3a1a`, `#e87d2a`, `#f0d0a0`): Search
- Dark grays (`#1a1a1a` to `#333`): Background

## Common Tasks

### Adding a new highlight type
1. Add CSS classes for the new highlight
2. Add state variable to track selection
3. Add badge HTML and update function
4. Update `loadPage()` to apply highlighting
5. Update `renderPageBars()` if it affects timeline

### Modifying the timeline
- Bar heights: Adjust formula in `renderPageBars()`
- Currently uses `40 + (count/max)*60` for 40% minimum height
- Index bars use sqrt scale for better visibility of small differences

### Scroll behavior
Always use `scrollToTargetInTextPanel()` instead of `scrollIntoView()` to prevent the nav from being pushed up.

## Gotchas

1. **Search state persistence**: Search results persist until explicitly cleared via badge ×
2. **Artist selection persistence**: Same pattern - persists across navigation
3. **Precomputed data**: Run `python build_data.py` after OCR changes
4. **Image zoom**: No containment set, allows free pan/zoom with minScale 0.5

## Testing Changes

1. Open in browser with local server (`python -m http.server`)
2. Test navigation (arrows, click timeline, keyboard)
3. Test search (enter term, click markers, clear badge)
4. Test artist selection (click in text, click in index, clear badge)
5. Check that scroll doesn't shift the header
