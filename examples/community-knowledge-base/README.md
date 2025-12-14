# Community Knowledge Base
## Decentralized Wiki for Local Knowledge Preservation

**A Seedbringer Example Project**

A collaborative, peer-to-peer knowledge base for preserving local traditions, skills, and wisdom using decentralized technology.

---

## Overview

This project enables communities to document and share knowledge without relying on centralized platforms that may disappear, be censored, or become inaccessible.

### Features

✅ **Collaborative Editing**: Multiple people can contribute simultaneously  
✅ **Offline-First**: Works without constant internet connection  
✅ **Peer-to-Peer Sync**: Data syncs directly between community members  
✅ **Version History**: Track all changes with full history  
✅ **Multilingual**: Built-in translation support  
✅ **Mobile-Friendly**: Document knowledge from anywhere  
✅ **No Central Server**: Fully decentralized using OrbitDB + IPFS

---

## Use Cases

- **Indigenous Communities**: Preserve traditional knowledge and oral histories
- **Agricultural Communities**: Document local farming techniques and seed varieties
- **Artisan Groups**: Share craft techniques and patterns
- **Local History**: Collaborative community archives
- **Emergency Preparedness**: Distributed information that survives disasters
- **Educational Institutions**: Student-maintained knowledge bases

---

## Quick Start

### Prerequisites

- Node.js 18+
- IPFS node running locally or remotely
- Modern web browser

### Installation

```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/examples/community-knowledge-base

# Install dependencies
npm install

# Start IPFS (if not already running)
ipfs daemon &

# Start the application
npm start
```

Visit `http://localhost:3000`

---

## Architecture

```
┌──────────────────────────────────────────┐
│      Web Interface (Browser)             │
│  - Article editor (Markdown)             │
│  - Search and navigation                 │
│  - User management                       │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│         OrbitDB (Database)               │
│  - Documents store                       │
│  - Access control                        │
│  - Conflict resolution                   │
└────────────────┬─────────────────────────┘
                 │
┌────────────────▼─────────────────────────┐
│            IPFS Layer                    │
│  - Content storage                       │
│  - Peer-to-peer sync                     │
│  - Content addressing                    │
└──────────────────────────────────────────┘
```

---

## Data Model

### Article

```javascript
{
  id: "traditional-corn-varieties",
  title: "Traditional Corn Varieties of Our Region",
  content: "# Traditional Corn Varieties\n\n...",
  language: "en",
  category: "agriculture",
  tags: ["corn", "seeds", "farming"],
  author: "QmUserIdentity...",
  created: "2025-12-14T10:00:00Z",
  lastModified: "2025-12-14T15:30:00Z",
  version: 3,
  translations: {
    "es": "QmTranslationCID...",
    "fr": "QmTranslationCID..."
  },
  media: ["QmImageCID1...", "QmImageCID2..."],
  contributors: ["QmUser1...", "QmUser2..."]
}
```

### Revision History

```javascript
{
  articleId: "traditional-corn-varieties",
  version: 3,
  timestamp: "2025-12-14T15:30:00Z",
  author: "QmUser2...",
  changes: {
    type: "edit",
    diff: "... diff content ...",
    summary: "Added section on Blue Corn cultivation"
  },
  previousVersion: 2,
  ipfsCID: "QmRevisionCID..."
}
```

---

## Implementation

### Setting Up OrbitDB

```javascript
// db-setup.js
import IPFS from 'ipfs';
import OrbitDB from 'orbit-db';

async function setupDatabase() {
  // Initialize IPFS
  const ipfs = await IPFS.create({
    repo: './ipfs',
    EXPERIMENTAL: {
      pubsub: true
    }
  });

  // Initialize OrbitDB
  const orbitdb = await OrbitDB.createInstance(ipfs);

  // Create or open database
  const db = await orbitdb.docs('community-knowledge', {
    accessController: {
      type: 'orbitdb',
      write: ['*']  // Anyone can write (customize for your needs)
    },
    indexBy: 'id',
  });

  console.log('Database address:', db.address.toString());
  // Save this address to share with community members

  return { ipfs, orbitdb, db };
}

export default setupDatabase;
```

### Creating Articles

