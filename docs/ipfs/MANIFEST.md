# IPFS Directory Structure and Manifest

## Framework Euystacio IPFS Manifest

This document describes the IPFS directory structure for Framework Euystacio's eternal knowledge preservation system.

---

## Overview

All critical documentation, specifications, and resources for Framework Euystacio are eternalized on IPFS to ensure permanent availability regardless of centralized platform changes.

**Primary IPFS Gateway:** Pinata  
**Backup Gateways:** IPFS.io, Cloudflare IPFS, Dweb.link  
**Pinning Strategy:** Multi-node redundancy with automated verification

---

## Directory Structure

```
/framework-euystacio/
├── /docs/
│   ├── /core/
│   │   ├── README.md
│   │   ├── SUPPORT.md
│   │   ├── NEXUS_API_SPEC.md
│   │   ├── DEPLOY_INSTRUCTIONS.md
│   │   ├── SECURITY_RUNBOOK.md
│   │   └── WEBSOCKET_EXAMPLE.md
│   │
│   ├── /technical/
│   │   ├── TECHNICAL_BLUEPRINT.md
│   │   ├── openapi.yaml
│   │   ├── tsconfig.json
│   │   └── architecture-diagrams/
│   │
│   ├── /community/
│   │   ├── CONTRIBUTING.md
│   │   ├── CODE_OF_CONDUCT.md
│   │   └── GOVERNANCE.md
│   │
│   ├── /templates/
│   │   ├── /social/
│   │   │   ├── twitter_thread.md
│   │   │   ├── reddit_ethereum.md
│   │   │   ├── reddit_cryptocurrency.md
│   │   │   ├── reddit_opensource.md
│   │   │   └── discord_announcement.md
│   │   │
│   │   ├── /email/
│   │   │   ├── ethereum_foundation.md
│   │   │   ├── protocol_labs.md
│   │   │   └── general_funders.md
│   │   │
│   │   └── /community/
│   │       ├── ama_script.md
│   │       ├── blog_post.md
│   │       └── impact_stats.md
│   │
│   └── /transparency/
│       ├── 2025-12.md
│       ├── 2026-01.md
│       └── [monthly reports...]
│
├── /contracts/
│   ├── TrustlessFundingProtocol.sol
│   └── contract-docs/
│
├── /examples/
│   ├── /renewable-energy-tracker/
│   ├── /community-knowledge-base/
│   └── /ecological-monitoring/
│
├── /scripts/
│   ├── eternalize.sh
│   ├── transparency_update.sh
│   └── webhook_setup.sh
│
└── /metadata/
    ├── MANIFEST.md (this file)
    ├── VERIFICATION.md
    └── GATEWAY_ACCESS.md
```

---

## Core Content Categories

### 1. Essential Documentation
**Path:** `/docs/core/`  
**Update Frequency:** As needed  
**Priority:** Critical

Files:
- `README.md` - Main project documentation
- `SUPPORT.md` - Funding and support information
- `NEXUS_API_SPEC.md` - Complete API specification
- `DEPLOY_INSTRUCTIONS.md` - Deployment guides
- `SECURITY_RUNBOOK.md` - Security procedures

**Purpose:** Core knowledge required to understand and use Framework Euystacio

---

### 2. Technical Specifications
**Path:** `/docs/technical/`  
**Update Frequency:** Per release  
**Priority:** High

Files:
- Technical architecture documents
- OpenAPI specifications
- Configuration files
- System diagrams

**Purpose:** Technical implementation details for developers

---

### 3. Community Resources
**Path:** `/docs/community/`  
**Update Frequency:** Quarterly  
**Priority:** Medium

Files:
- Contribution guidelines
- Code of conduct
- Governance procedures
- Community agreements

**Purpose:** Facilitate community participation and governance

---

### 4. Communication Templates
**Path:** `/docs/templates/`  
**Update Frequency:** As needed  
**Priority:** Medium

Subdirectories:
- `/social/` - Social media announcement templates
- `/email/` - Email outreach templates
- `/community/` - Community engagement resources

**Purpose:** Enable consistent communication and outreach

---

### 5. Transparency Reports
**Path:** `/docs/transparency/`  
**Update Frequency:** Monthly  
**Priority:** Critical

Files:
- Monthly financial reports (YYYY-MM.md format)
- Spending breakdowns
- Community updates
- Impact metrics

**Purpose:** Maintain complete financial and operational transparency

---

### 6. Smart Contracts
**Path:** `/contracts/`  
**Update Frequency:** Per audit  
**Priority:** Critical

Files:
- Solidity contract source code
- Contract documentation
- Audit reports
- Deployment addresses

**Purpose:** Trustless operations and on-chain transparency

---

### 7. Example Implementations
**Path:** `/examples/`  
**Update Frequency:** Quarterly  
**Priority:** Medium

Subdirectories:
- Complete working examples
- Use case demonstrations
- Integration patterns

**Purpose:** Educational resources and implementation guides

---

## IPFS Content Identifiers (CIDs)

### Latest Version CIDs

**Full Repository Snapshot:**
```
CID: [To be updated with actual CID after pinning]
Size: ~[Size]
Pinned: [Date]
Gateway: https://gateway.pinata.cloud/ipfs/[CID]
```

**Core Documentation Bundle:**
```
CID: [To be updated with actual CID after pinning]
Size: ~[Size]
Pinned: [Date]
Gateway: https://gateway.pinata.cloud/ipfs/[CID]
```

