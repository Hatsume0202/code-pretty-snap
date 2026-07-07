import React from 'react';

export default function CodeEditor({ code, onChange, language }) {
  return (
    <div className="code-editor">
      <div className="editor-header">
        <span className="editor-label">Code Input</span>
        <span className="editor-lang-badge">{language}</span>
      </div>
      <textarea
        className="editor-textarea"
        value={code}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste or type your code here..."
        spellCheck={false}
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="off"
        wrap="off"
      />
    </div>
  );
}