```javascript
// article-manager.js
class ArticleManager {
  constructor(db) {
    this.db = db;
  }

  async createArticle(article) {
    // Generate ID from title
    article.id = this.slugify(article.title);
    article.created = new Date().toISOString();
    article.lastModified = article.created;
    article.version = 1;

    // Store in OrbitDB
    const hash = await this.db.put(article);
    
    console.log('Article created:', article.id);
    return article;
  }

  async updateArticle(id, updates) {
    // Get current version
    const current = this.db.get(id)[0];
    
    // Create new version
    const updated = {
      ...current,
      ...updates,
      lastModified: new Date().toISOString(),
      version: current.version + 1
    };

    // Save revision history
    await this.saveRevision(current, updated);

    // Update database
    await this.db.put(updated);
    
    return updated;
  }

  async searchArticles(query) {
    // Full-text search
    const results = this.db.query(article => {
      const searchText = `${article.title} ${article.content} ${article.tags.join(' ')}`;
      return searchText.toLowerCase().includes(query.toLowerCase());
    });

    return results;
  }

  async getArticlesByCategory(category) {
    return this.db.query(article => article.category === category);
  }

  slugify(title) {
    return title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  }

  async saveRevision(oldVersion, newVersion) {
    // Store in separate revisions database
    const revision = {
      articleId: oldVersion.id,
      version: newVersion.version,
      timestamp: newVersion.lastModified,
      author: newVersion.author,
      changes: this.createDiff(oldVersion.content, newVersion.content)
    };

    // This would go to a revisions OrbitDB
    // await this.revisionsDb.put(revision);
  }

  createDiff(oldContent, newContent) {
    // Simple diff (in production, use a library like diff-match-patch)
    return {
      type: 'edit',
      summary: 'Content updated'
    };
  }
}

export default ArticleManager;
```

