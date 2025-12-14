# Ecological Monitoring System
## Track Environmental Health with Verifiable Data

**A Seedbringer Example Project**

Monitor biodiversity, water quality, soil health, and other environmental indicators with permanent, tamper-proof records.

---

## Overview

This system enables communities, NGOs, and citizen scientists to collect, verify, and share environmental data that cannot be altered or deleted—creating accountability for environmental protection.

### Key Features

✅ **Multi-Sensor Support**: Water quality, air quality, biodiversity observations, soil metrics  
✅ **Verifiable Evidence**: All data anchored to blockchain for legal/scientific validity  
✅ **Community Science**: Anyone can contribute observations  
✅ **Visual Mapping**: Geographic visualization of environmental data  
✅ **Trend Analysis**: Track changes over time  
✅ **Automated Alerts**: Notifications when thresholds are exceeded  
✅ **Mobile-First**: Field data collection via smartphone

---

## Use Cases

- **Water Quality Monitoring**: Citizen testing of rivers, lakes, wells
- **Biodiversity Tracking**: Species observations, population counts
- **Air Quality**: Community air monitoring in industrial areas
- **Soil Health**: Agricultural soil testing and organic matter tracking
- **Pollution Documentation**: Evidence collection for advocacy
- **Climate Change Indicators**: Long-term environmental trend monitoring

---

## Data Types Supported

### Water Quality
- pH, temperature, dissolved oxygen
- Turbidity, conductivity
- Nitrates, phosphates
- Bacterial contamination

### Air Quality
- PM2.5, PM10
- CO2, CO, NO2
- Ozone, VOCs
- Temperature, humidity

### Biodiversity
- Species observations
- Population counts
- Habitat assessment
- Phenology (seasonal events)

### Soil
- pH, moisture
- NPK levels
- Organic matter
- Compaction

---

## Quick Start

### Prerequisites

- Python 3.9+ or Node.js 18+
- IPFS node or Web3.Storage account
- GPS-enabled smartphone for field data

### Installation

```bash
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/examples/ecological-monitoring

# Python version
pip install -r requirements.txt
python app.py

# Or Node.js version
npm install
npm start
```

---

## Data Model

### Observation Record

```json
{
  "id": "obs-20251214-001",
  "timestamp": "2025-12-14T10:30:00Z",
  "type": "water-quality",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "accuracy": 5,
    "name": "Hudson River at Pier 45"
  },
  "measurements": {
    "ph": 7.2,
    "temperature": 18.5,
    "dissolvedOxygen": 8.2,
    "turbidity": 12
  },
  "observer": {
    "id": "QmUser123...",
    "name": "Jane Doe",
    "certified": true
  },
  "equipment": {
    "sensor": "Water Quality Probe Model X",
    "calibrationDate": "2025-12-01"
  },
  "photos": ["QmPhoto1...", "QmPhoto2..."],
  "notes": "Clear day, moderate flow",
  "ipfsCID": "bafybeig...",
  "blockchainTx": "0x123abc...",
  "verified": true
}
```

---

## Implementation Example (Python)

