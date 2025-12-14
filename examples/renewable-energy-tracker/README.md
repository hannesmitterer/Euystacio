# Renewable Energy Tracker
## Community Solar Monitoring on IPFS & Blockchain

**A Seedbringer Example Project**

Track and share solar panel performance data with permanent, verifiable records using decentralized technology.

---

## Overview

This project demonstrates how communities can transparently monitor renewable energy production, ensuring accountability and providing open data for research and policy decisions.

### Features

✅ **Real-time Monitoring**: Track solar panel output, efficiency, and environmental impact  
✅ **Permanent Records**: All data stored on IPFS with blockchain timestamps  
✅ **Open Data**: Anyone can verify and analyze the data  
✅ **Privacy-Preserving**: Aggregate community data while protecting individual privacy  
✅ **Mobile-Friendly**: Submit readings from smartphones  
✅ **Offline-Capable**: Cache data and sync when connected

---

## Use Cases

- **Community Solar Cooperatives**: Transparent reporting to members
- **Environmental NGOs**: Verifiable impact data for grant applications
- **Research Institutions**: Open datasets for renewable energy studies
- **Policy Advocacy**: Evidence-based arguments for renewable energy adoption
- **Local Governments**: Public transparency on municipal solar installations

---

## Quick Start

### Prerequisites

- Node.js 18+ or Python 3.9+
- IPFS node (or free Web3.Storage account)
- (Optional) Blockchain wallet with small amount of MATIC for anchoring

### Installation

```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/examples/renewable-energy-tracker

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### Configuration (.env)

```bash
# IPFS Settings
IPFS_API_URL=http://127.0.0.1:5001
# Or use Web3.Storage
WEB3_STORAGE_TOKEN=your_token_here

# Blockchain Settings (optional)
BLOCKCHAIN_RPC=https://polygon-rpc.com
PRIVATE_KEY=your_private_key_here
CONTRACT_ADDRESS=0x...

# Application Settings
PORT=3000
UPDATE_INTERVAL=300000  # 5 minutes in milliseconds
```

### Running

```bash
# Start the application
npm start

# Or in development mode
npm run dev
```

Visit `http://localhost:3000` to see the dashboard.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│          Web Interface / Mobile App         │
│     (Submit readings, view dashboard)       │
└───────────────────┬─────────────────────────┘
                    │
┌───────────────────┴─────────────────────────┐
│           Application Layer                 │
│  - Data validation                          │
│  - Aggregation & analytics                  │
│  - Privacy filtering                        │
└────┬──────────────────────────────────┬─────┘
     │                                   │
┌────▼─────────────────┐    ┌───────────▼──────────┐
│   IPFS Storage       │    │  Blockchain Anchor   │
│  - Raw readings      │    │  - Data hashes       │
│  - Daily summaries   │    │  - Timestamps        │
│  - Historical data   │    │  - Verification      │
└──────────────────────┘    └──────────────────────┘
```

---

## Data Model

### Solar Reading

```json
{
  "timestamp": "2025-12-14T10:30:00Z",
  "panelId": "community-solar-001",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "name": "Community Center Roof"
  },
  "production": {
    "currentWatts": 1250,
    "dailyKwh": 8.5,
    "lifetimeKwh": 12450
  },
  "efficiency": 0.87,
  "weather": {
    "condition": "sunny",
    "temperature": 22,
    "cloudCover": 0.1
  },
  "ipfsCID": "bafybeig...",
  "blockchainTx": "0x123abc..."
}
```

### Daily Summary

```json
{
  "date": "2025-12-14",
  "totalProduction": 45.2,
  "peakOutput": 2100,
  "avgEfficiency": 0.85,
  "carbonOffset": 22.6,
  "readingsCount": 288,
  "ipfsCID": "bafybeig...",
  "previousDayCID": "bafybeig..."
}
```

---

## API Endpoints

### Submit Reading

```bash
POST /api/readings

{
  "panelId": "community-solar-001",
  "currentWatts": 1250,
  "temperature": 22
}

Response:
{
  "success": true,
  "ipfsCID": "bafybeig...",
  "timestamp": "2025-12-14T10:30:00Z"
}
```

### Get Current Status

```bash
GET /api/status

Response:
{
  "currentOutput": 1250,
  "todayTotal": 8.5,
  "efficiency": 0.87,
  "lastUpdate": "2025-12-14T10:30:00Z"
}
```

### Get Historical Data

```bash
GET /api/history?days=30

