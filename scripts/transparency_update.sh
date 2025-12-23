#!/bin/bash
#
# Transparency Update Script for Framework Euystacio
# Automates monthly transparency report generation and publishing
#
# Usage: ./transparency_update.sh [month] [year]
# Example: ./transparency_update.sh 12 2025
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRANSPARENCY_DIR="$REPO_ROOT/docs/transparency"
ETHEREUM_ADDRESS="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
BITCOIN_ADDRESS="bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

# Get month and year from args or use current
MONTH=${1:-$(date +%m)}
YEAR=${2:-$(date +%Y)}
REPORT_FILE="$TRANSPARENCY_DIR/${YEAR}-${MONTH}.md"

echo -e "${GREEN}Framework Euystacio Transparency Update${NC}"
echo "========================================"
echo "Month: $MONTH"
echo "Year: $YEAR"
echo ""

# Create transparency directory if it doesn't exist
mkdir -p "$TRANSPARENCY_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Ethereum balance (requires curl and Etherscan API key)
# Note: This is a placeholder. To enable:
# 1. Get API key from https://etherscan.io/myapikey
# 2. Set ETHERSCAN_API_KEY environment variable
# 3. Uncomment the implementation below
get_eth_balance() {
    # if command_exists curl && [[ -n "$ETHERSCAN_API_KEY" ]]; then
    #     echo "Fetching Ethereum balance..."
    #     BALANCE=$(curl -s "https://api.etherscan.io/api?module=account&action=balance&address=${ETHEREUM_ADDRESS}&tag=latest&apikey=${ETHERSCAN_API_KEY}")
    #     # Parse and return balance
    #     echo "$BALANCE"
    # else
        echo "[Etherscan API integration not configured - set ETHERSCAN_API_KEY environment variable]"
    # fi
}

