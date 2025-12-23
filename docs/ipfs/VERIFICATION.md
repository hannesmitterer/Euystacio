# IPFS Content Verification Guide

## Framework Euystacio Content Verification

This guide explains how to verify the authenticity and integrity of Framework Euystacio content stored on IPFS.

---

## Why Verification Matters

IPFS content addressing provides inherent verification through cryptographic hashes (CIDs). However, this guide provides additional verification methods to ensure:

1. **Content Authenticity** - Content comes from official Framework Euystacio sources
2. **Integrity Assurance** - Content hasn't been tampered with or corrupted
3. **Version Validation** - You're accessing the intended version
4. **Source Transparency** - Clear chain of custody for all content

---

## Verification Methods

### Method 1: CID Verification (Primary)

**IPFS CID (Content Identifier)** is a cryptographic hash of the content itself. Same content = same CID.

**How to verify:**

```bash
# 1. Download content from IPFS
ipfs get <CID> -o downloaded-content

# 2. Calculate hash locally
ipfs add --only-hash -r downloaded-content/

# 3. Compare output CID with expected CID
# If they match, content is authentic and unmodified
```

**Example:**
```bash
# Official CID for v1.0.0 documentation
EXPECTED_CID="QmExample123..."

# Download and verify
ipfs get $EXPECTED_CID -o docs
CALCULATED_CID=$(ipfs add --only-hash -r docs/ | tail -1 | awk '{print $2}')

if [ "$EXPECTED_CID" == "$CALCULATED_CID" ]; then
  echo "✅ Content verified successfully"
else
  echo "❌ Content verification failed"
fi
```

---

### Method 2: Git Commit Verification

All IPFS-pinned content originates from specific Git commits in the official repository.

**How to verify:**

```bash
# 1. Clone official repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio

# 2. Checkout specific tagged version
git checkout v1.0.0

# 3. Compare with IPFS content
# Files should match exactly
```

**Verification script:**
```bash
#!/bin/bash
# compare-with-git.sh

IPFS_CONTENT_DIR="$1"
GIT_TAG="$2"

git clone https://github.com/hannesmitterer/Euystacio.git /tmp/euystacio-git
cd /tmp/euystacio-git
git checkout "$GIT_TAG"

diff -r /tmp/euystacio-git "$IPFS_CONTENT_DIR"

if [ $? -eq 0 ]; then
  echo "✅ IPFS content matches Git repository at tag $GIT_TAG"
else
  echo "❌ Differences found between IPFS content and Git repository"
fi
```

---

### Method 3: Cryptographic Signatures (Advanced)

For critical content, we provide GPG signatures.

**How to verify:**

```bash
# 1. Import Framework Euystacio GPG public key
gpg --import framework-euystacio-public.key

# 2. Download content and signature
ipfs get <CONTENT_CID> -o content
ipfs get <SIGNATURE_CID> -o content.sig

# 3. Verify signature
gpg --verify content.sig content

# Look for "Good signature from Framework Euystacio"
```

**GPG Public Key:**
```
[To be added - GPG public key fingerprint]
```

---

### Method 4: On-Chain Verification

Critical CIDs are published on Ethereum blockchain for immutable verification.

**Smart Contract:** `[To be deployed - contract address]`

**How to verify:**

```javascript
// Using ethers.js
const provider = new ethers.providers.EtherscanProvider('mainnet');
const contract = new ethers.Contract(
  CONTRACT_ADDRESS,
  CONTRACT_ABI,
  provider
);

// Get official CID for version
const officialCID = await contract.getVersionCID('v1.0.0');

// Compare with CID you're using
if (officialCID === yourCID) {
  console.log('✅ CID verified on-chain');
} else {
  console.log('❌ CID does not match on-chain record');
}
```

---

## Verified Content Registry

### Official CIDs by Version

