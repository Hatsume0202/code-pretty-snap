import React from 'react';
import { THEMES, LANGUAGES } from '../themes';

export default function Toolbar({
  language,
  setLanguage,
  themeName,
  setThemeName,
  showLineNumbers,
  setShowLineNumbers,
  windowStyle,
  setWindowStyle,
  fontSize,
  setFontSize,
  backgroundToggle,
  setBackgroundToggle,
  siteTheme,
  toggleSiteTheme,
  onDownload,
  downloading,
}) {
  return (
    <div className="toolbar">
      <div className="toolbar-row">
        {/* Language */}
        <div className="toolbar-group">
          <label className="toolbar-label">Language</label>
          <select
            className="toolbar-select"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {LANGUAGES.map((lang) => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
        </div>

        {/* Theme */}
        <div className="toolbar-group">
          <label className="toolbar-label">Theme</label>
          <select
            className="toolbar-select"
            value={themeName}
            onChange={(e) => setThemeName(e.target.value)}
          >
            {Object.keys(THEMES).map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        {/* Font Size */}
        <div className="toolbar-group">
          <label className="toolbar-label">Font Size: {fontSize}px</label>
          <input
            type="range"
            className="toolbar-slider"
            min="10"
            max="24"
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
          />
        </div>
      </div>

      <div className="toolbar-row">
        {/* Line Numbers */}
        <div className="toolbar-group toolbar-toggle-group">
          <label className="toolbar-label">Line Numbers</label>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={showLineNumbers}
              onChange={(e) => setShowLineNumbers(e.target.checked)}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>

        {/* Window Style */}
        <div className="toolbar-group">
          <label className="toolbar-label">Window Style</label>
          <select
            className="toolbar-select"
            value={windowStyle}
            onChange={(e) => setWindowStyle(e.target.value)}
          >
            <option value="mac">macOS</option>
            <option value="none">None</option>
          </select>
        </div>

        {/* Background */}
        <div className="toolbar-group">
          <label className="toolbar-label">Background</label>
          <select
            className="toolbar-select"
            value={backgroundToggle}
            onChange={(e) => setBackgroundToggle(e.target.value)}
          >
            <option value="window">Window</option>
            <option value="solid">Solid</option>
          </select>
        </div>

        {/* Site Theme Toggle */}
        <div className="toolbar-group">
          <label className="toolbar-label">Site Theme</label>
          <button
            className="toolbar-icon-btn"
            onClick={toggleSiteTheme}
            title={`Switch to ${siteTheme === 'dark' ? 'light' : 'dark'} mode`}
          >
            {siteTheme === 'dark' ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/>
                <line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/>
                <line x1="21" y1="12" x2="23" y2="12"/>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            )}
          </button>
        </div>

        {/* Download */}
        <div className="toolbar-group toolbar-download-group">
          <button
            className="toolbar-download-btn"
            onClick={onDownload}
            disabled={downloading}
          >
            {downloading ? (
              <>
                <span className="spinner"></span>
                Exporting...
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Download PNG
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