# Function to generate report template
generate_report_template() {
    local file=$1
    
    cat > "$file" <<'EOF'
# Transparency Report - {{MONTH_NAME}} {{YEAR}}

## Framework Euystacio - Seedbringer Treasury

**Report Period:** {{YEAR}}-{{MONTH}}-01 to {{YEAR}}-{{MONTH}}-{{LAST_DAY}}  
**Report Generated:** {{GENERATION_DATE}}  
**Report Version:** 1.0

---

## Executive Summary

**Key Metrics:**
- Total Funding Received: ${{TOTAL_FUNDING}} USD
- Total Spending: ${{TOTAL_SPENDING}} USD
- Current Runway: {{RUNWAY_MONTHS}} months
- Collapse Risk: {{COLLAPSE_RISK}}%
- Active Contributors: {{CONTRIBUTORS}}

**Highlights:**
- [List major accomplishments]
- [List significant developments]
- [List community milestones]

---

## Financial Overview

### Income

**Cryptocurrency Contributions:**
| Date | Type | Amount | Address | Transaction Hash |
|------|------|--------|---------|------------------|
| {{DATE}} | ETH | {{AMOUNT}} ETH | {{FROM_ADDRESS}} | {{TX_HASH}} |
| {{DATE}} | BTC | {{AMOUNT}} BTC | {{FROM_ADDRESS}} | {{TX_HASH}} |

**Total Income This Month:** ${{MONTHLY_INCOME}} USD

**Cumulative Funding (All-Time):** ${{TOTAL_FUNDING}} USD

### Expenses

**Category Breakdown:**

| Category | Amount | Percentage | Description |
|----------|--------|------------|-------------|
| IPFS & Infrastructure | ${{INFRA_COST}} | 37.5% | Pinata, hosting, storage |
| Development | ${{DEV_COST}} | 50% | Maintenance, features, fixes |
| Security | ${{SEC_COST}} | 12.5% | Audits, vulnerability assessment |
| **Total** | ${{TOTAL_SPENDING}} | 100% | |

**Detailed Expenses:**

1. **IPFS & Infrastructure (${{INFRA_COST}})**
   - Pinata Pro Plan: ${{PINATA_COST}}
   - Additional hosting: ${{HOSTING_COST}}
   - Bandwidth: ${{BANDWIDTH_COST}}
   - Domain renewals: ${{DOMAIN_COST}}

2. **Development (${{DEV_COST}})**
   - Core development ({{DEV_HOURS}} hours): ${{DEV_HOURS_COST}}
   - Code reviews: ${{REVIEW_COST}}
   - Testing and QA: ${{QA_COST}}

3. **Security (${{SEC_COST}})**
   - Security audits: ${{AUDIT_COST}}
   - Vulnerability assessments: ${{VULN_COST}}
   - Dependency updates: ${{DEP_COST}}

### Balance

**Current Balance:** ${{CURRENT_BALANCE}} USD
**Runway at Current Burn Rate:** {{RUNWAY_MONTHS}} months

---

## Development Progress

### Features Delivered

- [ ] Feature 1: {{DESCRIPTION}}
- [ ] Feature 2: {{DESCRIPTION}}
- [ ] Feature 3: {{DESCRIPTION}}

**Total Features:** {{FEATURE_COUNT}}  
**Total Issues Closed:** {{ISSUES_CLOSED}}  
**Total PRs Merged:** {{PRS_MERGED}}

### Code Metrics

- **Commits:** {{COMMITS}}
- **Lines Added:** +{{LINES_ADDED}}
- **Lines Removed:** -{{LINES_REMOVED}}
- **Files Changed:** {{FILES_CHANGED}}
- **Contributors:** {{CONTRIBUTORS}}

### Key Improvements

1. **{{IMPROVEMENT_1_TITLE}}**
   - Description: {{DESCRIPTION}}
   - Impact: {{IMPACT}}

2. **{{IMPROVEMENT_2_TITLE}}**
   - Description: {{DESCRIPTION}}
   - Impact: {{IMPACT}}

---

## Security Updates

### Vulnerabilities Addressed

| ID | Severity | Description | Resolution |
|----|----------|-------------|------------|
| {{VULN_ID}} | {{SEVERITY}} | {{DESCRIPTION}} | {{RESOLUTION}} |

**Total Vulnerabilities Fixed:** {{VULN_FIXED}}

### Security Audits

- **Internal Reviews:** {{INTERNAL_AUDITS}} completed
- **External Audits:** {{EXTERNAL_AUDITS}} scheduled/completed
- **Dependencies Updated:** {{DEP_UPDATES}}

---

## IPFS Content Updates

### Content Statistics

- **Total Content Size:** {{CONTENT_SIZE}} GB
- **New Content Added:** {{NEW_CONTENT}} MB
- **Total CIDs Pinned:** {{CIDS_PINNED}}
- **Gateway Availability:** {{AVAILABILITY}}%

### New Content This Month

| Content | CID | Size | Description |
|---------|-----|------|-------------|
| {{CONTENT_NAME}} | {{CID}} | {{SIZE}} | {{DESCRIPTION}} |

**Verification:**
All CIDs can be verified via:
- Pinata: https://gateway.pinata.cloud/ipfs/{{CID}}
- IPFS.io: https://ipfs.io/ipfs/{{CID}}

---

## Community Engagement

### Contributor Statistics

- **Active Contributors:** {{CONTRIBUTORS}}
- **New Contributors:** {{NEW_CONTRIBUTORS}}
- **GitHub Stars:** {{STARS}} ({{STARS_CHANGE}} this month)
- **Forks:** {{FORKS}}
- **Watchers:** {{WATCHERS}}

### Community Activity

- **GitHub Discussions:** {{DISCUSSIONS}} active
- **Issues Opened:** {{ISSUES_OPENED}}
- **Issues Closed:** {{ISSUES_CLOSED}}
- **Pull Requests:** {{PRS_OPENED}} opened, {{PRS_MERGED}} merged

### Notable Contributions

1. **{{CONTRIBUTOR_1}}** - {{CONTRIBUTION}}
2. **{{CONTRIBUTOR_2}}** - {{CONTRIBUTION}}
3. **{{CONTRIBUTOR_3}}** - {{CONTRIBUTION}}

**Thank you to all contributors!**

---

## Collapse Risk Assessment

### Risk Factors

| Factor | Weight | Score | Weighted Risk |
|--------|--------|-------|---------------|
| Single Point of Failure | 30% | {{SPOF_SCORE}}/10 | {{SPOF_RISK}}% |
| Financial Sustainability | 25% | {{FIN_SCORE}}/10 | {{FIN_RISK}}% |
| Security Vulnerabilities | 20% | {{SEC_SCORE}}/10 | {{SEC_RISK}}% |
| Knowledge Loss | 15% | {{KNOW_SCORE}}/10 | {{KNOW_RISK}}% |
| Community Fragmentation | 10% | {{COMM_SCORE}}/10 | {{COMM_RISK}}% |

**Overall Collapse Risk:** {{COLLAPSE_RISK}}%

**Trend:** {{RISK_TREND}} from last month ({{LAST_MONTH_RISK}}%)

### Risk Mitigation Actions

1. **{{MITIGATION_1}}**
   - Status: {{STATUS}}
   - Impact: Reduces risk by {{IMPACT}}%

2. **{{MITIGATION_2}}**
   - Status: {{STATUS}}
   - Impact: Reduces risk by {{IMPACT}}%

---

## Goals & Priorities

### Next Month Objectives

1. **{{OBJECTIVE_1}}**
   - Target: {{TARGET}}
   - Priority: {{PRIORITY}}

2. **{{OBJECTIVE_2}}**
   - Target: {{TARGET}}
   - Priority: {{PRIORITY}}

3. **{{OBJECTIVE_3}}**
   - Target: {{TARGET}}
   - Priority: {{PRIORITY}}

### Quarter Roadmap

**Q{{QUARTER}} {{YEAR}} Goals:**
- [ ] Goal 1: {{DESCRIPTION}}
- [ ] Goal 2: {{DESCRIPTION}}
- [ ] Goal 3: {{DESCRIPTION}}

---

## Acknowledgments

### Top Contributors This Month

**Financial Supporters:**
- [Listed with permission] - {{AMOUNT}}
- [Anonymous] - {{AMOUNT}}

**Code Contributors:**
- {{CONTRIBUTOR_1}} - {{CONTRIBUTIONS}}
- {{CONTRIBUTOR_2}} - {{CONTRIBUTIONS}}

**Community Support:**
- Special thanks to everyone who starred, shared, or provided feedback

---

## Verification

### On-Chain Verification

**Ethereum Address:**
```
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2
```
Verify: https://etherscan.io/address/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2

**Bitcoin Address:**
```
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```
Verify: https://blockchain.com/btc/address/bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

### IPFS Verification

**This Report CID:** {{REPORT_CID}}  
**Previous Report CID:** {{PREV_REPORT_CID}}  
**Access:** https://gateway.pinata.cloud/ipfs/{{REPORT_CID}}

### Git Verification

**Commit Hash:** {{COMMIT_HASH}}  
**Signed:** {{SIGNED}} (GPG)  
**Verify:** `git show {{COMMIT_HASH}}`

---

## Contact & Feedback

**Questions about this report?**
- GitHub Discussions: https://github.com/hannesmitterer/Euystacio/discussions
- Email: transparency@euystacio.io

**Report Issues:**
- GitHub Issues: https://github.com/hannesmitterer/Euystacio/issues

**Support Framework Euystacio:**
- Full details: https://github.com/hannesmitterer/Euystacio/blob/main/SUPPORT.md

---

**Report Prepared By:** Framework Euystacio Transparency Team  
**Next Report:** {{NEXT_MONTH}}-{{NEXT_YEAR}}  
**Frequency:** Monthly, published on the 1st of each month

---

## Appendix

### Funding Allocation Policy

As documented in SUPPORT.md:
- 40% Development
- 25% Infrastructure
- 15% Security
- 10% Community
- 10% Emergency Reserve

### Changelog from Last Month

- {{CHANGE_1}}
- {{CHANGE_2}}
- {{CHANGE_3}}

---

*This report is published to IPFS for permanent archival and transparency.*
*All financial data is verifiable on-chain.*
*All code metrics are verifiable via GitHub.*

**Together, we build systems that outlast us.**
EOF

    # Replace placeholders with actual values
    local month_name=$(date -d "${YEAR}-${MONTH}-01" +%B 2>/dev/null || echo "{{MONTH_NAME}}")
    local last_day=$(date -d "${YEAR}-${MONTH}-01 +1 month -1 day" +%d 2>/dev/null || echo "{{LAST_DAY}}")
    local generation_date=$(date +%Y-%m-%d)
    
    sed -i "s/{{MONTH_NAME}}/$month_name/g" "$file"
    sed -i "s/{{YEAR}}/$YEAR/g" "$file"
    sed -i "s/{{MONTH}}/$MONTH/g" "$file"
    sed -i "s/{{LAST_DAY}}/$last_day/g" "$file"
    sed -i "s/{{GENERATION_DATE}}/$generation_date/g" "$file"
    
    echo -e "${GREEN}✓${NC} Report template created: $file"
}

# Main execution
echo "Generating transparency report template..."
generate_report_template "$REPORT_FILE"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit $REPORT_FILE with actual data"
echo "2. Fill in all {{PLACEHOLDER}} values"
echo "3. Review and verify all numbers"
echo "4. Commit to Git: git add $REPORT_FILE"
echo "5. Pin to IPFS using: ./scripts/eternalize.sh"
echo "6. Publish CID in README and social media"
echo ""
echo -e "${GREEN}Template generation complete!${NC}"
