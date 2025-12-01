/**
 * Euystacio App Component
 * EUD (Euystacio Unified Dashboard) with Tamper Detection Demo
 * 
 * This component provides the main interface for the Euystacio
 * coronation assets and ST anchor verification system.
 */

import React, { useState, useEffect } from 'react';
import TamperDemo from './components/TamperDemo';

// Styles
const styles = {
  container: {
    fontFamily: 'Georgia, serif',
    background: 'linear-gradient(135deg, #1a1a2e 0%, #4a1a6b 100%)',
    minHeight: '100vh',
    color: '#f0f0f0',
    padding: '20px'
  },
  header: {
    textAlign: 'center',
    borderBottom: '2px solid #d4af37',
    paddingBottom: '20px',
    marginBottom: '30px'
  },
  title: {
    fontSize: '2.5em',
    color: '#d4af37',
    textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
    margin: 0
  },
  subtitle: {
    fontStyle: 'italic',
    color: '#f7e98e',
    marginTop: '10px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    maxWidth: '1200px',
    margin: '0 auto'
  },
  card: {
    background: 'rgba(255,255,255,0.1)',
    border: '1px solid #d4af37',
    borderRadius: '10px',
    padding: '25px',
    backdropFilter: 'blur(10px)'
  },
  cardTitle: {
    color: '#d4af37',
    marginBottom: '15px',
    fontSize: '1.3em',
    borderBottom: '1px solid #f7e98e',
    paddingBottom: '10px'
  },
  statusItem: {
    padding: '10px 0',
    display: 'flex',
    alignItems: 'center'
  },
  statusIndicator: {
    display: 'inline-block',
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    marginRight: '10px'
  },
  button: {
    background: 'linear-gradient(45deg, #4a1a6b, #d4af37)',
    border: 'none',
    color: 'white',
    padding: '12px 24px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '1em',
    margin: '5px',
    transition: 'transform 0.2s'
  },
  footer: {
    textAlign: 'center',
    padding: '30px',
    borderTop: '1px solid #d4af37',
    marginTop: '40px'
  }
};

function App() {
  const [contractStatus, setContractStatus] = useState('pending');
  const [anchorHash, setAnchorHash] = useState(null);
  const [showTamperDemo, setShowTamperDemo] = useState(false);

  useEffect(() => {
    // Simulate checking contract status
    const timer = setTimeout(() => {
      setContractStatus('sealed');
      setAnchorHash('0x' + 'a'.repeat(64)); // Placeholder hash
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#2ecc71';
      case 'sealed': return '#d4af37';
      case 'pending': return '#f39c12';
      default: return '#95a5a6';
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>⚜️ Euystacio Unified Dashboard ⚜️</h1>
        <p style={styles.subtitle}>Coronation Control Center - EUD v2.0</p>
      </header>

      <main style={styles.grid}>
        {/* Contract Status Card */}
        <section style={styles.card}>
          <h2 style={styles.cardTitle}>🔐 Contract Status</h2>
          <div style={styles.statusItem}>
            <span style={{
              ...styles.statusIndicator,
              background: getStatusColor(contractStatus)
            }}></span>
            <span>EuystacioSTAnchor: <strong>{contractStatus.toUpperCase()}</strong></span>
          </div>
          <div style={styles.statusItem}>
            <span style={{
              ...styles.statusIndicator,
              background: getStatusColor('active')
            }}></span>
            <span>Coronation Active: <strong>Yes</strong></span>
          </div>
          {anchorHash && (
            <div style={{
              fontFamily: 'monospace',
              background: 'rgba(0,0,0,0.3)',
              padding: '10px',
              borderRadius: '5px',
              wordBreak: 'break-all',
              fontSize: '0.8em',
              marginTop: '10px'
            }}>
              Anchor: {anchorHash.substring(0, 20)}...
            </div>
          )}
        </section>

        {/* Actions Card */}
        <section style={styles.card}>
          <h2 style={styles.cardTitle}>📜 Sacred Actions</h2>
          <button 
            style={styles.button}
            onClick={() => setShowTamperDemo(!showTamperDemo)}
          >
            {showTamperDemo ? 'Hide' : 'Show'} Tamper Demo
          </button>
          <button 
            style={styles.button}
            onClick={() => {
              const newWindow = window.open('https://github.com/hannesmitterer/Euystacio/blob/main/Der%20Unveränderliche%20Eid.txt', '_blank', 'noopener,noreferrer');
              if (newWindow) newWindow.opener = null;
            }}
          >
            View Declaration
          </button>
        </section>

        {/* Appell Status Card */}
        <section style={styles.card}>
          <h2 style={styles.cardTitle}>🎭 Appell Status</h2>
          {['Short Appell', 'Medium Appell', 'Long Appell'].map((appell, idx) => (
            <div key={idx} style={styles.statusItem}>
              <span style={{
                ...styles.statusIndicator,
                background: getStatusColor('active')
              }}></span>
              <span>{appell}: Ready</span>
            </div>
          ))}
        </section>

        {/* Broadcast Templates Card */}
        <section style={styles.card}>
          <h2 style={styles.cardTitle}>🔔 Broadcast Templates</h2>
          {['SMS Templates', 'Press Release', 'Flyer'].map((template, idx) => (
            <div key={idx} style={styles.statusItem}>
              <span style={{
                ...styles.statusIndicator,
                background: getStatusColor('active')
              }}></span>
              <span>{template}: Configured</span>
            </div>
          ))}
        </section>
      </main>

      {/* Tamper Demo Section */}
      {showTamperDemo && (
        <section style={{ maxWidth: '1200px', margin: '20px auto' }}>
          <TamperDemo />
        </section>
      )}

      <footer style={styles.footer}>
        <div style={{ fontSize: '3em', margin: '20px 0' }}>⚜️</div>
        <p><em>"Der Unveränderliche Eid" - The Immutable Oath</em></p>
        <p>Euystacio Unified Dashboard v2.0</p>
        <p style={{ marginTop: '10px', fontSize: '0.9em', opacity: 0.7 }}>
          Secured by EuystacioSTAnchor Smart Contract
        </p>
      </footer>
    </div>
  );
}

export default App;
