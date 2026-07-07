/**
 * Map highlight.js CSS class names to our theme token keys.
 */
const HLJS_CLASS_MAP = {
  'hljs-keyword': 'keyword',
  'hljs-string': 'string',
  'hljs-number': 'number',
  'hljs-built_in': 'builtin',
  'hljs-literal': 'keyword',
  'hljs-type': 'class',
  'hljs-attr': 'operator',
  'hljs-comment': 'comment',
  'hljs-function': 'function',
  'hljs-title': 'function',
  'hljs-params': 'punctuation',
  'hljs-meta': 'punctuation',
  'hljs-selector-tag': 'keyword',
  'hljs-selector-id': 'function',
  'hljs-selector-class': 'class',
  'hljs-regexp': 'string',
  'hljs-symbol': 'number',
  'hljs-variable': 'builtin',
  'hljs-template-variable': 'string',
  'hljs-tag': 'operator',
  'hljs-name': 'function',
  'hljs-attribute': 'operator',
  'hljs-addition': 'string',
  'hljs-deletion': 'keyword',
  'hljs-section': 'function',
  'hljs-link': 'string',
};

/**
 * Given a highlight.js HTML string with hljs-* classes,
 * replace each tagged span with inline color style from the theme.
 *
 * @param {string} html - highlight.js output like '<span class="hljs-keyword">def</span>'
 * @param {object} themeTokens - The tokens object from a theme definition
 * @returns {string} HTML with inline color styles
 */
export function applyThemeToHtml(html, themeTokens) {
  if (!html) return '';

  return html.replace(
    /<span class="([^"]+)">/g,
    (match, classNames) => {
      const classes = classNames.split(/\s+/);
      for (const cls of classes) {
        const tokenKey = HLJS_CLASS_MAP[cls];
        if (tokenKey && themeTokens[tokenKey]) {
          return `<span style="color:${themeTokens[tokenKey]}">`;
        }
      }
      return '<span>';
    }
  );
}

/**
 * Format the filename for download.
 */
export function getDownloadFileName(language) {
  const extMap = {
    python: 'py', javascript: 'js', typescript: 'ts', html: 'html',
    css: 'css', jsx: 'jsx', tsx: 'tsx', json: 'json', yaml: 'yaml',
    markdown: 'md', bash: 'sh', sql: 'sql', rust: 'rs', go: 'go',
    java: 'java', cpp: 'cpp', csharp: 'cs', ruby: 'rb', php: 'php',
    swift: 'swift', kotlin: 'kt', scala: 'scala',
  };
  const ext = extMap[language] || 'txt';
  return `code_snap.${ext}.png`;
}

/**
 * Format the language name for display in the title bar.
 */
export function formatLanguage(language) {
  return language.charAt(0).toUpperCase() + language.slice(1);
}
