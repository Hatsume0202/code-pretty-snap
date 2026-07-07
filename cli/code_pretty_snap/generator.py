"""Core image generation engine for code-pretty-snap.

Uses pure Pillow to render beautiful code screenshots pixel by pixel.
"""

from __future__ import annotations

from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from pygments import lexers
from pygments.token import Token

from code_pretty_snap.themes import get_theme
from code_pretty_snap.utils import (
    draw_rounded_rect,
    estimate_text_width,
    get_monospace_font,
    hex_to_rgba,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TITLE_BAR_HEIGHT = 38
TITLE_BAR_SEPARATOR_WIDTH = 1
PADDING_TOP = 16
PADDING_SIDES = 24
PADDING_BOTTOM = 24
LINE_NUMBERS_WIDTH = 40
LINE_NUMBERS_PADDING_RIGHT = 12  # space between line numbers and code
CORNER_RADIUS = 12
SHADOW_OFFSET = 4
SHADOW_BLUR_RADIUS = 3
SHADOW_OPACITY = 0.30
SHADOW_MARGIN = 20  # extra canvas space around the window for shadow

# macOS traffic-light dot colors
DOT_CLOSE = "#FF5F57"
DOT_MINIMIZE = "#FEBC2E"
DOT_MAXIMIZE = "#28C840"
DOT_RADIUS = 6  # 12px diameter -> 6px radius
DOT_SPACING = 8
DOT_LEFT_MARGIN = 16

# ---------------------------------------------------------------------------
# Token utilities
# ---------------------------------------------------------------------------

# Mapping of Pygments token types to our theme key names.
# More specific tokens are checked first (in order of the list).
_TOKEN_MAP: list[tuple[str, str]] = [
    ("Comment.Preproc", "Comment.Special"),
    ("Comment.Special", "Comment.Special"),
    ("Comment.Single", "Comment"),
    ("Comment.Multiline", "Comment"),
    ("Comment", "Comment"),
    ("Keyword.Constant", "Keyword"),
    ("Keyword.Declaration", "Keyword"),
    ("Keyword.Namespace", "Keyword"),
    ("Keyword.Pseudo", "Keyword"),
    ("Keyword.Reserved", "Keyword"),
    ("Keyword.Type", "Keyword"),
    ("Keyword", "Keyword"),
    ("Name.Attribute", "Name.Attribute"),
    ("Name.Builtin.Pseudo", "Name.Builtin"),
    ("Name.Builtin", "Name.Builtin"),
    ("Name.Class", "Name.Class"),
    ("Name.Constant", "Name.Builtin"),
    ("Name.Decorator", "Name.Decorator"),
    ("Name.Entity", "Name"),
    ("Name.Exception", "Name.Builtin"),
    ("Name.Function.Magic", "Name.Function"),
    ("Name.Function", "Name.Function"),
    ("Name.Label", "Name"),
    ("Name.Namespace", "Name.Class"),
    ("Name.Other", "Name"),
    ("Name.Tag", "Keyword"),
    ("Name.Variable.Magic", "Name.Builtin"),
    ("Name.Variable", "Name"),
    ("String.Affix", "String"),
    ("String.Backtick", "String"),
    ("String.Char", "String"),
    ("String.Delimiter", "String"),
    ("String.Doc", "Comment"),
    ("String.Double", "String"),
    ("String.Escape", "Keyword"),
    ("String.Heredoc", "String"),
    ("String.Interpol", "String"),
    ("String.Other", "String"),
    ("String.Regex", "String"),
    ("String.Single", "String"),
    ("String.Symbol", "String"),
    ("String", "String"),
    ("Number.Bin", "Number"),
    ("Number.Float", "Number"),
    ("Number.Hex", "Number"),
    ("Number.Integer.Long", "Number"),
    ("Number.Integer", "Number"),
    ("Number.Oct", "Number"),
    ("Number", "Number"),
    ("Operator.Word", "Keyword"),
    ("Operator", "Operator"),
    ("Punctuation", "Punctuation"),
    ("Generic.Heading", "Generic.Heading"),
    ("Generic.Subheading", "Generic.Subheading"),
    # Fallback for any "Name.*" not matched above
    ("Name", "Name"),
]


def _resolve_token_color(
    token_type: Token, token_colors: dict[str, str], default_fg: str
) -> str:
    """Resolve the hex color string for a given Pygments token type.

    Walks the Pygments token type hierarchy to find the best match
    in the theme's token_colors map.
    """
    token_str = str(token_type)

    # Try the direct token string first
    if token_str in token_colors:
        return token_colors[token_str]

    # Try the mapping table
    for pyg_key, theme_key in _TOKEN_MAP:
        if pyg_key == token_str:
            if theme_key in token_colors:
                return token_colors[theme_key]
            break

    # If it's a subtype of a known key, walk the parent chain
    parts = token_str.split(".")
    for i in range(len(parts) - 1, 0, -1):
        parent = ".".join(parts[:i])
        if parent in token_colors:
            return token_colors[parent]

    # Fall back to default foreground
    return default_fg


# ---------------------------------------------------------------------------
# Code tokenization
# ---------------------------------------------------------------------------


def tokenize_code(code: str, language: str) -> list[list[tuple[str, str]]]:
    """Tokenize code into lines of (token_type_str, text) pairs.

    Args:
        code: Source code string.
        language: Pygments language alias (e.g. 'python', 'javascript').

    Returns:
        List of lines, each line is a list of (token_type_str, text) tuples.
    """
    try:
        lexer = lexers.get_lexer_by_name(language)
    except Exception:
        # Fallback to 'text' lexer if language not found
        lexer = lexers.get_lexer_by_name("text")

    tokens = list(lexer.get_tokens(code))

    lines: list[list[tuple[str, str]]] = []
    current_line: list[tuple[str, str]] = []
    for token_type, text in tokens:
        token_str = str(token_type)
        while text:
            idx = text.find("\n")
            if idx == -1:
                # No newline — add all text to current line
                current_line.append((token_str, text))
                break
            else:
                # Text before newline
                if idx > 0:
                    current_line.append((token_str, text[:idx]))
                # End current line
                lines.append(current_line)
                current_line = []
                # Continue with text after newline
                text = text[idx + 1 :]
                if not text:
                    # Trailing newline — add an empty line
                    lines.append([])

    # Add the last line if not empty
    if current_line:
        lines.append(current_line)

    # Ensure at least one line exists
    if not lines:
        lines.append([])

    return lines


# ---------------------------------------------------------------------------
# Layout calculations
# ---------------------------------------------------------------------------


def _calculate_dimensions(
    token_lines: list[list[tuple[str, str]]],
    font: ImageFont.FreeTypeFont,
    font_size: int,
    show_lines: bool,
    window_style: str,
    background: str,
    width: int,
    theme: dict,
) -> tuple[int, int, int, int]:
    """Calculate image canvas dimensions and content area.

    Args:
        token_lines: Tokenized code lines.
        font: The loaded font.
        font_size: Font size in pixels.
        show_lines: Whether to show line numbers.
        window_style: Window style ('mac' or 'none').
        background: Background type ('window' or 'solid').
        width: Desired image width (0 = auto).
        font_size: Font size in px.

    Returns:
        Tuple of (canvas_width, canvas_height, content_x, content_y)
        where content_x, content_y is the top-left of the code area
        (after title bar if window style).
    """
    line_height = int(font_size * 1.5)

    # Calculate max line width in pixels
    max_line_width = 0
    for line in token_lines:
        line_text = "".join(text for _, text in line)
        line_w = estimate_text_width(line_text, font)
        if line_w > max_line_width:
            max_line_width = line_w

    # Calculate content area width
    content_width = max_line_width
    if show_lines:
        content_width += LINE_NUMBERS_WIDTH + LINE_NUMBERS_PADDING_RIGHT
    content_width += PADDING_SIDES * 2

    # Apply user-specified width if set
    if width > 0 and width > content_width:
        content_width = width
    elif width > 0:
        content_width = width

    # Calculate content area height
    num_lines = len(token_lines)
    content_height = num_lines * line_height + PADDING_TOP + PADDING_BOTTOM

    # Determine if we have a window decoration
    is_window = window_style == "mac" or background == "window"

    title_bar_offset = TITLE_BAR_HEIGHT if is_window else 0

    total_content_height = content_height + title_bar_offset

    # Add shadow margins
    canvas_width = content_width + SHADOW_MARGIN * 2
    canvas_height = total_content_height + SHADOW_MARGIN * 2

    content_x = SHADOW_MARGIN + PADDING_SIDES
    content_y = SHADOW_MARGIN + title_bar_offset + PADDING_TOP

    if show_lines:
        content_x += LINE_NUMBERS_WIDTH + LINE_NUMBERS_PADDING_RIGHT

    return canvas_width, canvas_height, content_x, content_y


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------


def _draw_shadow(
    draw: ImageDraw.ImageDraw,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    radius: int,
) -> None:
    """Draw a drop shadow for the window background.

    Draws the rounded rectangle offset by SHADOW_OFFSET pixels with
    a semi-transparent black fill. The blur is applied later.
    """
    shadow_color = (0, 0, 0, int(255 * SHADOW_OPACITY))
    draw_rounded_rect(
        draw,
        (x1 + SHADOW_OFFSET, y1 + SHADOW_OFFSET, x2 + SHADOW_OFFSET, y2 + SHADOW_OFFSET),
        radius,
        fill=shadow_color,
    )


def _draw_title_bar(
    draw: ImageDraw.ImageDraw,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    theme: dict,
    title: str,
) -> None:
    """Draw the macOS-style title bar with traffic light dots and title text.

    The title bar spans from (x1, y1) to (x2, y1 + TITLE_BAR_HEIGHT).
    y2 is the bottom of the entire window (used for the separator line reference).
    """
    title_y1 = y1
    title_y2 = y1 + TITLE_BAR_HEIGHT
    title_center_y = (title_y1 + title_y2) // 2
    dot_y = title_center_y - DOT_RADIUS

    # Draw traffic light dots
    dot_positions = [
        (x1 + DOT_LEFT_MARGIN, DOT_CLOSE),
        (x1 + DOT_LEFT_MARGIN + DOT_RADIUS * 2 + DOT_SPACING, DOT_MINIMIZE),
        (
            x1 + DOT_LEFT_MARGIN + (DOT_RADIUS * 2 + DOT_SPACING) * 2,
            DOT_MAXIMIZE,
        ),
    ]

    for dot_x, dot_color_hex in dot_positions:
        draw.ellipse(
            [dot_x, dot_y, dot_x + DOT_RADIUS * 2, dot_y + DOT_RADIUS * 2],
            fill=dot_color_hex,
        )

    # Draw title text (centered in title bar)
    font = get_monospace_font(int((title_y2 - title_y1) * 0.45))
    title_color = theme.get("title_color", theme["fg"])
    try:
        title_w = estimate_text_width(title, font)
    except Exception:
        title_w = len(title) * font.size * 0.6
    title_x = (x1 + x2 - title_w) // 2
    title_y = title_center_y - font.size // 2
    draw.text((title_x, title_y), title, fill=title_color, font=font)

    # Draw separator line below title bar
    separator_color = hex_to_rgba(theme["bg"], 120)
    draw.line(
        [x1, title_y2, x2, title_y2],
        fill=separator_color,
        width=TITLE_BAR_SEPARATOR_WIDTH,
    )


def _draw_line_numbers(
    draw: ImageDraw.ImageDraw,
    line_y: int,
    line_height: int,
    num_lines: int,
    current_line_idx: int,
    theme: dict,
    canvas_x1: int,
    canvas_y1: int,
) -> None:
    """Draw line numbers for the code listing.

    Args:
        draw: ImageDraw object.
        line_y: Starting y position of the first line of code.
        line_height: Height of each line in pixels.
        num_lines: Number of lines in the code.
        current_line_idx: Index of the current line (0-based).
        theme: Theme dictionary.
        canvas_x1: Left edge of the window background.
        canvas_y1: Top edge of the window background (title bar start).
    """
    ln_color = theme["line_numbers"]
    font = get_monospace_font(12)  # slightly smaller for line numbers

    ln_x = canvas_x1 + SHADOW_MARGIN + PADDING_SIDES
    # Line numbers are right-aligned within the line numbers column
    ln_right_x = ln_x + LINE_NUMBERS_WIDTH

    for i in range(num_lines):
        y = line_y + i * line_height
        # Vertically center the line number
        ln_num = i + 1
        ln_text = str(ln_num)
        try:
            ln_w = estimate_text_width(ln_text, font)
        except Exception:
            ln_w = len(ln_text) * font.size * 0.6
        draw.text(
            (ln_right_x - ln_w, y),
            ln_text,
            fill=ln_color,
            font=font,
        )


def _draw_code_line(
    draw: ImageDraw.ImageDraw,
    tokens: list[tuple[str, str]],
    x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    theme: dict,
) -> None:
    """Draw a single line of tokenized code.

    Args:
        draw: ImageDraw object.
        tokens: List of (token_type_str, text) pairs for this line.
        x: Starting x position.
        y: Starting y position.
        font: The monospace font to use.
        theme: Theme dictionary.
    """
    token_colors = theme["token_colors"]
    default_fg = theme["fg"]
    cur_x = x

    for token_str, text in tokens:
        color_hex = _resolve_token_color(token_str, token_colors, default_fg)
        try:
            draw.text((cur_x, y), text, fill=color_hex, font=font)
            advance = estimate_text_width(text, font)
            cur_x += advance
        except Exception:
            # Draw character by character as fallback
            for ch in text:
                draw.text((cur_x, y), ch, fill=color_hex, font=font)
                try:
                    ch_advance = estimate_text_width(ch, font)
                except Exception:
                    ch_advance = font.size * 0.6
                cur_x += ch_advance


# ---------------------------------------------------------------------------
# Main generation function
# ---------------------------------------------------------------------------


def generate_image(
    code: str,
    language: str,
    theme_name: str = "monokai",
    show_lines: bool = True,
    window_style: str = "mac",
    font_size: int = 14,
    background: str = "window",
    width: int = 0,
) -> Image.Image:
    """Generate a beautiful code screenshot image.

    Args:
        code: Source code to render.
        language: Language alias for Pygments syntax highlighting.
        theme_name: Name of the theme to use.
        show_lines: Whether to include line numbers.
        window_style: 'mac' for macOS title bar decoration, 'none' for plain.
        font_size: Font size in pixels.
        background: 'window' for full window decoration, 'solid' for solid fill.
        width: Fixed image width in pixels (0 = auto-width).

    Returns:
        A PIL Image object ready to save.
    """
    # Load theme
    theme = get_theme(theme_name)

    # Load font
    font = get_monospace_font(font_size)

    # Tokenize code
    token_lines = tokenize_code(code, language)

    # Ensure at least one line
    if not token_lines:
        token_lines = [[]]

    # Determine if we show window decoration
    is_window = (background == "window") or (window_style == "mac")

    # Calculate dimensions
    line_height = int(font_size * 1.5)
    (
        canvas_width,
        canvas_height,
        content_x,
        content_y,
    ) = _calculate_dimensions(
        token_lines,
        font,
        font_size,
        show_lines,
        window_style,
        background,
        width,
        theme,
    )

    # Create canvas
    img = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Window background rectangle coordinates (inside shadow margins)
    win_x1 = SHADOW_MARGIN
    win_y1 = SHADOW_MARGIN
    title_bar_bottom = (
        win_y1 + TITLE_BAR_HEIGHT if is_window else win_y1
    )
    # Total content area
    num_lines = len(token_lines)
    total_content_height = num_lines * line_height + PADDING_TOP + PADDING_BOTTOM
    win_y2 = win_y1 + (TITLE_BAR_HEIGHT if is_window else 0) + total_content_height
    win_x2 = canvas_width - SHADOW_MARGIN

    # Determine window background color
    if is_window:
        window_bg = theme.get("window_bg", theme["bg"])
    else:
        window_bg = theme["bg"]

    # Step 1: Draw shadow (only for window style)
    if is_window:
        # Draw shadow on a separate layer for blurring
        shadow_layer = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        _draw_shadow(shadow_draw, win_x1, win_y1, win_x2, win_y2, CORNER_RADIUS)
        shadow_layer = shadow_layer.filter(
            ImageFilter.BoxBlur(SHADOW_BLUR_RADIUS)
        )
        img = Image.alpha_composite(img, shadow_layer)
        draw = ImageDraw.Draw(img)

    # Step 2: Draw window background
    if is_window:
        draw_rounded_rect(
            draw,
            (win_x1, win_y1, win_x2, win_y2),
            CORNER_RADIUS,
            fill=window_bg,
        )
    else:
        # Solid fill — just a rectangle covering the content area
        draw.rectangle(
            (win_x1, win_y1, win_x2, win_y2),
            fill=window_bg,
        )

    # Step 3: Draw title bar (if window style)
    title = language.capitalize() if language else "Code"
    if is_window:
        _draw_title_bar(
            draw,
            win_x1,
            win_y1,
            win_x2,
            win_y2,
            theme,
            title,
        )

    # Step 4: Draw line numbers
    code_start_y = content_y
    if show_lines:
        _draw_line_numbers(
            draw,
            code_start_y,
            line_height,
            num_lines,
            0,
            theme,
            win_x1,
            win_y1,
        )

    # Step 5: Draw code
    for i, line_tokens in enumerate(token_lines):
        y = code_start_y + i * line_height
        _draw_code_line(
            draw,
            line_tokens,
            content_x,
            y,
            font,
            theme,
        )

    # Step 6: Crop to content (remove excess shadow margins)
    # Actually, keep the shadow visible — just trim any fully transparent pixels
    bbox = img.getbbox()
    if bbox:
        # Expand bbox slightly to keep the shadow visible
        crop_x1 = max(0, bbox[0] - 2)
        crop_y1 = max(0, bbox[1] - 2)
        crop_x2 = min(img.width, bbox[2] + 2)
        crop_y2 = min(img.height, bbox[3] + 2)
        img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))

    # Convert to RGB for saving as PNG (flatten alpha)
    if img.mode == "RGBA":
        # Create a white background and composite
        background_img = Image.new("RGB", img.size, (255, 255, 255))
        background_img.paste(img, mask=img.split()[3])
        img = background_img

    return img
