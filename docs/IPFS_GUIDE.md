# IPFS Eternalization Guide

This guide explains how to eternalize your Euystacio documentation using IPFS and Pinata.

## What is IPFS?

The InterPlanetary File System (IPFS) is a protocol and peer-to-peer network for storing and sharing data in a distributed file system. It uses content-addressing to uniquely identify each file in a global namespace.

## What is Pinata?

Pinata is a pinning service for IPFS that ensures your content remains available on the IPFS network by storing it on multiple nodes.

## Using the Eternalization Script

The `eternalize.sh` script automates the entire process:

### Prerequisites

1. Export your Pinata JWT token:
   ```bash
   export PINATA_JWT="your_pinata_jwt_token"
   ```

2. Ensure your documentation is in the `docs/` directory

### Running the Script

```bash
./eternalize.sh
```

The script will:
1. Install IPFS CLI if not present
2. Initialize the IPFS repository
3. Start the IPFS daemon
4. Add your documentation to IPFS
5. Pin the content to Pinata
6. Display the CID and gateway URLs

### Output

After successful execution, you'll receive:
- A Content Identifier (CID) for your documentation
- IPFS gateway URL: `https://ipfs.io/ipfs/<CID>`
- Pinata gateway URL: `https://gateway.pinata.cloud/ipfs/<CID>`

## Benefits

- **Permanent**: Content is addressed by its hash, making it immutable
- **Decentralized**: No single point of failure
- **Censorship-resistant**: Content cannot be removed by any single entity
- **Verifiable**: Content integrity is guaranteed by cryptographic hashing

## Next Steps

After eternalization:
1. Share the CID with your community
2. Add the gateway URLs to your README
3. Consider setting up automatic pinning for updates

---

For more information about IPFS, visit [ipfs.tech](https://ipfs.tech)
