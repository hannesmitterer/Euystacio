/**
 * Euystacio React Application Entry Point
 * Vite React Bootstrap for EUD Tamper Demo
 * 
 * IMPORTANT: Do not commit private keys or secrets.
 * All sensitive values should be set via environment variables.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