Response:
{
  "data": [
    { "date": "2025-12-14", "production": 45.2, ... },
    ...
  ],
  "ipfsCIDs": ["bafybeig...", ...],
  "verifiable": true
}
```

---

## Implementation

### Core Logic (JavaScript)

```javascript
// solar-tracker.js
import { create } from 'ipfs-http-client';
import { ethers } from 'ethers';

class SolarTracker {
  constructor(config) {
    this.ipfs = create({ url: config.ipfsUrl });
    this.provider = new ethers.JsonRpcProvider(config.rpcUrl);
    this.contract = new ethers.Contract(
      config.contractAddress,
      contractABI,
      new ethers.Wallet(config.privateKey, this.provider)
    );
  }

  async submitReading(reading) {
    // 1. Validate data
    this.validateReading(reading);

    // 2. Add timestamp
    reading.timestamp = new Date().toISOString();

    // 3. Store on IPFS
    const { cid } = await this.ipfs.add(JSON.stringify(reading));
    reading.ipfsCID = cid.toString();

    // 4. Anchor to blockchain (hourly batches)
    if (this.shouldAnchor()) {
      const tx = await this.contract.anchorReading(cid.toString());
      reading.blockchainTx = tx.hash;
    }

    // 5. Emit event
    this.emit('reading-submitted', reading);

    return reading;
  }

  async getDailySummary(date) {
    // Aggregate all readings for the day
    const readings = await this.getReadingsForDay(date);
    
    const summary = {
      date,
      totalProduction: readings.reduce((sum, r) => sum + r.production.dailyKwh, 0),
      peakOutput: Math.max(...readings.map(r => r.production.currentWatts)),
      avgEfficiency: readings.reduce((sum, r) => sum + r.efficiency, 0) / readings.length,
      carbonOffset: this.calculateCarbonOffset(readings),
      readingsCount: readings.length
    };

    // Store summary on IPFS
    const { cid } = await this.ipfs.add(JSON.stringify(summary));
    summary.ipfsCID = cid.toString();

    return summary;
  }

  calculateCarbonOffset(readings) {
    // IMPORTANT: Carbon intensity varies by region and grid composition
    // This example uses 0.5 kg CO2 per kWh (global average)
    // Replace with your local grid's carbon intensity:
    // - US average: ~0.4 kg/kWh
    // - EU average: ~0.3 kg/kWh
    // - Coal-heavy grids: ~0.8-1.0 kg/kWh
    // - Renewable-heavy grids: ~0.1-0.2 kg/kWh
    const CARBON_INTENSITY = 0.5; // kg CO2 per kWh - CUSTOMIZE FOR YOUR REGION
    const totalKwh = readings.reduce((sum, r) => sum + r.production.dailyKwh, 0);
    return totalKwh * CARBON_INTENSITY;
  }

  validateReading(reading) {
    if (!reading.panelId) throw new Error('Panel ID required');
    if (reading.currentWatts < 0) throw new Error('Invalid wattage');
    // Additional validation...
  }
}

export default SolarTracker;
```

### Web Interface (HTML + JavaScript)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Community Solar Tracker</title>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background: #f5f5f5;
    }
    .dashboard {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    .card {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
      font-size: 2em;
      font-weight: bold;
      color: #2563eb;
    }
    .metric-label {
      color: #666;
      margin-top: 5px;
    }
    .chart {
      height: 300px;
      background: white;
      border-radius: 8px;
      padding: 20px;
    }
  </style>
</head>
<body>
  <h1>🌞 Community Solar Tracker</h1>
  <p>Real-time renewable energy monitoring on IPFS & Blockchain</p>

  <div class="dashboard">
    <div class="card">
      <div class="metric-value" id="current-output">--</div>
      <div class="metric-label">Current Output (W)</div>
    </div>
    <div class="card">
      <div class="metric-value" id="today-total">--</div>
      <div class="metric-label">Today's Total (kWh)</div>
    </div>
    <div class="card">
      <div class="metric-value" id="efficiency">--</div>
      <div class="metric-label">Efficiency (%)</div>
    </div>
    <div class="card">
      <div class="metric-value" id="carbon-offset">--</div>
      <div class="metric-label">CO₂ Offset (kg)</div>
    </div>
  </div>

  <div class="chart">
    <canvas id="production-chart"></canvas>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    // Fetch and display current status
    async function updateStatus() {
      const response = await fetch('/api/status');
      const data = await response.json();
      
      document.getElementById('current-output').textContent = data.currentOutput;
      document.getElementById('today-total').textContent = data.todayTotal.toFixed(1);
      document.getElementById('efficiency').textContent = (data.efficiency * 100).toFixed(0);
      document.getElementById('carbon-offset').textContent = data.carbonOffset.toFixed(1);
    }

    // Update every 5 minutes
    updateStatus();
    setInterval(updateStatus, 300000);

    // Load historical chart
    async function loadChart() {
      const response = await fetch('/api/history?days=7');
      const { data } = await response.json();
      
      new Chart(document.getElementById('production-chart'), {
        type: 'line',
        data: {
          labels: data.map(d => d.date),
          datasets: [{
            label: 'Daily Production (kWh)',
            data: data.map(d => d.production),
            borderColor: '#2563eb',
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }

    loadChart();
  </script>
</body>
</html>
```

