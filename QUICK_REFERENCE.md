# Seedbringer Quick Reference
## Essential Links & Commands

**🚀 New to Seedbringer? Start here: [SEEDBRINGER_INDEX.md](./SEEDBRINGER_INDEX.md)**

---

## Core Documents (Read in Order)

1. **[Seedbringer Manifesto](./SEEDBRINGER_MANIFESTO.md)** - Philosophy & vision (5 min read)
2. **[Getting Started Guide](./GETTING_STARTED.md)** - Practical introduction (15 min read)
3. **[Technical Blueprint](./TECHNICAL_BLUEPRINT.md)** - Implementation details (30 min read)

---

## Example Projects

| Project | Description | Difficulty |
|---------|-------------|-----------|
| [Renewable Energy Tracker](./examples/renewable-energy-tracker/) | Monitor solar panels with IPFS/blockchain | Beginner-Intermediate |
| [Community Knowledge Base](./examples/community-knowledge-base/) | Decentralized wiki with OrbitDB | Intermediate |
| [Ecological Monitoring](./examples/ecological-monitoring/) | Environmental data tracking | Intermediate-Advanced |

---

## Quick Commands

### Install IPFS
```bash
# Linux/Mac
wget https://dist.ipfs.io/kubo/v0.24.0/kubo_v0.24.0_linux-amd64.tar.gz
tar -xvzf kubo_v0.24.0_linux-amd64.tar.gz
cd kubo && sudo bash install.sh
ipfs init
ipfs daemon
```

### Upload to IPFS
```bash
# Add a file
ipfs add myfile.txt

# Add a directory
ipfs add -r myproject/

# Pin content
ipfs pin add QmHash...
```

### Deploy an Example
```bash
# Clone repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/examples/renewable-energy-tracker

# Install and run
npm install
npm start
```

---

## Core Principles

🔍 **Transparency** - Open by default, verifiable by all  
🤝 **Collaboration** - Global participation, collective intelligence  
⚖️ **Equity** - Universal access, no gatekeepers  
🏛️ **Permanence** - Decentralized preservation for future generations

---

## Key Technologies

- **IPFS**: Content-addressed storage (permanent files)
- **Blockchain**: Immutable timestamps (proof of existence)
- **OrbitDB**: Distributed database (collaborative data)
- **libp2p**: Peer-to-peer networking (no servers)

---

## Community

- **GitHub**: https://github.com/hannesmitterer/Euystacio
- **Email**: community@seedbringer.org
- **Issues**: https://github.com/hannesmitterer/Euystacio/issues
- **Discussions**: https://github.com/hannesmitterer/Euystacio/discussions

---

## License

Dual licensed: [MIT](./LICENSE) + [Sacred Commons](./SACRED_COMMONS_LICENSE.md)

**"All is Open Source"** - Free forever, for everyone.

---

## Common Tasks

### I want to...

**...understand the philosophy**  
→ Read [Seedbringer Manifesto](./SEEDBRINGER_MANIFESTO.md)

**...try a working example**  
→ See [examples/](./examples/)

**...build something**  
→ Follow [Technical Blueprint](./TECHNICAL_BLUEPRINT.md)

**...contribute**  
→ Check [Issues](https://github.com/hannesmitterer/Euystacio/issues) or improve documentation

**...translate to my language**  
→ Email translations@seedbringer.org

**...teach others**  
→ Use [Getting Started Guide](./GETTING_STARTED.md) workshop template

---

## Resources

- **IPFS Docs**: https://docs.ipfs.io
- **Ethereum Docs**: https://ethereum.org/developers
- **OrbitDB**: https://orbitdb.org
- **Web3.Storage**: https://web3.storage (free IPFS hosting)

---

## Philosophy in One Line

*"We do not own the seeds. We are their carriers."*

All is Open Source. All is Accessible. All is Permanent.

—The Seedbringer Collective
