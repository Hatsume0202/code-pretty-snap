export const THEMES = {
  monokai: {
    bg: "#272822",
    fg: "#F8F8F2",
    line_numbers: "#90908A",
    window_bg: "#1D1E19",
    title_color: "#F8F8F2",
    tab_bg: "#1D1E19",
    tokens: {
      comment: "#75715E",
      keyword: "#F92672",
      string: "#E6DB74",
      number: "#AE81FF",
      function: "#A6E22E",
      "class": "#A6E22E",
      builtin: "#66D9EF",
      operator: "#F92672",
      punctuation: "#F8F8F2",
    }
  },
  dracula: {
    bg: "#282A36",
    fg: "#F8F8F2",
    line_numbers: "#6272A4",
    window_bg: "#21222C",
    title_color: "#F8F8F2",
    tab_bg: "#21222C",
    tokens: {
      comment: "#6272A4",
      keyword: "#FF79C6",
      string: "#F1FA8C",
      number: "#BD93F9",
      function: "#50FA7B",
      "class": "#8BE9FD",
      builtin: "#8BE9FD",
      operator: "#FF79C6",
      punctuation: "#F8F8F2",
    }
  },
  nord: {
    bg: "#2E3440",
    fg: "#D8DEE9",
    line_numbers: "#616E88",
    window_bg: "#242933",
    title_color: "#D8DEE9",
    tab_bg: "#242933",
    tokens: {
      comment: "#616E88",
      keyword: "#81A1C1",
      string: "#A3BE8C",
      number: "#B48EAD",
      function: "#88C0D0",
      "class": "#8FBCBB",
      builtin: "#5E81AC",
      operator: "#81A1C1",
      punctuation: "#D8DEE9",
    }
  },
  github: {
    bg: "#FFFFFF",
    fg: "#24292E",
    line_numbers: "#959DA5",
    window_bg: "#F6F8FA",
    title_color: "#24292E",
    tab_bg: "#F6F8FA",
    tokens: {
      comment: "#6A737D",
      keyword: "#D73A49",
      string: "#032F62",
      number: "#005CC5",
      function: "#6F42C1",
      "class": "#22863A",
      builtin: "#005CC5",
      operator: "#D73A49",
      punctuation: "#24292E",
    }
  },
  "one-light": {
    bg: "#FAFAFA",
    fg: "#383A42",
    line_numbers: "#9D9D9F",
    window_bg: "#F0F0F1",
    title_color: "#383A42",
    tab_bg: "#F0F0F1",
    tokens: {
      comment: "#A0A1A7",
      keyword: "#E45649",
      string: "#50A14F",
      number: "#986801",
      function: "#4078F2",
      "class": "#C18401",
      builtin: "#0184BC",
      operator: "#E45649",
      punctuation: "#383A42",
    }
  },
  "solarized-light": {
    bg: "#FDF6E3",
    fg: "#586E75",
    line_numbers: "#93A1A1",
    window_bg: "#EEE8D5",
    title_color: "#586E75",
    tab_bg: "#EEE8D5",
    tokens: {
      comment: "#93A1A1",
      keyword: "#859900",
      string: "#2AA198",
      number: "#D33682",
      function: "#268BD2",
      "class": "#B58900",
      builtin: "#CB4B16",
      operator: "#859900",
      punctuation: "#586E75",
    }
  }
};

export const LANGUAGES = [
  'python', 'javascript', 'typescript', 'html', 'css', 'jsx', 'tsx',
  'json', 'yaml', 'markdown', 'bash', 'sql', 'rust', 'go', 'java',
  'cpp', 'csharp', 'ruby', 'php', 'swift', 'kotlin', 'scala'
];

export const DEFAULT_CODE = `def fibonacci(n):
    """Generate the Fibonacci sequence up to n terms."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def main():
    n = 10
    result = fibonacci(n)
    print(f"First {n} Fibonacci numbers: {result}")

if __name__ == "__main__":
    main()
`;
