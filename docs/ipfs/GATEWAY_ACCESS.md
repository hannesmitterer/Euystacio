# IPFS Gateway Access Guide

## Accessing Framework Euystacio Content via IPFS

This guide explains how to access Framework Euystacio documentation, code, and resources through IPFS gateways.

---

## Quick Start

### Access via Web Browser

**Format:**
```
https://[GATEWAY]/ipfs/[CID]
```

**Example:**
```
https://gateway.pinata.cloud/ipfs/QmExample123.../README.md
```

Just paste the URL in your browser - no special software needed!

---

## Available Gateways

### Primary Gateway (Recommended)

**Pinata Cloud:**
```
https://gateway.pinata.cloud/ipfs/[CID]
```

**Features:**
- ✅ High performance
- ✅ 99.9% uptime
- ✅ Global CDN
- ✅ Optimized for Framework Euystacio content

---

### Backup Gateways

**IPFS.io (Official):**
```
https://ipfs.io/ipfs/[CID]
```

**Cloudflare IPFS:**
```
https://cloudflare-ipfs.com/ipfs/[CID]
```

**Dweb.link:**
```
https://dweb.link/ipfs/[CID]
```

**Use backup gateways if:**
- Primary gateway is slow or unavailable
- You want to verify content across multiple sources
- Geographic optimization needed

---

## Access Methods

### Method 1: Direct Web Access (Easiest)

**No software installation required**

1. Get the CID from official sources:
   - GitHub README
   - MANIFEST.md file
   - Monthly transparency reports

2. Construct gateway URL:
   ```
   https://gateway.pinata.cloud/ipfs/[YOUR_CID]
   ```

3. Open in any web browser

**Example - Accessing README:**
```
https://gateway.pinata.cloud/ipfs/QmExample.../README.md
```

---

### Method 2: IPFS Desktop App

**Install IPFS Desktop for better performance**

1. **Download IPFS Desktop:**
   - Visit: https://docs.ipfs.tech/install/ipfs-desktop/
   - Available for Windows, macOS, Linux

2. **Install and run:**
   - Follow installation wizard
   - Start IPFS Desktop
   - Wait for daemon to initialize

3. **Access content locally:**
   ```
   http://localhost:8080/ipfs/[CID]
   ```

**Benefits:**
- Faster access (local caching)
- No reliance on public gateways
- Support IPFS network (become a node)
- Offline access to pinned content

---

### Method 3: IPFS Command Line

**For developers and advanced users**

1. **Install IPFS CLI:**
   ```bash
   # macOS (Homebrew)
   brew install ipfs
   
   # Linux
   wget https://dist.ipfs.tech/kubo/v0.22.0/kubo_v0.22.0_linux-amd64.tar.gz
   tar -xvzf kubo_v0.22.0_linux-amd64.tar.gz
   cd kubo
   sudo bash install.sh
   
   # Windows
   # Download from https://dist.ipfs.tech/kubo/
   ```

2. **Initialize IPFS:**
   ```bash
   ipfs init
   ```

3. **Start daemon:**
   ```bash
   ipfs daemon
   ```

4. **Get content:**
   ```bash
   # Download to current directory
   ipfs get [CID]
   
   # Download to specific location
   ipfs get [CID] -o /path/to/destination
   
   # Cat file contents (small files)
   ipfs cat [CID]/README.md
   ```

**Advanced commands:**
```bash
# List directory contents
ipfs ls [CID]

# Get file info
ipfs object stat [CID]

# Pin content locally (keep forever)
ipfs pin add [CID]

# Check pin status
ipfs pin ls [CID]
```

---

## Content Organization

### Root CID Structure

When you access the root CID, you'll see:

```
/
├── README.md
├── SUPPORT.md
├── docs/
│   ├── NEXUS_API_SPEC.md
│   ├── DEPLOY_INSTRUCTIONS.md
│   └── ...
├── templates/
│   ├── social/
│   └── email/
├── contracts/
└── examples/
```