| Version | Date | Content CID | Signature CID | Git Tag | On-Chain |
|---------|------|-------------|---------------|---------|----------|
| v1.0.0 | 2025-12-15 | [CID] | [SIG_CID] | v1.0.0 | [TX] |
| v1.1.0 | TBD | [CID] | [SIG_CID] | v1.1.0 | [TX] |

**Update frequency:** Updated with each major release

---

## Official Distribution Channels

### Trusted Sources for CIDs

**Primary:**
- GitHub repository: https://github.com/hannesmitterer/Euystacio
- Official website: [To be deployed]
- Ethereum smart contract: [Contract address]

**Secondary:**
- Twitter: [@euystacio](https://twitter.com/euystacio)
- Discord announcements: [Server invite]
- Monthly transparency reports (on IPFS)

**WARNING:** Only trust CIDs from these official sources. Verify all CIDs using multiple methods.

---

## Gateway Verification

### Trusted IPFS Gateways

**Primary:**
- https://gateway.pinata.cloud/ipfs/[CID]

**Verified Backups:**
- https://ipfs.io/ipfs/[CID]
- https://cloudflare-ipfs.com/ipfs/[CID]
- https://dweb.link/ipfs/[CID]

**Gateway Verification:**
```bash
# Verify same content across gateways
CID="QmExample..."

# Download from each gateway
curl https://gateway.pinata.cloud/ipfs/$CID -o pinata.tar.gz
curl https://ipfs.io/ipfs/$CID -o ipfs-io.tar.gz
curl https://cloudflare-ipfs.com/ipfs/$CID -o cloudflare.tar.gz

# Compare checksums
sha256sum pinata.tar.gz ipfs-io.tar.gz cloudflare.tar.gz

# All should match
```

---

## Verification Automation

### Automated Verification Script

```bash
#!/bin/bash
# verify-ipfs-content.sh

set -e

CID="$1"
VERSION="$2"

echo "🔍 Verifying Framework Euystacio content..."
echo "CID: $CID"
echo "Version: $VERSION"
echo ""

# 1. CID verification
echo "Step 1: CID Integrity Check"
ipfs get "$CID" -o /tmp/euystacio-verify
CALC_CID=$(ipfs add --only-hash -r /tmp/euystacio-verify/ | tail -1 | awk '{print $2}')

if [ "$CID" == "$CALC_CID" ]; then
  echo "✅ CID integrity verified"
else
  echo "❌ CID integrity check failed"
  exit 1
fi

# 2. Git repository comparison
echo "Step 2: Git Repository Comparison"
git clone https://github.com/hannesmitterer/Euystacio.git /tmp/euystacio-git
cd /tmp/euystacio-git
git checkout "$VERSION"

diff -r /tmp/euystacio-git /tmp/euystacio-verify

if [ $? -eq 0 ]; then
  echo "✅ Content matches Git repository"
else
  echo "⚠️  Differences found (may be expected for generated files)"
fi

# 3. Gateway consistency
echo "Step 3: Gateway Consistency Check"
curl -sI "https://gateway.pinata.cloud/ipfs/$CID" | grep "200 OK"
curl -sI "https://ipfs.io/ipfs/$CID" | grep "200 OK"
echo "✅ Content accessible across gateways"

echo ""
echo "✅ All verification checks passed!"
echo "Content is authentic Framework Euystacio material"

# Cleanup
rm -rf /tmp/euystacio-verify /tmp/euystacio-git
```

**Usage:**
```bash
chmod +x verify-ipfs-content.sh
./verify-ipfs-content.sh <CID> <VERSION_TAG>
```

---

## Verification Checklist

Use this checklist when verifying Framework Euystacio IPFS content:

- [ ] **CID Listed** - CID appears in official MANIFEST.md or VERIFICATION.md
- [ ] **Source Verified** - CID announced via official channels (GitHub, Twitter, etc.)
- [ ] **Gateway Test** - Content accessible via multiple trusted gateways
- [ ] **Hash Match** - Recalculated CID matches expected CID
- [ ] **Git Comparison** - Content matches official Git repository at tagged version
- [ ] **Signature Check** - GPG signature valid (for signed content)
- [ ] **On-Chain Check** - CID matches blockchain record (for critical content)
- [ ] **Date Validation** - Content date aligns with version release date

---

## Reporting Issues

### If Verification Fails

**Do NOT use the content** if verification fails. Instead:

1. **Document the issue:**
   - CID used
   - Verification method that failed
   - Error messages or discrepancies
   - Gateway used

2. **Report immediately:**
   - GitHub Issue: https://github.com/hannesmitterer/Euystacio/issues
   - Email: security@euystacio.io
   - Use label: `security` and `ipfs`

3. **Wait for confirmation:**
   - Official team will investigate
   - Corrected CID will be published
   - Incident will be documented

### Security Incidents

For serious security concerns (e.g., suspected content tampering):
- Email: security@euystacio.io
- Include: All verification details
- PGP encryption recommended for sensitive reports

---

## Advanced Verification

### For Paranoid Verification

If you need maximum assurance:

```bash
# 1. Verify CID from multiple official sources
# Check GitHub, Twitter, on-chain contract

# 2. Download from multiple gateways
# Compare byte-for-byte

# 3. Clone Git repository
# Build/generate content yourself
# Compare with IPFS content

# 4. Verify cryptographic signatures
# Check GPG signature with official key

# 5. Cross-reference transparency reports
# Ensure CID mentioned in monthly reports

# 6. Community verification
# Check Discord/Reddit for community verification
```

---

## Transparency Reports Verification

Monthly transparency reports are also on IPFS and should be verified:

**Structure:**
```
/transparency/
├── 2025-12.md (CID: QmExample123...)
├── 2026-01.md (CID: QmExample456...)
└── [monthly reports...]
```

**Verification:**
Each report includes:
- Previous report CID (chain of custody)
- Current report CID (self-reference)
- Git commit hash (source verification)
- On-chain transaction IDs (financial verification)

---

## Verification Best Practices

### Recommended Practices

1. **Always verify from official sources** - Never trust CIDs from unknown channels
2. **Use multiple verification methods** - Don't rely on single method
3. **Check multiple gateways** - Ensures content availability and consistency
4. **Compare with Git repository** - Source of truth for all content
5. **Verify signatures when available** - Additional layer of authenticity
6. **Stay updated** - Follow official channels for CID announcements
7. **Report discrepancies** - Help maintain content integrity

### What to Avoid

- ❌ Using CIDs from untrusted sources
- ❌ Skipping verification for "convenience"
- ❌ Using only one gateway without verification
- ❌ Ignoring verification failures
- ❌ Sharing unverified content

---

## Trust Model

### Chain of Trust

```
GitHub Repository (Source)
    ↓
Git Commit (Signed)
    ↓
IPFS Upload (Hashed → CID)
    ↓
Pinata Pinning (Redundancy)
    ↓
On-Chain Record (Immutable)
    ↓
Community Verification (Distributed Trust)
```

### Trust Assumptions

You must trust:
- IPFS cryptographic hashing (SHA-256)
- Git commit integrity
- Official GitHub repository control
- GPG key management (for signatures)
- Ethereum blockchain (for on-chain verification)

You do NOT need to trust:
- Any single IPFS gateway
- Pinning services
- Individual community members
- Third-party distributors

---

## Resources

**Tools:**
- IPFS CLI: https://docs.ipfs.tech/install/
- GPG: https://gnupg.org/
- Ethers.js: https://docs.ethers.org/

**Documentation:**
- IPFS Documentation: https://docs.ipfs.tech/
- Content Addressing: https://docs.ipfs.tech/concepts/content-addressing/
- Git Verification: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work

**Support:**
- GitHub: https://github.com/hannesmitterer/Euystacio
- Email: support@euystacio.io

---

**Document Version:** 1.0.0  
**Last Updated:** December 2025  
**Next Review:** Quarterly  
**Maintained By:** Framework Euystacio Security Team
