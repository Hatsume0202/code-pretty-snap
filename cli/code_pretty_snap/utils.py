"""Helper utilities for code-pretty-snap."""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

# Common font search paths
_FONT_PATHS = [
    # Linux
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    str(Path.home() / ".fonts"),
    str(Path.home() / ".local/share/fonts"),
    # macOS
    "/Library/Fonts",
    str(Path.home() / "Library/Fonts"),
    "/System/Library/Fonts",
    # Windows
    "C:\\Windows\\Fonts",
]

# Font family preferences in order of preference
_FONT_PREFERENCES = [
    "JetBrainsMono-Regular",
    "JetBrains Mono Regular",
    "JetBrainsMono",
    "JetBrains Mono",
    "FiraCode-Regular",
    "Fira Code Regular",
    "FiraCode",
    "Fira Code",
    "DejaVuSansMono",
    "DejaVu Sans Mono",
    "DejaVuSansMono-Bold",
    "DejaVu Sans Mono Bold",
]


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    """Convert hex color string to RGBA tuple."""
    r, g, b = _hex_to_rgb(hex_color)
    return (r, g, b, alpha)


def get_monospace_font(size: int) -> ImageFont.FreeTypeFont:
    """Try to load a monospace font, falling back through preferences.

    Attempts to load fonts from the preference list using direct name lookup
    and by searching common system font directories for matching filenames.
    Falls back to Pillow's default font if nothing else works.
    """
    # First try direct loading by name
    for font_name in _FONT_PREFERENCES:
        try:
            font = ImageFont.truetype(font_name, size)
            return font
        except (OSError, IOError):
            pass

    # Then search common font directories
    for font_dir in _FONT_PATHS:
        if not os.path.isdir(font_dir):
            continue
        for root, _dirs, files in os.walk(font_dir):
            for fname in files:
                fname_lower = fname.lower()
                # Check for any of our preferred fonts
                for pref in _FONT_PREFERENCES:
                    pref_lower = pref.lower().replace(" ", "")
                    match_name = pref_lower.replace("-regular", "").replace("-bold", "")
                    test_name = fname_lower.replace(".ttf", "").replace(".otf", "")
                    test_name = test_name.replace("-regular", "").replace("-bold", "")
                    test_name = test_name.replace(" ", "").replace("_", "")
                    if match_name == test_name:
                        try:
                            font = ImageFont.truetype(
                                os.path.join(root, fname), size
                            )
                            return font
                        except (OSError, IOError):
                            continue

    # Fall back to default
    try:
        font = ImageFont.load_default()
        return font
    except (OSError, IOError):
        # Ultimate fallback — this path is unlikely
        return ImageFont.load_default()


def draw_rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int] | tuple[int, int, int, int],
    outline: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> None:
    """Draw a rounded rectangle on a Draw object.

    Uses arc + line primitives to create the rounded corners.

    Args:
        draw: PIL ImageDraw object
        xy: (x1, y1, x2, y2) bounding box
        radius: Corner radius in pixels
        fill: Fill color as RGB or RGBA tuple
        outline: Optional outline color
        outline_width: Width of outline
    """
    x1, y1, x2, y2 = xy
    radius = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)

    if radius <= 0:
        draw.rectangle(xy, fill=fill, outline=outline, width=outline_width)
        return

    # Draw filled rounded rect using pieslice + rectangle
    # Four corners as circles
    if fill is not None:
        # Draw the four corner arcs
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
        draw.pieslice(
            [x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill
        )
        draw.pieslice(
            [x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill
        )
        draw.pieslice(
            [x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill
        )

        # Fill the center rectangle
        draw.rectangle(
            [x1 + radius, y1, x2 - radius, y2], fill=fill
        )
        # Fill the top/bottom strips between corners
        draw.rectangle(
            [x1, y1 + radius, x2, y2 - radius], fill=fill
        )

    # Draw outline if requested
    if outline is not None and outline_width > 0:
        # We draw arcs for corners and lines for edges
        draw.arc(
            [x1, y1, x1 + radius * 2, y1 + radius * 2],
            180,
            270,
            fill=outline,
            width=outline_width,
        )
        draw.arc(
            [x2 - radius * 2, y1, x2, y1 + radius * 2],
            270,
            360,
            fill=outline,
            width=outline_width,
        )
        draw.arc(
            [x1, y2 - radius * 2, x1 + radius * 2, y2],
            90,
            180,
            fill=outline,
            width=outline_width,
        )
        draw.arc(
            [x2 - radius * 2, y2 - radius * 2, x2, y2],
            0,
            90,
            fill=outline,
            width=outline_width,
        )
        # Top edge
        draw.line(
            [x1 + radius, y1, x2 - radius, y1],
            fill=outline,
            width=outline_width,
        )
        # Right edge
        draw.line(
            [x2, y1 + radius, x2, y2 - radius],
            fill=outline,
            width=outline_width,
        )
        # Bottom edge
        draw.line(
            [x1 + radius, y2, x2 - radius, y2],
            fill=outline,
            width=outline_width,
        )
        # Left edge
        draw.line(
            [x1, y1 + radius, x1, y2 - radius],
            fill=outline,
            width=outline_width,
        )


def estimate_text_width(text: str, font: ImageFont.FreeTypeFont) -> int:
    """Estimate the pixel width of text rendered with the given font.

    Uses font.getlength() when available (Pillow >= 9.0), falls back to
    font.getsize().
    """
    try:
        return int(math.ceil(font.getlength(text)))
    except (AttributeError, TypeError):
        # Fallback for older Pillow
        left, _top, right, _bottom = font.getbbox(text)
        return right - left
