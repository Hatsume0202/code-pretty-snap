# code-pretty-snap

Generate beautiful code screenshots directly in your terminal — like carbon.now.sh, but fully offline and pixel-perfect.

Built with **pure Pillow** pixel rendering (no HTML, no wkhtmltopdf, no Playwright).

## Installation

```bash
cd cli
pip install -e .
```

Or install the dependencies manually:

```bash
pip install -r requirements.txt
```

## Usage

### Quick start

Render inline code:

```bash
code-pretty-snap "print('hello world')" --lang python --output snap.png
```

Render from a file:

```bash
code-pretty-snap myscript.py --output snap.png
```

### All options

```bash
code-pretty-snap [code] [options]

Positional:
  code                  Inline code string OR path to a source file

Options:
  -l, --lang            Language (auto-detect if omitted)
  -t, --theme           Theme name: monokai, dracula, nord, github, one-light,
                        solarized-light (default: monokai)
  -o, --output          Output PNG file path (default: code_snap.png)
  -n, --show-lines      Show line numbers (default: on)
  --no-line-numbers     Hide line numbers
  --window-style        Window style: mac, none (default: mac)
  --font-size           Font size in px (default: 14)
  --background          Background type: window, solid (default: window)
  --width               Image width in px (0 = auto-width)
```

### Examples

```bash
# Dark theme with Dracula
code-pretty-snap script.py --theme dracula --output dracula.png

# Light theme, no window decoration
code-pretty-snap "const x = 42;" --lang javascript --theme github --background solid --output plain.png

# Custom font size and fixed width
code-pretty-snap app.py --font-size 18 --width 800 --output wide.png
```

## Themes

| Theme            | Type  |
|------------------|-------|
| monokai          | Dark  |
| dracula          | Dark  |
| nord             | Dark  |
| github           | Light |
| one-light        | Light |
| solarized-light  | Light |

## Requirements

- Python 3.10+
- Pillow >= 10.0
- Pygments >= 2.15

## How it works

1. The input code is tokenized by **Pygments** for syntax highlighting.
2. Each token is rendered pixel-by-pixel using **Pillow** image drawing primitives.
3. A macOS-style window frame is drawn with traffic-light buttons, drop shadow, and rounded corners.
4. Line numbers and title text are added.
5. The result is saved as a PNG image.

No browser, no HTML, no web fonts — just pure Python pixel rendering.
