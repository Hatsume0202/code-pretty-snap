"""argparse CLI entry point for code-pretty-snap."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from pygments import lexers

from code_pretty_snap import __version__
from code_pretty_snap.generator import generate_image
from code_pretty_snap.themes import THEME_NAMES


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate beautiful code screenshots in your terminal.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  code-pretty-snap "print(\'hello world\')" --lang python\n'
            "  code-pretty-snap myscript.py --lang python --output snap.png\n"
            "  code-pretty-snap code.rs --theme dracula --show-lines --font-size 16\n"
        ),
    )

    parser.add_argument(
        "code",
        type=str,
        help=(
            "Inline code string OR path to a source file. "
            "If the path exists on disk, it's read as a file."
        ),
    )

    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default=None,
        help=(
            "Language for syntax highlighting. Auto-detected via Pygments if not "
            "specified. Supports 50+ languages."
        ),
    )

    parser.add_argument(
        "--theme",
        "-t",
        type=str,
        default="monokai",
        choices=THEME_NAMES,
        help=f"Color theme (default: monokai). Choices: {', '.join(THEME_NAMES)}",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="code_snap.png",
        help="Output PNG file path (default: code_snap.png)",
    )

    parser.add_argument(
        "--show-lines",
        "-n",
        action="store_true",
        default=True,
        help="Show line numbers (default: True)",
    )

    parser.add_argument(
        "--no-line-numbers",
        action="store_false",
        dest="show_lines",
        help="Hide line numbers",
    )

    parser.add_argument(
        "--window-style",
        type=str,
        default="mac",
        choices=["mac", "none"],
        help="Window style decoration (default: mac)",
    )

    parser.add_argument(
        "--font-size",
        type=int,
        default=14,
        help="Font size in px (default: 14)",
    )

    parser.add_argument(
        "--background",
        type=str,
        default="window",
        choices=["window", "solid"],
        help="Background type (default: window)",
    )

    parser.add_argument(
        "--width",
        type=int,
        default=0,
        help=(
            "Image width in px (default: 0 = auto-width based on longest line)"
        ),
    )

    parsed = parser.parse_args(argv)

    # Validate font size
    if parsed.font_size < 6:
        parser.error("font-size must be at least 6px")
    if parsed.font_size > 72:
        parser.error("font-size must be at most 72px")

    return parsed


def resolve_code_input(code_arg: str) -> tuple[str, Optional[str]]:
    """Resolve the code input argument.

    Checks if the argument is an existing file path. If so, reads the file
    and returns its content along with a suggested language (from file extension).

    Returns:
        Tuple of (code_content, suggested_language or None)
    """
    if os.path.isfile(code_arg):
        with open(code_arg, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
        # Suggest language from file extension
        try:
            guessed = lexers.guess_lexer_for_filename(code_arg, code)
            suggested_lang = guessed.aliases[0] if guessed.aliases else None
        except Exception:
            suggested_lang = None
        return code, suggested_lang
    else:
        return code_arg, None


def detect_language(code: str, lang_arg: Optional[str]) -> str:
    """Detect the language for syntax highlighting.

    If --lang was provided, use it. Otherwise try to auto-detect via Pygments.
    Falls back to 'text' if detection fails.
    """
    if lang_arg:
        return lang_arg

    try:
        guessed = lexers.guess_lexer(code)
        if guessed and guessed.aliases:
            # Filter out overly generic aliases
            lang = guessed.aliases[0]
            if lang in ("text", "output"):
                # Try harder with a more specific guess
                guessed2 = lexers.guess_lexer(code.strip())
                if guessed2 and guessed2.aliases:
                    lang = guessed2.aliases[0]
            return lang
    except Exception:
        pass

    return "text"


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_args(argv)

    try:
        # Resolve code input
        code, suggested_lang = resolve_code_input(args.code)

        # Detect language
        language = args.lang or suggested_lang
        detected_lang = detect_language(code, language)

        # Generate the image
        img = generate_image(
            code=code,
            language=detected_lang,
            theme_name=args.theme,
            show_lines=args.show_lines,
            window_style=args.window_style,
            font_size=args.font_size,
            background=args.background,
            width=args.width,
        )

        # Save the image
        img.save(args.output, "PNG")
        print(f"Code snapshot saved to: {args.output}", file=sys.stderr)
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