### Accessing Specific Files

**Format:**
```
https://[GATEWAY]/ipfs/[ROOT_CID]/[PATH]/[FILE]
```

**Examples:**
```
# README.md
https://gateway.pinata.cloud/ipfs/QmRoot.../README.md

# API Spec
https://gateway.pinata.cloud/ipfs/QmRoot.../docs/NEXUS_API_SPEC.md

# Social template
https://gateway.pinata.cloud/ipfs/QmRoot.../templates/social/twitter_thread.md
```

---

## Current Content CIDs

### Latest Version

**Full Repository (v1.0.0):**
```
CID: [To be updated after pinning]
Size: ~[Size] MB
Pinned: December 2025
```

**Access:**
```
https://gateway.pinata.cloud/ipfs/[CID]
```

### Documentation Bundle

**Core Docs Only:**
```
CID: [To be updated after pinning]
Size: ~[Size] MB
Contents: README, SUPPORT, API Spec, Deployment guides
```

### Monthly Reports

**December 2025 Transparency Report:**
```
CID: [To be updated after first report]
Path: /docs/transparency/2025-12.md
```

**Access:**
```
https://gateway.pinata.cloud/ipfs/[REPORT_CID]
```

---

## Performance Tips

### For Faster Access

1. **Use geographically close gateway:**
   - Pinata: Global CDN (usually fastest)
   - IPFS.io: Varies by location
   - Cloudflare: Excellent global coverage

2. **Run local IPFS node:**
   - Cache content locally
   - Serve from your machine
   - Contribute to network

3. **Pin frequently accessed content:**
   ```bash
   ipfs pin add [CID]
   ```

4. **Use direct file links:**
   - Instead of browsing directories
   - Reduces gateway load
   - Faster response

---

## Downloading Content

### Download Entire Repository

**Via Browser:**
1. Navigate to root CID
2. Look for download/archive option (gateway dependent)
3. Save to disk

**Via CLI:**
```bash
# Download everything
ipfs get [ROOT_CID] -o framework-euystacio

# Navigate contents
cd framework-euystacio
ls -la
```

### Download Specific Files

**Via wget/curl:**
```bash
# Single file
wget https://gateway.pinata.cloud/ipfs/[CID]/README.md

# Multiple files
curl https://gateway.pinata.cloud/ipfs/[CID]/docs/SUPPORT.md -o SUPPORT.md
```

**Via IPFS CLI:**
```bash
# Specific file
ipfs get [CID]/README.md -o README.md

# Entire directory
ipfs get [CID]/docs/ -o docs/
```

---

## Verifying Content

### Always Verify Downloads

Before using downloaded content, verify authenticity:

1. **Check CID matches:**
   ```bash
   ipfs add --only-hash [DOWNLOADED_FILE]
   # Compare output with expected CID
   ```

2. **Verify from multiple gateways:**
   - Download from 2-3 different gateways
   - Compare file hashes
   - Should be identical

3. **Cross-reference with GitHub:**
   - Compare with official repository
   - Check Git commit hash

See [VERIFICATION.md](./VERIFICATION.md) for complete verification guide.

---

## Offline Access

### Save Content for Offline Use

**Method 1: IPFS Pin**
```bash
# Pin content to your local node
ipfs pin add [CID]

# Content remains accessible even offline
ipfs cat [CID]/README.md
```

**Method 2: Regular Download**
```bash
# Download to filesystem
ipfs get [CID] -o framework-euystacio

# Access normally
cd framework-euystacio
cat README.md
```

**Method 3: Browser Caching**
- Use IPFS browser extension
- Content cached locally
- Available without internet

---

## Mobile Access

### Accessing on Mobile Devices

**Web Browser:**
- Works on any mobile browser
- Use same gateway URLs
- May be slower on mobile networks

**IPFS Mobile Apps:**

**iOS:**
- IPFS Browser (App Store)
- Brave Browser (has IPFS support)

