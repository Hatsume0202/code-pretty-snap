import React, { useMemo } from 'react';
import hljs from 'highlight.js';
import { applyThemeToHtml, formatLanguage } from '../utils';

export default function Preview({
  code,
  theme,
  language,
  showLineNumbers,
  windowStyle,
  fontSize,
  backgroundToggle,
}) {
  const highlightedHtml = useMemo(() => {
    if (!code.trim()) {
      return '<span style="color: ' + theme.fg + '; opacity: 0.4">// start typing code...</span>';
    }

    let lang = language;
    // Map JSX/TSX to JavaScript/TypeScript for hljs
    if (lang === 'jsx') lang = 'javascript';
    if (lang === 'tsx') lang = 'typescript';
    if (lang === 'csharp') lang = 'csharp';
    if (lang === 'cpp') lang = 'cpp';
    if (lang === 'kotlin') lang = 'kotlin';
    if (lang === 'scala') lang = 'scala';
    if (lang === 'ruby') lang = 'ruby';
    if (lang === 'php') lang = 'php';
    if (lang === 'swift') lang = 'swift';
    if (lang === 'rust') lang = 'rust';
    if (lang === 'go') lang = 'go';
    if (lang === 'yaml') lang = 'yaml';
    if (lang === 'markdown') lang = 'markdown';

    try {
      const supported = hljs.getLanguage(lang);
      if (supported) {
        const result = hljs.highlight(code, { language: lang, ignoreIllegals: true });
        return applyThemeToHtml(result.value, theme.tokens);
      }
      // Fallback to auto-detect
      const result = hljs.highlightAuto(code);
      return applyThemeToHtml(result.value, theme.tokens);
    } catch {
      return `<span style="color:${theme.fg}">${escapeHtml(code)}</span>`;
    }
  }, [code, language, theme]);

  const lines = code ? code.split('\n') : [''];

  const renderLineNumbers = () => {
    if (!showLineNumbers) return null;
    return (
      <div className="line-numbers" style={{ color: theme.line_numbers }}>
        {lines.map((_, i) => (
          <div key={i} className="line-number">{i + 1}</div>
        ))}
      </div>
    );
  };

  const renderWindowDecoration = () => {
    if (windowStyle !== 'mac') return null;

    return (
      <>
        <div className="mac-title-bar" style={{ backgroundColor: theme.tab_bg, color: theme.title_color }}>
          <div className="mac-dots">
            <span className="mac-dot mac-dot-red"></span>
            <span className="mac-dot mac-dot-yellow"></span>
            <span className="mac-dot mac-dot-green"></span>
          </div>
          <span className="mac-title-text">{formatLanguage(language)}</span>
          <div className="mac-spacer"></div>
        </div>
        <div className="title-separator" style={{ backgroundColor: theme.bg }}></div>
      </>
    );
  };

  const previewStyle = {
    backgroundColor: backgroundToggle === 'solid' ? theme.bg : theme.window_bg,
    color: theme.fg,
    fontSize: `${fontSize}px`,
  };

  const codeBlockStyle = {
    backgroundColor: theme.bg,
  };

  return (
    <div className="preview-wrapper" id="code-preview">
      <div className="preview-surface" style={previewStyle}>
        {renderWindowDecoration()}
        <div className="code-container" style={codeBlockStyle}>
          {renderLineNumbers()}
          <div className="code-content">
            <pre
              className="code-pre"
              dangerouslySetInnerHTML={{ __html: highlightedHtml }}
              style={{ fontFamily: "'JetBrains Mono', 'Fira Code', 'Source Code Pro', monospace" }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}
