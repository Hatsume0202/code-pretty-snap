import React, { useState, useCallback, useEffect } from 'react';
import CodeEditor from './components/CodeEditor';
import Preview from './components/Preview';
import Toolbar from './components/Toolbar';
import Footer from './components/Footer';
import { THEMES, DEFAULT_CODE } from './themes';
import { getDownloadFileName } from './utils';

export default function App() {
  // Code state
  const [code, setCode] = useState(DEFAULT_CODE);
  const [language, setLanguage] = useState('python');
  const [themeName, setThemeName] = useState('monokai');
  const [showLineNumbers, setShowLineNumbers] = useState(true);
  const [windowStyle, setWindowStyle] = useState('mac');
  const [fontSize, setFontSize] = useState(14);
  const [backgroundToggle, setBackgroundToggle] = useState('window');
  const [downloading, setDownloading] = useState(false);

  // Site theme (dark/light for the UI itself)
  const [siteTheme, setSiteTheme] = useState(() => {
    const stored = localStorage.getItem('cps-site-theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', siteTheme);
    localStorage.setItem('cps-site-theme', siteTheme);
  }, [siteTheme]);

  const toggleSiteTheme = useCallback(() => {
    setSiteTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  const theme = THEMES[themeName];

  const handleDownload = useCallback(async () => {
    const html2canvas = (await import('html2canvas')).default;
    const previewEl = document.getElementById('code-preview');
    if (!previewEl) return;

    setDownloading(true);
    try {
      const canvas = await html2canvas(previewEl, {
        scale: 2,
        backgroundColor: backgroundToggle === 'solid' ? theme.bg : theme.window_bg,
        allowTaint: false,
        useCORS: true,
        logging: false,
      });
      const link = document.createElement('a');
      link.download = getDownloadFileName(language);
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (err) {
      console.error('Download failed:', err);
    } finally {
      setDownloading(false);
    }
  }, [language, backgroundToggle, theme]);

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-logo">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="16 18 22 12 16 6"/>
            <polyline points="8 6 2 12 8 18"/>
          </svg>
          <h1>Code Pretty Snap</h1>
        </div>
      </header>

      <Toolbar
        language={language}
        setLanguage={setLanguage}
        themeName={themeName}
        setThemeName={setThemeName}
        showLineNumbers={showLineNumbers}
        setShowLineNumbers={setShowLineNumbers}
        windowStyle={windowStyle}
        setWindowStyle={setWindowStyle}
        fontSize={fontSize}
        setFontSize={setFontSize}
        backgroundToggle={backgroundToggle}
        setBackgroundToggle={setBackgroundToggle}
        siteTheme={siteTheme}
        toggleSiteTheme={toggleSiteTheme}
        onDownload={handleDownload}
        downloading={downloading}
      />

      <main className="main-content">
        <div className="panels">
          <div className="panel panel-editor">
            <CodeEditor code={code} onChange={setCode} language={language} />
          </div>
          <div className="panel panel-preview">
            <Preview
              code={code}
              theme={theme}
              language={language}
              showLineNumbers={showLineNumbers}
              windowStyle={windowStyle}
              fontSize={fontSize}
              backgroundToggle={backgroundToggle}
            />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