**Android:**
- IPFS Lite
- Brave Browser
- Opera (experimental IPFS support)

**Tips:**
- Use WiFi for large downloads
- Bookmark frequently accessed CIDs
- Consider data usage

---

## Integration Examples

### Embed in Website

```html
<!-- Embed README -->
<iframe 
  src="https://gateway.pinata.cloud/ipfs/[CID]/README.md"
  width="100%" 
  height="600">
</iframe>
```

### Fetch via JavaScript

```javascript
// Using fetch API
async function getIPFSContent(cid, path) {
  const url = `https://gateway.pinata.cloud/ipfs/${cid}/${path}`;
  const response = await fetch(url);
  const content = await response.text();
  return content;
}

// Usage
const readme = await getIPFSContent('QmExample...', 'README.md');
console.log(readme);
```

### Fetch via Python

```python
import requests

def get_ipfs_content(cid, path=''):
    url = f"https://gateway.pinata.cloud/ipfs/{cid}/{path}"
    response = requests.get(url)
    return response.text

# Usage
readme = get_ipfs_content('QmExample...', 'README.md')
print(readme)
```

---

## Troubleshooting

### Common Issues

**Problem: Gateway timeout**
```
Solution: 
1. Try different gateway
2. Wait and retry (content may be loading)
3. Use local IPFS node
```

**Problem: 404 Not Found**
```
Solution:
1. Verify CID is correct
2. Check CID from official source
3. Content may not be pinned yet
4. Try alternative gateway
```

**Problem: Slow loading**
```
Solution:
1. Use geographically closer gateway
2. Run local IPFS node
3. Pin content locally for repeated access
4. Check internet connection
```

**Problem: Content differs from expected**
```
Solution:
1. VERIFY IMMEDIATELY (see VERIFICATION.md)
2. Do not use the content
3. Report to security@euystacio.io
4. Wait for official clarification
```

---

## Gateway Status

### Check Gateway Health

**Pinata Status:**
```
https://status.pinata.cloud/
```

**IPFS.io Status:**
```
https://twitter.com/IPFS
```

**Community Check:**
```bash
# Test gateway response time
time curl -I https://gateway.pinata.cloud/ipfs/[KNOWN_CID]
```

---

## Support & Resources

### Getting Help

**Documentation:**
- IPFS Docs: https://docs.ipfs.tech/
- Pinata Docs: https://docs.pinata.cloud/
- Framework Euystacio: https://github.com/hannesmitterer/Euystacio

**Support Channels:**
- GitHub Issues: https://github.com/hannesmitterer/Euystacio/issues
- Email: support@euystacio.io
- IPFS Forums: https://discuss.ipfs.tech/

**Report Problems:**
- Gateway issues → gateway provider
- Content verification issues → security@euystacio.io
- General questions → GitHub Discussions

---

## Best Practices

### Recommended Practices

1. **Bookmark official CID sources:**
   - GitHub MANIFEST.md
   - Official website
   - Monthly transparency reports

2. **Use multiple gateways:**
   - For verification
   - For redundancy
   - For performance

3. **Run local node (if possible):**
   - Supports IPFS network
   - Faster access
   - Offline capability

4. **Verify all content:**
   - Check CIDs match
   - Compare across gateways
   - Cross-reference with Git

5. **Keep updated:**
   - Follow official announcements
   - Check for new versions
   - Update pinned content

---

## Contributing to IPFS Network

### Help Distribute Content

**Run an IPFS node and pin Framework Euystacio content:**

```bash
# Install and start IPFS
ipfs init
ipfs daemon

# Pin official content
ipfs pin add [OFFICIAL_CID]

# Check pin status
ipfs pin ls [OFFICIAL_CID]
```

**Benefits:**
- Help ensure content availability
- Support decentralization
- Reduce gateway load
- Contribute to resilience

---

**Document Version:** 1.0.0  
**Last Updated:** December 2025  
**Next Review:** Quarterly  
**Official CIDs:** See MANIFEST.md for current CIDs
