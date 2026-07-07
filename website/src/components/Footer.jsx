import React from 'react';

export default function Footer() {
  return (
    <footer className="footer">
      <p>
        Built with{' '}
        <a href="https://react.dev" target="_blank" rel="noreferrer">React</a>
        ,{' '}
        <a href="https://highlightjs.org" target="_blank" rel="noreferrer">highlight.js</a>
        , and{' '}
        <a href="https://html2canvas.hertzen.com" target="_blank" rel="noreferrer">html2canvas</a>
        . Font:{' '}
        <a href="https://www.jetbrains.com/lp/mono/" target="_blank" rel="noreferrer">JetBrains Mono</a>
        .
      </p>
    </footer>
  );
}