### Web Interface

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Community Knowledge Base</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
      display: grid;
      grid-template-columns: 250px 1fr;
      height: 100vh;
    }
    .sidebar {
      background: #f5f5f5;
      padding: 20px;
      overflow-y: auto;
      border-right: 1px solid #ddd;
    }
    .main {
      padding: 20px;
      overflow-y: auto;
    }
    .search-box {
      width: 100%;
      padding: 10px;
      margin-bottom: 20px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    .article-list {
      list-style: none;
      padding: 0;
    }
    .article-link {
      display: block;
      padding: 10px;
      margin-bottom: 5px;
      background: white;
      border-radius: 4px;
      text-decoration: none;
      color: #333;
      cursor: pointer;
    }
    .article-link:hover {
      background: #e3f2fd;
    }
    .editor {
      border: 1px solid #ddd;
      padding: 20px;
      min-height: 400px;
      border-radius: 4px;
    }
    button {
      background: #2563eb;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 4px;
      cursor: pointer;
      margin-right: 10px;
    }
    button:hover {
      background: #1d4ed8;
    }
    .metadata {
      color: #666;
      font-size: 0.9em;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="sidebar">
    <h2>📚 Knowledge Base</h2>
    <input 
      type="search" 
      class="search-box" 
      placeholder="Search articles..."
      id="search-input"
    >
    
    <h3>Categories</h3>
    <ul class="article-list" id="categories">
      <li><a class="article-link" data-category="all">All Articles</a></li>
      <li><a class="article-link" data-category="agriculture">🌾 Agriculture</a></li>
      <li><a class="article-link" data-category="crafts">🎨 Crafts</a></li>
      <li><a class="article-link" data-category="history">📜 History</a></li>
      <li><a class="article-link" data-category="recipes">🍳 Recipes</a></li>
      <li><a class="article-link" data-category="medicine">🌿 Medicine</a></li>
    </ul>

    <h3>Recent Articles</h3>
    <ul class="article-list" id="recent-articles"></ul>
    
    <button onclick="createNewArticle()">+ New Article</button>
  </div>

  <div class="main">
    <div id="article-view">
      <h1 id="article-title">Welcome to Community Knowledge Base</h1>
      <div class="metadata" id="article-metadata"></div>
      <div id="article-content">
        <p>Select an article from the sidebar or create a new one to get started.</p>
        <p>This knowledge base is stored on IPFS and syncs peer-to-peer with your community.</p>
      </div>
      <button onclick="editArticle()">Edit</button>
    </div>

    <div id="article-edit" style="display: none;">
      <input 
        type="text" 
        id="edit-title" 
        placeholder="Article Title"
        style="width: 100%; padding: 10px; margin-bottom: 10px; font-size: 1.5em;"
      >
      <select id="edit-category" style="padding: 10px; margin-bottom: 10px;">
        <option value="agriculture">Agriculture</option>
        <option value="crafts">Crafts</option>
        <option value="history">History</option>
        <option value="recipes">Recipes</option>
        <option value="medicine">Medicine</option>
      </select>
      <textarea 
        id="edit-content" 
        class="editor" 
        placeholder="Write your article in Markdown..."
      ></textarea>
      <input 
        type="text" 
        id="edit-tags" 
        placeholder="Tags (comma-separated)"
        style="width: 100%; padding: 10px; margin-top: 10px;"
      >
      <div style="margin-top: 20px;">
        <button onclick="saveArticle()">💾 Save</button>
        <button onclick="cancelEdit()" style="background: #666;">Cancel</button>
      </div>
    </div>
  </div>

  <script type="module">
    import setupDatabase from './db-setup.js';
    import ArticleManager from './article-manager.js';
    import { marked } from 'https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js';

    let db, articleManager, currentArticle;

    // Initialize
    async function init() {
      const { db: database } = await setupDatabase();
      db = database;
      articleManager = new ArticleManager(db);

      // Load recent articles
      loadRecentArticles();

      // Set up event listeners
      document.getElementById('search-input').addEventListener('input', handleSearch);
      
      // Set up category filters
      document.querySelectorAll('[data-category]').forEach(link => {
        link.addEventListener('click', (e) => {
          const category = e.target.dataset.category;
          if (category === 'all') {
            loadRecentArticles();
          } else {
            loadArticlesByCategory(category);
          }
        });
      });

      // Listen for database updates
      db.events.on('replicated', () => {
        console.log('Database synced with peers');
        loadRecentArticles();
      });
    }

    async function loadRecentArticles() {
      const articles = db.query(() => true)
        .sort((a, b) => new Date(b.lastModified) - new Date(a.lastModified))
        .slice(0, 10);

      const list = document.getElementById('recent-articles');
      list.innerHTML = articles.map(article => `
        <li>
          <a class="article-link" onclick="viewArticle('${article.id}')">
            ${article.title}
          </a>
        </li>
      `).join('');
    }

    async function loadArticlesByCategory(category) {
      const articles = await articleManager.getArticlesByCategory(category);
      // Display filtered articles...
    }

    function handleSearch(e) {
      const query = e.target.value;
      if (query.length > 2) {
        articleManager.searchArticles(query).then(results => {
          // Display search results...
        });
      }
    }

    window.viewArticle = function(id) {
      const article = db.get(id)[0];
      if (!article) return;

      currentArticle = article;

      document.getElementById('article-title').textContent = article.title;
      document.getElementById('article-metadata').innerHTML = `
        Category: ${article.category} | 
        Last updated: ${new Date(article.lastModified).toLocaleDateString()} |
        Version: ${article.version}
      `;
      document.getElementById('article-content').innerHTML = marked.parse(article.content);
      
      document.getElementById('article-view').style.display = 'block';
      document.getElementById('article-edit').style.display = 'none';
    };

    window.editArticle = function() {
      if (!currentArticle) return;

      document.getElementById('edit-title').value = currentArticle.title;
      document.getElementById('edit-category').value = currentArticle.category;
      document.getElementById('edit-content').value = currentArticle.content;
      document.getElementById('edit-tags').value = currentArticle.tags.join(', ');

      document.getElementById('article-view').style.display = 'none';
      document.getElementById('article-edit').style.display = 'block';
    };

    window.createNewArticle = function() {
      currentArticle = null;
      document.getElementById('edit-title').value = '';
      document.getElementById('edit-content').value = '';
      document.getElementById('edit-tags').value = '';

      document.getElementById('article-view').style.display = 'none';
      document.getElementById('article-edit').style.display = 'block';
    };

    window.saveArticle = async function() {
      const title = document.getElementById('edit-title').value;
      const category = document.getElementById('edit-category').value;
      const content = document.getElementById('edit-content').value;
      const tags = document.getElementById('edit-tags').value.split(',').map(t => t.trim());

      const articleData = { title, category, content, tags, author: 'QmCurrentUser...' };

      if (currentArticle) {
        await articleManager.updateArticle(currentArticle.id, articleData);
      } else {
        currentArticle = await articleManager.createArticle(articleData);
      }

      viewArticle(currentArticle.id);
      loadRecentArticles();
    };

    window.cancelEdit = function() {
      if (currentArticle) {
        viewArticle(currentArticle.id);
      } else {
        document.getElementById('article-view').style.display = 'block';
        document.getElementById('article-edit').style.display = 'none';
      }
    };

    // Start the application
    init();
  </script>
</body>
</html>
```

---

## Deployment

### Local Community Network

Perfect for communities with local internet but unreliable external connectivity:

```bash
# Each community member runs a node
npm install
npm start

# Share the database address
# Others can replicate using: orbitdb.open('ADDRESS')
```

### Hybrid Cloud + Local

Host a "seed" node in the cloud for reliability:

```bash
# Deploy to cloud provider (Render, Fly.io, etc.)
# Local nodes sync with cloud node when online
# Works offline, syncs when connected
```

---

## Customization

### Access Control

```javascript
// Restricted write access
const db = await orbitdb.docs('community-knowledge', {
  accessController: {
    type: 'orbitdb',
    write: [
      'QmTrustedUser1...',
      'QmTrustedUser2...',
      'QmTrustedUser3...'
    ]
  }
});
```

### Multi-Database Setup

```javascript
// Separate databases for different purposes
const publicDb = await orbitdb.docs('public-knowledge');
const memberOnlyDb = await orbitdb.docs('member-knowledge');
const archiveDb = await orbitdb.docs('historical-archive');
```

---

## Troubleshooting

**Articles not syncing between peers**
- Ensure IPFS pubsub is enabled
- Check peers are connected: `ipfs swarm peers`
- Verify database address is shared correctly

**Database loading slowly**
- OrbitDB loads entire history; this is normal
- Consider periodic "snapshots" to reduce load time

---

## License

MIT License

---

*"Knowledge is not owned. It is shared, grown, and passed forward."*

—The Seedbringer Collective