```python
# ecological_monitor.py
import json
from datetime import datetime
import ipfshttpclient
from web3 import Web3
import gps

class EcologicalMonitor:
    def __init__(self, ipfs_api, web3_provider, contract_address):
        self.ipfs = ipfshttpclient.connect(ipfs_api)
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract = self.w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    
    def record_observation(self, observation_type, measurements, photos=None):
        """Record an environmental observation"""
        
        # Get GPS location
        location = self.get_current_location()
        
        # Create observation record
        observation = {
            'id': self.generate_id(),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'type': observation_type,
            'location': location,
            'measurements': measurements,
            'observer': self.get_observer_info(),
            'photos': photos or [],
            'notes': ''
        }
        
        # Upload photos to IPFS
        if photos:
            observation['photos'] = [self.upload_photo(photo) for photo in photos]
        
        # Store observation on IPFS
        observation_json = json.dumps(observation)
        ipfs_result = self.ipfs.add_json(observation_json)
        observation['ipfsCID'] = ipfs_result
        
        # Anchor to blockchain
        tx_hash = self.anchor_to_blockchain(ipfs_result)
        observation['blockchainTx'] = tx_hash
        observation['verified'] = True
        
        print(f"Observation recorded: {observation['id']}")
        print(f"IPFS: {ipfs_result}")
        print(f"Blockchain: {tx_hash}")
        
        return observation
    
    def get_current_location(self):
        """Get GPS coordinates"""
        # In real implementation, use actual GPS library
        return {
            'lat': 40.7128,
            'lon': -74.0060,
            'accuracy': 5,
            'name': 'Current Location'
        }
    
    def upload_photo(self, photo_path):
        """Upload photo to IPFS"""
        with open(photo_path, 'rb') as file:
            result = self.ipfs.add(file)
            return result['Hash']
    
    def anchor_to_blockchain(self, ipfs_cid):
        """Anchor IPFS CID to blockchain"""
        # Build transaction
        tx = self.contract.functions.recordObservation(ipfs_cid).buildTransaction({
            'from': self.w3.eth.default_account,
            'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return self.w3.toHex(tx_hash)
    
    def query_observations(self, location_bounds=None, date_range=None, obs_type=None):
        """Query historical observations"""
        # Implementation would query IPFS/blockchain
        pass
    
    def generate_report(self, observations):
        """Generate environmental report"""
        report = {
            'period': f"{observations[0]['timestamp']} to {observations[-1]['timestamp']}",
            'total_observations': len(observations),
            'types': {},
            'alerts': []
        }
        
        # Analyze observations
        for obs in observations:
            obs_type = obs['type']
            report['types'][obs_type] = report['types'].get(obs_type, 0) + 1
            
            # Check for alerts
            alerts = self.check_thresholds(obs)
            report['alerts'].extend(alerts)
        
        return report
    
    def check_thresholds(self, observation):
        """Check if measurements exceed safety thresholds"""
        alerts = []
        
        thresholds = {
            'water-quality': {
                'ph': (6.5, 8.5),
                'dissolvedOxygen': (5.0, None),
                'turbidity': (None, 50)
            }
        }
        
        if observation['type'] in thresholds:
            for param, (min_val, max_val) in thresholds[observation['type']].items():
                if param in observation['measurements']:
                    value = observation['measurements'][param]
                    
                    if min_val and value < min_val:
                        alerts.append({
                            'type': 'below_threshold',
                            'parameter': param,
                            'value': value,
                            'threshold': min_val
                        })
                    
                    if max_val and value > max_val:
                        alerts.append({
                            'type': 'above_threshold',
                            'parameter': param,
                            'value': value,
                            'threshold': max_val
                        })
        
        return alerts

# Usage example
monitor = EcologicalMonitor(
    ipfs_api='/ip4/127.0.0.1/tcp/5001',
    web3_provider='https://polygon-rpc.com',
    contract_address='0x...'
)

# Record water quality observation
observation = monitor.record_observation(
    observation_type='water-quality',
    measurements={
        'ph': 7.2,
        'temperature': 18.5,
        'dissolvedOxygen': 8.2,
        'turbidity': 12
    },
    photos=['photo1.jpg', 'photo2.jpg']
)

# Generate report
observations = [observation]  # In reality, query historical data
report = monitor.generate_report(observations)
print(json.dumps(report, indent=2))
```

---

## Mobile App Interface

