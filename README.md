# Code Pretty Snap 📸

> Generate beautiful code screenshots, right from your terminal — like [carbon.now.sh](https://carbon.now.sh), but offline and CLI-first.

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/CLI-ready-green)](cli/)
[![Website](https://img.shields.io/badge/website-demo-purple)](website/)

</div>

---

## ✨ Features

- **CLI Tool** — Generate code screenshots from your terminal with `pip install code-pretty-snap`
- **Beautiful output** — macOS-style window decorations, syntax highlighting, rounded corners, drop shadows
- **6 hand-crafted themes** — Monokai, Dracula, Nord (dark); GitHub, One Light, Solarized Light (light)
- **50+ languages** — Powered by Pygments for syntax highlighting
- **Demo Website** — Try it online with live preview and one-click PNG download
- **Zero extra runtime deps** — Pure Pillow pixel rendering, no browser or wkhtmltopdf needed

## 🚀 Quick Start (CLI)

```bash
# Install
pip install code-pretty-snap

# Use it
code-pretty-snap "print('hello world')" --lang python --output hello.png

# Or from a file
code-pretty-snap myscript.py --lang python --output snap.png
```

## 📖 CLI Usage

```
usage: code-pretty-snap [-h] [-l LANG] [-t THEME] [-o OUTPUT] [-n] [--window-style {mac,none}] [--font-size FONT_SIZE] [--background {window,solid}] [--width WIDTH] code

Generate beautiful code screenshots

positional arguments:
  code                  Code string or path to source file

options:
  -h, --help            Show this help message
  -l, --lang LANG       Programming language (auto-detect if omitted)
  -t, --theme THEME     Color theme (default: monokai)
  -o, --output OUTPUT   Output PNG path (default: code_snap.png)
  -n, --show-lines      Show line numbers (default: on)
  --window-style        Window decoration: 'mac' or 'none' (default: mac)
  --font-size FONT_SIZE Font size in px (default: 14)
  --background          Background type: 'window' or 'solid' (default: window)
  --width WIDTH         Image width (default: auto)
```

## 🎨 Themes

| Theme | Type | Preview |
|-------|------|---------|
| Monokai | Dark | Classic Monokai dark |
| Dracula | Dark | Dracula dark purple |
| Nord | Dark | Nordic blue-grey |
| GitHub | Light | GitHub Light |
| One Light | Light | Atom One Light |
| Solarized Light | Light | Solarized Light |

## 🌐 Demo Website

An interactive demo website is available in the [`website/`](website/) directory:

```bash
cd website
npm install
npm run dev
```

Features:
- Live code editing with instant preview
- Theme and language selection
- PNG download with one click
- Responsive design (works on mobile)
- Dark/light UI mode

## 📦 Project Structure

```
code-pretty-snap/
├── cli/                    # Python CLI tool
│   ├── code_pretty_snap/   # Python package
│   │   ├── cli.py          # CLI entry point (argparse)
│   │   ├── generator.py    # Image generation (Pillow)
│   │   ├── themes.py       # Theme definitions
│   │   └── utils.py        # Helpers (fonts, drawing)
│   ├── pyproject.toml
│   └── README.md
├── website/                # Vite + React demo website
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── themes.js       # Theme colors
│   │   └── ...
│   ├── package.json
│   └── README.md
├── examples/               # Example screenshots
├── LICENSE                 # MIT License
└── README.md               # This file
```

## 🛠️ Development

### CLI

```bash
cd cli
pip install -e .
code-pretty-snap "print('hello')" --lang python --output test.png
```

### Website

```bash
cd website
npm install
npm run dev      # development server
npm run build    # production build
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
