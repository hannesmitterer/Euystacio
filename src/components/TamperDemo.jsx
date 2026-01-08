/**
 * TamperDemo Component
 * Demonstrates tamper detection for EUD (Euystacio Unified Dashboard)
 * 
 * This component simulates the verification of document hashes
 * against the on-chain EuystacioSTAnchor smart contract.
 */

import React, { useState, useCallback } from 'react';

// Simulated original hashes (in production, these come from the blockchain)
const ORIGINAL_HASHES = {
  'Der Unveränderliche Eid': 'a3b2c1d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
  'Sacred Declaration': 'b4c3d2e1f0987654321098765432109876fedcba0987654321fedcba098765',
  'Coronation Manifest': 'c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0123456789abcdef0123456789abcdef'
};

const styles = {
  container: {
    background: 'rgba(255,255,255,0.1)',
    border: '1px solid #d4af37',
    borderRadius: '10px',
    padding: '25px',
    backdropFilter: 'blur(10px)'
  },
  title: {
    color: '#d4af37',
    marginBottom: '20px',
    fontSize: '1.5em',
    textAlign: 'center',
    borderBottom: '1px solid #f7e98e',
    paddingBottom: '15px'
  },
  documentGrid: {
    display: 'grid',
    gap: '15px'
  },
  documentCard: {
    background: 'rgba(0,0,0,0.2)',
    borderRadius: '8px',
    padding: '15px',
    border: '1px solid #666'
  },
  documentName: {
    fontWeight: 'bold',
    marginBottom: '10px',
    fontSize: '1.1em'
  },
  hashDisplay: {
    fontFamily: 'monospace',
    fontSize: '0.8em',
    background: 'rgba(0,0,0,0.3)',
    padding: '8px',
    borderRadius: '4px',
    wordBreak: 'break-all',
    marginBottom: '10px'
  },
  statusBadge: {
    display: 'inline-block',
    padding: '4px 12px',
    borderRadius: '20px',
    fontSize: '0.85em',
    fontWeight: 'bold'
  },
  verified: {
    background: '#27ae60',
    color: 'white'
  },
  tampered: {
    background: '#e74c3c',
    color: 'white'
  },
  pending: {
    background: '#f39c12',
    color: 'white'
  },
  button: {
    background: 'linear-gradient(45deg, #4a1a6b, #d4af37)',
    border: 'none',
    color: 'white',
    padding: '10px 20px',
    borderRadius: '5px',
    cursor: 'pointer',
    marginTop: '15px',
    width: '100%',
    fontSize: '1em'
  },
  controls: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
    flexWrap: 'wrap'
  },
  controlButton: {
    background: 'rgba(212, 175, 55, 0.2)',
    border: '1px solid #d4af37',
    color: '#f0f0f0',
    padding: '8px 16px',
    borderRadius: '5px',
    cursor: 'pointer',
    flex: '1',
    minWidth: '120px'
  },
  log: {
    background: 'rgba(0,0,0,0.4)',
    padding: '15px',
    borderRadius: '5px',
    marginTop: '20px',
    maxHeight: '200px',
    overflowY: 'auto',
    fontFamily: 'monospace',
    fontSize: '0.85em'
  },
  logEntry: {
    marginBottom: '5px',
    padding: '3px 0',
    borderBottom: '1px solid rgba(255,255,255,0.1)'
  }
};

function TamperDemo() {
  const [documents, setDocuments] = useState(
    Object.keys(ORIGINAL_HASHES).map(name => ({
      name,
      originalHash: ORIGINAL_HASHES[name],
      currentHash: ORIGINAL_HASHES[name],
      status: 'pending'
    }))
  );
  const [logs, setLogs] = useState([]);
  const [isVerifying, setIsVerifying] = useState(false);

  const addLog = useCallback((message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, message, type }]);
  }, []);

  const verifyAll = useCallback(async () => {
    setIsVerifying(true);
    addLog('Starting tamper verification...', 'info');
    
    for (let i = 0; i < documents.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const doc = documents[i];
      const isValid = doc.currentHash === doc.originalHash;
      
      setDocuments(prev => prev.map((d, idx) => 
        idx === i ? { ...d, status: isValid ? 'verified' : 'tampered' } : d
      ));
      
      if (isValid) {
        addLog(`✓ ${doc.name}: Hash verified`, 'success');
      } else {
        addLog(`✗ ${doc.name}: TAMPER DETECTED!`, 'error');
      }
    }
    
    addLog('Verification complete.', 'info');
    setIsVerifying(false);
  }, [documents, addLog]);

  const simulateTamper = useCallback((index) => {
    setDocuments(prev => prev.map((doc, idx) => 
      idx === index 
        ? { 
            ...doc, 
            currentHash: 'TAMPERED_' + doc.originalHash.substring(9),
            status: 'pending'
          } 
        : doc
    ));
    addLog(`⚠ Simulated tampering on: ${documents[index].name}`, 'warning');
  }, [documents, addLog]);

  const resetAll = useCallback(() => {
    setDocuments(
      Object.keys(ORIGINAL_HASHES).map(name => ({
        name,
        originalHash: ORIGINAL_HASHES[name],
        currentHash: ORIGINAL_HASHES[name],
        status: 'pending'
      }))
    );
    setLogs([]);
    addLog('Demo reset to initial state.', 'info');
  }, [addLog]);

  const getStatusStyle = (status) => {
    switch (status) {
      case 'verified': return styles.verified;
      case 'tampered': return styles.tampered;
      default: return styles.pending;
    }
  };

  const getLogColor = (type) => {
    switch (type) {
      case 'success': return '#2ecc71';
      case 'error': return '#e74c3c';
      case 'warning': return '#f39c12';
      default: return '#95a5a6';
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🔍 Tamper Detection Demo</h2>
      
      <div style={styles.controls}>
        <button 
          style={styles.controlButton}
          onClick={verifyAll}
          disabled={isVerifying}
        >
          {isVerifying ? 'Verifying...' : 'Verify All'}
        </button>
        <button 
          style={styles.controlButton}
          onClick={() => simulateTamper(Math.floor(Math.random() * documents.length))}
          disabled={isVerifying}
        >
          Simulate Tamper
        </button>
        <button 
          style={styles.controlButton}
          onClick={resetAll}
          disabled={isVerifying}
        >
          Reset Demo
        </button>
      </div>
      
      <div style={styles.documentGrid}>
        {documents.map((doc, index) => (
          <div key={index} style={styles.documentCard}>
            <div style={styles.documentName}>{doc.name}</div>
            <div style={styles.hashDisplay}>
              <strong>Current Hash:</strong><br />
              {doc.currentHash.substring(0, 32)}...
            </div>
            <span style={{ ...styles.statusBadge, ...getStatusStyle(doc.status) }}>
              {doc.status.toUpperCase()}
            </span>
          </div>
        ))}
      </div>
      
      {logs.length > 0 && (
        <div style={styles.log}>
          <strong style={{ color: '#d4af37' }}>Verification Log:</strong>
          {logs.map((log, idx) => (
            <div 
              key={idx} 
              style={{ ...styles.logEntry, color: getLogColor(log.type) }}
            >
              [{log.timestamp}] {log.message}
            </div>
          ))}
        </div>
      )}
      
      <p style={{ 
        marginTop: '20px', 
        fontSize: '0.9em', 
        opacity: 0.7, 
        textAlign: 'center' 
      }}>
        This demo simulates verification against the EuystacioSTAnchor smart contract.
        In production, hashes are retrieved from the blockchain.
      </p>
    </div>
  );
}

export default TamperDemo;