Simple HTML/JavaScript interface for field use:

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EcoMonitor</title>
  <style>
    body { font-family: sans-serif; padding: 20px; max-width: 600px; margin: 0 auto; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; }
    input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
    button { background: #2563eb; color: white; padding: 15px; border: none; border-radius: 4px; width: 100%; font-size: 1em; }
    .location { background: #f0f0f0; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
    .photo-preview { max-width: 100%; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>🌍 EcoMonitor</h1>
  <p>Record environmental observations</p>

  <div class="location">
    <strong>📍 Location:</strong> <span id="location">Getting GPS...</span>
  </div>

  <div class="form-group">
    <label>Observation Type</label>
    <select id="obs-type">
      <option value="water-quality">Water Quality</option>
      <option value="air-quality">Air Quality</option>
      <option value="biodiversity">Biodiversity</option>
      <option value="soil">Soil</option>
    </select>
  </div>

  <div id="water-quality-fields">
    <div class="form-group">
      <label>pH</label>
      <input type="number" step="0.1" id="ph" placeholder="7.0">
    </div>
    <div class="form-group">
      <label>Temperature (°C)</label>
      <input type="number" step="0.1" id="temperature">
    </div>
    <div class="form-group">
      <label>Dissolved Oxygen (mg/L)</label>
      <input type="number" step="0.1" id="do">
    </div>
  </div>

  <div class="form-group">
    <label>Photos</label>
    <input type="file" accept="image/*" capture="environment" multiple id="photos">
    <div id="photo-previews"></div>
  </div>

  <div class="form-group">
    <label>Notes</label>
    <textarea id="notes" rows="3" placeholder="Additional observations..."></textarea>
  </div>

  <button onclick="submitObservation()">📤 Submit Observation</button>

  <script>
    // Get GPS location
    navigator.geolocation.getCurrentPosition(position => {
      document.getElementById('location').textContent = 
        `${position.coords.latitude.toFixed(4)}, ${position.coords.longitude.toFixed(4)}`;
    });

    // Photo preview
    document.getElementById('photos').addEventListener('change', function(e) {
      const previews = document.getElementById('photo-previews');
      previews.innerHTML = '';
      
      Array.from(e.target.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = document.createElement('img');
          img.src = e.target.result;
          img.className = 'photo-preview';
          previews.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    });

    async function submitObservation() {
      const data = {
        type: document.getElementById('obs-type').value,
        measurements: {
          ph: parseFloat(document.getElementById('ph').value),
          temperature: parseFloat(document.getElementById('temperature').value),
          dissolvedOxygen: parseFloat(document.getElementById('do').value)
        },
        notes: document.getElementById('notes').value
      };

      // Submit to backend
      const response = await fetch('/api/observations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      alert(`Observation recorded!\nIPFS: ${result.ipfsCID}\nBlockchain: ${result.blockchainTx}`);
    }
  </script>
</body>
</html>
```

---

## Visualization Dashboard

Display environmental data on a map:

```javascript
// Use Leaflet.js for mapping
import L from 'leaflet';

const map = L.map('map').setView([40.7128, -74.0060], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add observation markers
observations.forEach(obs => {
  const color = getColorForValue(obs.measurements.ph);
  
  L.circleMarker([obs.location.lat, obs.location.lon], {
    radius: 8,
    fillColor: color,
    color: '#000',
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
  })
  .bindPopup(`
    <strong>${obs.type}</strong><br>
    pH: ${obs.measurements.ph}<br>
    Temperature: ${obs.measurements.temperature}°C<br>
    <a href="https://ipfs.io/ipfs/${obs.ipfsCID}">View on IPFS</a>
  `)
  .addTo(map);
});
```

---

## Deployment

### Raspberry Pi Field Station

Deploy monitoring stations that continuously collect and upload data:

```bash
# Install on Raspberry Pi
sudo apt-get update
sudo apt-get install python3-pip ipfs

# Install sensors (example: Atlas Scientific)
pip3 install atlas-i2c

# Set up autostart
sudo systemctl enable ecological-monitor
```

### Cloud Backend

Process and visualize data:

```bash
# Deploy to cloud
git push heroku main

# Or use Docker
docker build -t ecomonitor .
docker run -p 8080:8080 ecomonitor
```

---

## Integration with Sensors

### Example: Water Quality Sensor

```python
from atlas_i2c import AtlasI2C

# Connect to Atlas Scientific pH sensor
ph_sensor = AtlasI2C(address=99)  # pH sensor default address

def read_ph():
    ph_sensor.write("R")
    time.sleep(1)
    response = ph_sensor.read()
    return float(response.split(":")[1])

# Record observation with sensor data
observation = monitor.record_observation(
    observation_type='water-quality',
    measurements={
        'ph': read_ph(),
        'temperature': read_temperature_sensor(),
        'dissolvedOxygen': read_do_sensor()
    }
)
```

---

## Contributing

Improvements needed:
- Additional sensor integrations
- Machine learning for anomaly detection
- Mobile app (React Native/Flutter)
- Advanced data visualization
- Multi-language support

---

## License

MIT License

---

*"What we measure, we can protect. What we record, we cannot deny."*

—The Seedbringer Collective