---

## Deployment

### Option 1: Self-Hosted

```bash
# Install IPFS
wget https://dist.ipfs.io/kubo/v0.24.0/kubo_v0.24.0_linux-amd64.tar.gz
tar -xvzf kubo_v0.24.0_linux-amd64.tar.gz
cd kubo && sudo bash install.sh
ipfs init
ipfs daemon &

# Run the application
npm start
```

### Option 2: Cloud Deployment (Free Tier)

**Vercel/Netlify** (Frontend):
```bash
npm run build
vercel deploy
```

**Render** (Backend):
```bash
# Push to GitHub
# Connect repository to Render
# Auto-deploys on push
```

---

## Customization Guide

### Adding New Metrics

1. Update data model in `models/reading.js`
2. Add validation in `validateReading()`
3. Update dashboard UI
4. Modify IPFS storage structure if needed

### Integrating Hardware

Connect to actual solar inverters:

```javascript
// Example: SolarEdge inverter integration
import SolarEdge from 'solaredge-api';

const se = new SolarEdge({ apiKey: process.env.SOLAREDGE_API_KEY });

async function fetchRealData() {
  const power = await se.getPowerOverview();
  return {
    currentWatts: power.currentPower.power,
    dailyKwh: power.lastDayData.energy / 1000
  };
}
```

### Multi-Location Support

Track multiple installations:

```javascript
// locations.json
{
  "locations": [
    { "id": "site-1", "name": "Community Center", "capacity": 5000 },
    { "id": "site-2", "name": "School Roof", "capacity": 3000 }
  ]
}

// Aggregate across locations
async function getTotalProduction() {
  const sites = await Promise.all(
    locations.map(loc => getProductionForSite(loc.id))
  );
  return sites.reduce((sum, site) => sum + site.production, 0);
}
```

---

## Privacy Considerations

This example **intentionally makes data public** for transparency. If you need privacy:

### Aggregate Data Only

```javascript
// Don't expose exact locations
const reading = {
  region: "Northeast Quadrant",  // instead of exact coordinates
  approximateOutput: Math.round(watts / 100) * 100  // rounded
};
```

### Encrypt Sensitive Details

```javascript
import nacl from 'tweetnacl';

// Encrypt panel IDs
const encrypted = nacl.secretbox(
  Buffer.from(panelId),
  nonce,
  secretKey
);

// Public data includes only hash
reading.panelHash = hash(panelId);
```

---

## Troubleshooting

**IPFS connection fails**
- Ensure IPFS daemon is running: `ipfs daemon`
- Check IPFS API endpoint in `.env`
- Try using Web3.Storage instead

**Blockchain transactions fail**
- Verify you have sufficient MATIC for gas
- Check RPC endpoint is responding
- Reduce transaction frequency (batch updates)

**Data not updating**
- Check UPDATE_INTERVAL in config
- Verify data source connection
- Check browser console for errors

---

## Contributing

Improvements welcome!

- Add hardware integrations
- Improve visualizations
- Optimize IPFS pinning
- Reduce blockchain costs
- Mobile app version

---

## License

MIT License - See [LICENSE](../../LICENSE)

---

## Support

- **Issues**: https://github.com/hannesmitterer/Euystacio/issues
- **Community**: [Discord/Forum]
- **Email**: examples@seedbringer.org

---

*"Sunlight is free. The data about it should be too."*

—The Seedbringer Collective