**Monthly Transparency Report (Latest):**
```
CID: [To be updated with actual CID after pinning]
Report: 2025-12
Pinned: [Date]
Gateway: https://gateway.pinata.cloud/ipfs/[CID]
```

---

## Version Control

### Version Tracking

Each major update receives a new IPFS pin with versioned naming:

**Naming Convention:**
```
framework-euystacio-v[MAJOR].[MINOR].[PATCH]-[YYYY-MM-DD]
```

**Example:**
```
framework-euystacio-v1.0.0-2025-12-15
```

### Version History

| Version | Date | CID | Notes |
|---------|------|-----|-------|
| v1.0.0 | 2025-12-15 | [CID] | Initial eternal distribution |
| v1.1.0 | TBD | [CID] | [Future updates] |

---

## Pinning Strategy

### Primary Pinning Service
**Service:** Pinata Cloud  
**Tier:** Pro Plan  
**Redundancy:** Multiple pins per content  
**Monitoring:** Automated verification every 24 hours

### Backup Pinning Services
**Services:**
- IPFS.io (public gateway)
- Cloudflare IPFS
- Web3.Storage (planned)
- Estuary (planned)

### Self-Hosted Nodes
**Status:** Planned with funding  
**Configuration:**
- IPFS Cluster for redundancy
- Geographic distribution
- Automated sync with Pinata

---

## Content Update Process

### Standard Update Workflow

1. **Local Changes**
   - Update content in repository
   - Commit to version control
   - Create release tag

2. **IPFS Upload**
   - Run `scripts/eternalize.sh`
   - Generate new CID
   - Verify content integrity

3. **Pinning**
   - Pin via Pinata API
   - Verify pin status
   - Test gateway access

4. **Documentation**
   - Update this MANIFEST.md
   - Record CID in version history
   - Update VERIFICATION.md

5. **Announcement**
   - Publish transparency report
   - Announce new CID
   - Update gateway links

---

## Access Verification

### Verification Commands

**Check content availability:**
```bash
# Via Pinata
curl -I https://gateway.pinata.cloud/ipfs/[CID]

# Via IPFS.io
curl -I https://ipfs.io/ipfs/[CID]

# Via Cloudflare
curl -I https://cloudflare-ipfs.com/ipfs/[CID]
```

**Download content:**
```bash
# Using IPFS CLI
ipfs get [CID] -o framework-euystacio

# Using curl
curl https://gateway.pinata.cloud/ipfs/[CID] -o content.tar.gz
```

**Verify integrity:**
```bash
# Calculate hash
ipfs add --only-hash -r framework-euystacio/

# Should match pinned CID
```

---

## Emergency Recovery

### If Primary Gateway Fails

1. **Use backup gateways:**
   - https://ipfs.io/ipfs/[CID]
   - https://cloudflare-ipfs.com/ipfs/[CID]
   - https://dweb.link/ipfs/[CID]

2. **Run local IPFS node:**
   ```bash
   ipfs daemon
   ipfs get [CID]
   ```

3. **Contact community:**
   - GitHub Discussions
   - Discord (if available)
   - Email: support@euystacio.io

### Content Recovery

All content can be recovered from:
- IPFS network (via CID)
- GitHub repository (source files)
- Local backups (if maintained)
- Community nodes (distributed)

---

## Monitoring & Maintenance

### Automated Checks

**Daily:**
- Pin status verification
- Gateway availability testing
- Content integrity checks

**Weekly:**
- Pin refresh (if needed)
- Gateway performance monitoring
- Storage usage tracking

**Monthly:**
- Full content audit
- Version cleanup
- Cost optimization review

### Manual Reviews

**Quarterly:**
- Content structure review
- Deprecated content removal
- Documentation updates
- Strategy reassessment

---

## Cost Tracking

### Current IPFS Costs

**Monthly:**
- Pinata Pro: $150
- Bandwidth overages: Variable
- Additional services: $50

**Projected with Growth:**
- Year 1: ~$3,600
- Year 2: ~$5,000 (with expanded content)
- Year 3: ~$7,000 (with self-hosted nodes)

**Sustainability:**
All costs tracked in monthly transparency reports with CIDs documented.

---

## Future Enhancements

### Planned Improvements

**Q1 2025:**
- [ ] Filecoin integration for long-term archival
- [ ] IPFS Cluster deployment
- [ ] IPNS for mutable pointers
- [ ] Enhanced verification automation

**Q2 2025:**
- [ ] Self-hosted IPFS nodes
- [ ] Multi-region distribution
- [ ] Advanced pinning strategies
- [ ] Performance optimization

**Q3-Q4 2025:**
- [ ] IPFS pubsub integration
- [ ] Offline-first capabilities
- [ ] Mobile IPFS support
- [ ] Educational content expansion

---

## Contact & Support

**Questions about IPFS implementation:**
- GitHub Issues: https://github.com/hannesmitterer/Euystacio/issues
- Email: support@euystacio.io
- Documentation: See GATEWAY_ACCESS.md

**Report access issues:**
- Create GitHub issue with "ipfs" label
- Include CID and gateway used
- Describe error encountered

---

## License

All content pinned to IPFS is licensed under:
- **MIT License** (code and technical documentation)
- **Sacred Commons License** (accessibility guarantee)

See repository LICENSE file for full details.

---

**Manifest Version:** 1.0.0  
**Last Updated:** December 2025  
**Maintained By:** Framework Euystacio / Seedbringer Treasury  
**Verification:** See VERIFICATION.md for cryptographic proofs
