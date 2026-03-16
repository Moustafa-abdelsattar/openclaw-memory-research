# 🦞 Research and Exploration on OpenClaw (Lobster) Memory

**Author:** Research Team  
**Date:** March 16, 2026  
**Version:** 1.0  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What is "Memory" in OpenClaw?](#2-what-is-memory-in-openclaw)
3. [Memory Architecture Overview](#3-memory-architecture-overview)
4. [The Two Memory Layers](#4-the-two-memory-layers)
5. [Memory Tools (Agent-Facing)](#5-memory-tools-agent-facing)
6. [Vector Memory Search](#6-vector-memory-search)
7. [Hybrid Search (BM25 + Vector)](#7-hybrid-search-bm25--vector)
8. [Post-Processing Pipeline](#8-post-processing-pipeline)
9. [Automatic Memory Flush (Pre-Compaction)](#9-automatic-memory-flush-pre-compaction)
10. [Context Window & Compaction](#10-context-window--compaction)
11. [Session Pruning](#11-session-pruning)
12. [Session Management & Persistence](#12-session-management--persistence)
13. [Advanced Memory Features](#13-advanced-memory-features)
14. [QMD Backend (Experimental)](#14-qmd-backend-experimental)
15. [Configuration Reference](#15-configuration-reference)
16. [Best Practices & Recommendations](#16-best-practices--recommendations)
17. [Glossary](#17-glossary)

---

## 1. Executive Summary

OpenClaw's memory system is what transforms a stateless AI model into a **persistent, context-aware personal assistant**. Unlike a simple chatbot that forgets everything after each session, OpenClaw uses a layered approach combining:

- **Plain Markdown files** as the source of truth for long-term memory
- **Session transcripts** (JSONL) for conversation continuity
- **Vector embeddings** for semantic search across memories
- **Hybrid retrieval** (BM25 + vector) for both exact and fuzzy matching
- **Automatic memory flush** to protect critical context before compaction
- **Compaction** to summarize old conversations and stay within model context limits
- **Session pruning** to trim tool output bloat without rewriting history

The key insight: **the model only "remembers" what gets written to disk**. Memory files *are* the memory. The AI wakes up fresh each session and relies entirely on these files to maintain continuity.

---

## 2. What is "Memory" in OpenClaw?

Memory in OpenClaw is **NOT** what you might think. It is not:

- ❌ A hidden database the AI magically accesses
- ❌ RAM or state that persists between API calls
- ❌ Training data or fine-tuning

It **IS**:

- ✅ **Plain Markdown files** on disk in the agent workspace
- ✅ **Session transcripts** (JSONL) that record conversation history
- ✅ **Vector indexes** that enable semantic search over those files
- ✅ A combination of **retrieval and injection** into the model's context window

### The Fundamental Constraint

Every AI model has a **context window** — a maximum number of tokens it can "see" at once. For example, Claude's context window is 200K tokens. Everything the model needs to know must fit in this window. Memory is the system that decides **what goes in** and **what stays on disk for later retrieval**.

---

## 3. Memory Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MODEL CONTEXT WINDOW                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ System Prompt │  │ Workspace    │  │  Conversation     │  │
│  │ (rules, tools,│  │ Files        │  │  History          │  │
│  │  skills list) │  │ (AGENTS.md,  │  │  (recent messages │  │
│  │               │  │  SOUL.md,    │  │   + compaction    │  │
│  │               │  │  USER.md...) │  │   summaries)      │  │
│  └──────────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
    Built by OpenClaw    Injected at         Managed by
    each run             session start       session system
                              │
                    ┌─────────┴─────────┐
                    │   DISK STORAGE     │
                    │                    │
                    │  MEMORY.md         │  ← Curated long-term memory
                    │  memory/YYYY-MM-DD │  ← Daily logs
                    │  sessions/*.jsonl  │  ← Conversation transcripts
                    │  sessions.json     │  ← Session metadata
                    │  *.sqlite          │  ← Vector index
                    └────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │  RETRIEVAL LAYER   │
                    │                    │
                    │  memory_search     │  ← Semantic vector search
                    │  memory_get        │  ← Direct file read
                    │  Hybrid (BM25+Vec) │  ← Keyword + semantic
                    └────────────────────┘
```

---

## 4. The Two Memory Layers

OpenClaw uses a **two-layer memory model**, much like how humans have short-term and long-term memory.

### 4.1 Daily Logs — `memory/YYYY-MM-DD.md`

**Purpose:** Raw, day-to-day notes and running context.

**Characteristics:**
- One file per day (e.g., `memory/2026-03-16.md`)
- Append-only (new entries added at the bottom)
- Read at session start: today + yesterday's files are loaded
- Contains: decisions made, tasks completed, things learned, conversations had
- Think of it as a **daily journal**

**Example:**
```markdown
# 2026-03-16

## Morning
- User asked about OpenClaw memory system
- Created comprehensive research document

## Afternoon  
- Pushed research to GitHub
- Boss confirmed receipt of memory research
```

### 4.2 Long-Term Memory — `MEMORY.md`

**Purpose:** Curated, distilled long-term knowledge.

**Characteristics:**
- Single file at workspace root
- **Optional** (not auto-created)
- Only loaded in **main, private sessions** (never in group chats — security measure)
- Contains: user preferences, important decisions, recurring patterns, lessons learned
- Think of it as a **personal knowledge base**

**Example:**
```markdown
# Long-Term Memory

## User Preferences
- Prefers concise answers
- Timezone: Africa/Cairo (GMT+2)
- Working hours: 9am-6pm

## Important Decisions
- 2026-03-01: Migrated to OpenClaw v2.x
- 2026-03-10: Set up Discord integration

## Lessons Learned
- Always confirm before sending external messages
- Daily memory files should be reviewed weekly
```

### 4.3 When to Write What Where

| Content Type | Where | Example |
|---|---|---|
| Today's events | `memory/YYYY-MM-DD.md` | "Had meeting about X" |
| User preferences | `MEMORY.md` | "Prefers dark mode" |
| Temporary tasks | `memory/YYYY-MM-DD.md` | "TODO: follow up on email" |
| Durable facts | `MEMORY.md` | "User's GitHub: @username" |
| Conversation notes | `memory/YYYY-MM-DD.md` | "Discussed Y with Z" |
| Recurring patterns | `MEMORY.md` | "Weekly standup at 10am" |

---

## 5. Memory Tools (Agent-Facing)

OpenClaw provides two tools that the AI agent uses to interact with memory:

### 5.1 `memory_search` — Semantic Recall

**What it does:** Searches across all memory files using vector similarity (and optionally keyword matching).

**How it works:**
1. Memory files are chunked into ~400-token segments with 80-token overlap
2. Each chunk is embedded into a vector using an embedding model
3. When a search query comes in, it's also embedded
4. The system finds the most similar chunks by cosine similarity
5. Returns: snippet text (~700 chars), file path, line range, relevance score

**What it returns:**
- Snippet text (capped at ~700 characters)
- Source file path and line range
- Relevance score
- Provider/model used for embedding
- Whether a fallback was used

**When the agent uses it:** Before answering anything about prior work, decisions, dates, people, preferences, or todos. This is a **mandatory recall step** — the agent must search before claiming to know (or not know) something.

### 5.2 `memory_get` — Targeted Read

**What it does:** Reads a specific memory file (or portion of it) directly.

**How it works:**
- Takes a file path (relative to workspace), optional start line, optional line count
- Returns the raw file content
- Only works on `MEMORY.md` and files under `memory/`
- Gracefully handles missing files (returns empty string instead of error)

**When the agent uses it:** After `memory_search` finds relevant snippets, the agent uses `memory_get` to pull the full context around those snippets.

### 5.3 Workflow: Search → Get → Answer

```
User asks: "What was the decision about the API migration?"

1. Agent calls memory_search("API migration decision")
2. Gets snippet: "...decided to use REST over GraphQL..." from memory/2026-03-10.md:15
3. Agent calls memory_get("memory/2026-03-10.md", from=12, lines=10)
4. Gets full context around the decision
5. Agent answers with source citation
```

---

## 6. Vector Memory Search

### 6.1 How Indexing Works

OpenClaw maintains a vector index for semantic search:

**Storage:** Per-agent SQLite database at `~/.openclaw/memory/<agentId>.sqlite`

**What gets indexed:**
- `MEMORY.md`
- All `memory/**/*.md` files
- Optionally: extra paths via `memorySearch.extraPaths`
- Optionally: session transcripts (experimental)

**Chunking strategy:**
- Target chunk size: ~400 tokens
- Overlap between chunks: ~80 tokens
- This ensures context isn't lost at chunk boundaries

**Freshness:**
- File watcher on `MEMORY.md` + `memory/` (debounced 1.5s)
- Re-sync on session start, on search, or on a configured interval
- Automatic reindex when embedding model/provider changes

### 6.2 Embedding Providers

OpenClaw supports multiple embedding providers (auto-selected in this priority):

| Priority | Provider | Model | Notes |
|---|---|---|---|
| 1 | Local | GGUF via node-llama-cpp | ~0.6 GB download, fully offline |
| 2 | OpenAI | text-embedding-3-small | Requires API key |
| 3 | Gemini | gemini-embedding-001 | Requires API key |
| 4 | Voyage | voyage-* | Requires API key |
| 5 | Mistral | mistral-* | Requires API key |
| 6 | Ollama | Local/self-hosted | No real API key needed |

**Local embedding** uses `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF` (~0.6 GB) by default and auto-downloads on first use.

**Fallback system:** If the primary provider fails, OpenClaw can fall back to a secondary provider. Configure via `memorySearch.fallback`.

### 6.3 Multimodal Memory (Gemini Embedding 2)

With `gemini-embedding-2-preview`, OpenClaw can index **images and audio** alongside Markdown:

- Supported images: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.heic`, `.heif`
- Supported audio: `.mp3`, `.wav`, `.ogg`, `.opus`, `.m4a`, `.aac`, `.flac`
- Search queries remain text, but can match against image/audio embeddings
- Only applies to files in `memorySearch.extraPaths` (not default memory roots)

### 6.4 SQLite Vector Acceleration (sqlite-vec)

When available, OpenClaw uses the `sqlite-vec` extension for hardware-accelerated vector operations:

- Stores embeddings in SQLite virtual tables (`vec0`)
- Performs distance queries in-database (fast)
- Falls back to JavaScript cosine similarity if sqlite-vec is unavailable
- Configurable via `memorySearch.store.vector.enabled`

### 6.5 Embedding Cache

OpenClaw caches chunk embeddings in SQLite to avoid re-embedding unchanged text:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        cache: {
          enabled: true,
          maxEntries: 50000
        }
      }
    }
  }
}
```

### 6.6 Batch Indexing (OpenAI + Gemini + Voyage)

For large corpus indexing, OpenClaw supports async batch embedding:

- Submits many embedding requests in a single batch job
- Processes asynchronously (cheaper and faster for bulk operations)
- Configurable concurrency, polling interval, and timeout
- OpenAI offers discounted pricing for Batch API workloads

---

## 7. Hybrid Search (BM25 + Vector)

### 7.1 The Problem

Vector search is great at understanding meaning:
- "Mac Studio gateway host" ≈ "the machine running the gateway" ✅

But weak at exact tokens:
- Searching for `a828e60` (a commit hash) — vector search may miss it ❌

BM25 (keyword search) is the opposite: strong at exact tokens, weak at paraphrases.

### 7.2 The Solution: Combine Both

OpenClaw's hybrid search merges results from both retrieval methods:

```
Query → Vector Search (semantic similarity)
      → BM25 Search (keyword relevance)
      → Weighted Merge → Final Results
```

**Merge formula:**
```
finalScore = vectorWeight × vectorScore + textWeight × textScore
```

Where `textScore = 1 / (1 + max(0, bm25Rank))`

**Default weights:** `vectorWeight: 0.7`, `textWeight: 0.3`

### 7.3 Configuration

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            candidateMultiplier: 4
          }
        }
      }
    }
  }
}
```

### 7.4 Fallback Behavior

- If embeddings are unavailable → BM25-only results
- If FTS5 can't be created → vector-only results
- Neither fails hard — the system degrades gracefully

---

## 8. Post-Processing Pipeline

After merging vector and keyword scores, two optional stages refine results:

```
Vector + Keyword → Weighted Merge → Temporal Decay → Sort → MMR → Top-K Results
```

### 8.1 MMR Re-Ranking (Diversity)

**Problem:** Multiple results may be near-duplicates (e.g., similar daily notes about the same topic).

**Solution:** Maximal Marginal Relevance (MMR) balances relevance with diversity.

**How it works:**
1. Results scored by original relevance
2. MMR iteratively selects results that maximize:
   ```
   λ × relevance − (1−λ) × max_similarity_to_selected
   ```
3. Similarity measured via Jaccard text similarity on tokenized content

**Lambda parameter:**
- `λ = 1.0` → pure relevance (no diversity)
- `λ = 0.0` → maximum diversity (ignores relevance)
- Default: `0.7` (balanced, slight relevance bias)

**Example:**

Without MMR:
```
1. memory/2026-02-10.md  (0.92) ← router + VLAN
2. memory/2026-02-08.md  (0.89) ← router + VLAN (near-duplicate!)
3. memory/network.md     (0.85) ← reference doc
```

With MMR (λ=0.7):
```
1. memory/2026-02-10.md  (0.92) ← router + VLAN
2. memory/network.md     (0.85) ← reference doc (diverse!)
3. memory/2026-02-05.md  (0.78) ← AdGuard DNS (diverse!)
```

### 8.2 Temporal Decay (Recency Boost)

**Problem:** A well-worded note from 6 months ago can outrank yesterday's update on the same topic.

**Solution:** Exponential decay multiplier based on age:

```
decayedScore = score × e^(-λ × ageInDays)
```

Where `λ = ln(2) / halfLifeDays`

**Default half-life: 30 days**

| Age | Score Retention |
|---|---|
| Today | 100% |
| 7 days | ~84% |
| 30 days | 50% |
| 90 days | 12.5% |
| 180 days | ~1.6% |

**Important:** Evergreen files are **never** decayed:
- `MEMORY.md` (root memory file)
- Non-dated files in `memory/` (e.g., `memory/projects.md`)

### 8.3 Combined Configuration

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            candidateMultiplier: 4,
            mmr: {
              enabled: true,
              lambda: 0.7
            },
            temporalDecay: {
              enabled: true,
              halfLifeDays: 30
            }
          }
        }
      }
    }
  }
}
```

---

## 9. Automatic Memory Flush (Pre-Compaction)

### 9.1 The Problem

When a conversation gets very long, OpenClaw must "compact" (summarize) older messages to stay within the model's context window. But if the model hasn't written important context to disk yet, that information could be **lost forever** during compaction.

### 9.2 The Solution

Before auto-compaction triggers, OpenClaw runs a **silent agentic turn** that reminds the model to write durable notes to disk:

```
Session nearing context limit
         │
         ▼
   Soft threshold crossed?  ──No──► Continue normally
         │
        Yes
         │
         ▼
   Run silent memory flush turn
   ("Write any lasting notes to memory/YYYY-MM-DD.md")
         │
         ▼
   Agent writes critical context to disk
   (Reply: NO_REPLY — user sees nothing)
         │
         ▼
   Auto-compaction proceeds safely
```

### 9.3 Configuration

```json5
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,                    // default: true
          softThresholdTokens: 4000,        // trigger before compaction
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

### 9.4 Key Details

- Runs **once per compaction cycle** (tracked in `sessions.json`)
- **Silent** — uses `NO_REPLY` so the user sees nothing
- **Skipped** when workspace is read-only
- Only runs for embedded sessions (not CLI backends)
- Soft threshold = `contextWindow - reserveTokensFloor - softThresholdTokens`

---

## 10. Context Window & Compaction

### 10.1 What is Compaction?

Compaction **summarizes older conversation** into a compact entry and keeps recent messages intact. It's like an AI taking notes on an earlier conversation so it can "remember" the gist without keeping every word.

### 10.2 Types of Compaction

| Type | Trigger | User Action |
|---|---|---|
| **Auto-compaction** | Session nears context window limit | Automatic |
| **Manual compaction** | User sends `/compact` | User-initiated |
| **Server-side** | OpenAI provider-side compaction | Automatic (OpenAI only) |

### 10.3 What Happens During Compaction

1. OpenClaw detects the session is nearing the context limit
2. (Optional) Memory flush runs first to save critical data
3. Older messages are summarized into a compact entry
4. The summary is **persisted** in the session's JSONL transcript
5. Future turns see: summary + recent messages

### 10.4 Compaction Settings

```json5
{
  agents: {
    defaults: {
      compaction: {
        enabled: true,
        reserveTokens: 16384,          // headroom for next turn
        keepRecentTokens: 20000,       // keep this many recent tokens intact
        reserveTokensFloor: 20000,     // safety floor
        model: "openrouter/anthropic/claude-sonnet-4-5",  // optional: use different model
        identifierPolicy: "strict"     // preserve IDs in summaries
      }
    }
  }
}
```

### 10.5 Compaction vs. Pruning vs. Memory

| Mechanism | Persists? | What it affects | When |
|---|---|---|---|
| **Compaction** | ✅ Yes (JSONL) | Conversation history | Near context limit |
| **Pruning** | ❌ No (in-memory only) | Old tool results | Every LLM call |
| **Memory files** | ✅ Yes (Markdown) | Durable facts & notes | Agent writes them |

---

## 11. Session Pruning

### 11.1 What It Is

Session pruning trims **old tool results** from the in-memory context before each LLM call. It does **NOT** rewrite the on-disk history.

### 11.2 Why It Matters

Tool results (like file reads, command outputs, web searches) accumulate rapidly and can bloat the context. Pruning keeps the active context lean without losing the actual conversation.

### 11.3 Two Levels of Pruning

**Soft-trim:** For oversized tool results
- Keeps head + tail of the output
- Inserts `...` in the middle
- Appends a note with the original size
- Skips results containing images

**Hard-clear:** For older tool results
- Replaces the entire result with a placeholder: `"[Old tool result content cleared]"`

### 11.4 Cache-TTL Mode

Pruning is optimized for Anthropic's prompt caching:
- Only runs when the last API call is older than the TTL (default 5 minutes)
- After pruning, the TTL resets
- Reduces cache-write costs for the first request after idle periods

### 11.5 Defaults

```json5
{
  ttl: "5m",
  keepLastAssistants: 3,          // protect recent tool results
  softTrimRatio: 0.3,
  hardClearRatio: 0.5,
  minPrunableToolChars: 50000,
  softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
  hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" }
}
```

---

## 12. Session Management & Persistence

### 12.1 Two Persistence Layers

**1. Session Store (`sessions.json`)**
- Key/value map: `sessionKey → SessionEntry`
- Small, mutable file
- Tracks metadata: current session ID, token counts, toggles, compaction count

**2. Transcripts (`<sessionId>.jsonl`)**
- Append-only conversation log
- Tree structure (entries have `id` + `parentId`)
- Contains: messages, tool calls, compaction summaries

### 12.2 Session Keys

Sessions are identified by keys that encode the routing:

| Pattern | Example | When |
|---|---|---|
| Main DM | `agent:main:main` | Direct chat (default) |
| Per-peer DM | `agent:main:direct:<peerId>` | `dmScope: "per-peer"` |
| Group chat | `agent:main:discord:group:<id>` | Group messages |
| Cron job | `cron:<jobId>` | Scheduled tasks |
| Webhook | `hook:<uuid>` | Incoming webhooks |

### 12.3 Session Lifecycle

- **Daily reset:** New session at 4:00 AM local time (configurable)
- **Idle reset:** New session after `idleMinutes` of inactivity (optional)
- **Manual reset:** `/new` or `/reset` commands
- **When both:** Whichever expires first wins

### 12.4 Session Maintenance

```json5
{
  session: {
    maintenance: {
      mode: "enforce",        // "warn" or "enforce"
      pruneAfter: "30d",      // remove sessions older than this
      maxEntries: 500,        // cap total session entries
      rotateBytes: "10mb",    // rotate sessions.json when oversized
      maxDiskBytes: "1gb",    // hard disk budget (optional)
      highWaterBytes: "800mb" // cleanup target (default 80% of maxDiskBytes)
    }
  }
}
```

### 12.5 DM Scope & Security

⚠️ **Critical for multi-user setups:** By default, all DMs share the same session (`dmScope: "main"`). This means User A's conversation context is visible to User B.

**Fix:** Set `dmScope: "per-channel-peer"` to isolate sessions per sender:

```json5
{
  session: {
    dmScope: "per-channel-peer"
  }
}
```

---

## 13. Advanced Memory Features

### 13.1 Session Memory Search (Experimental)

Index session transcripts and surface them via `memory_search`:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        experimental: { sessionMemory: true },
        sources: ["memory", "sessions"]
      }
    }
  }
}
```

- Opt-in, off by default
- Indexed asynchronously (results may be slightly stale)
- Isolated per agent

### 13.2 Additional Memory Paths

Index Markdown files outside the default workspace:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
      }
    }
  }
}
```

### 13.3 Memory Citations

When enabled, snippets include `Source: <path#line>` footers:

```json5
{
  memory: {
    citations: "auto"  // "auto" | "on" | "off"
  }
}
```

### 13.4 Custom OpenAI-Compatible Endpoints

Use any OpenAI-compatible embedding API:

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",
        model: "text-embedding-3-small",
        remote: {
          baseUrl: "https://api.example.com/v1/",
          apiKey: "YOUR_API_KEY",
          headers: { "X-Custom-Header": "value" }
        }
      }
    }
  }
}
```

---

## 14. QMD Backend (Experimental)

### 14.1 What is QMD?

QMD is a local-first search sidecar that combines **BM25 + vectors + reranking**. It's an alternative to OpenClaw's built-in SQLite indexer.

### 14.2 How It Works

- Markdown stays the source of truth
- OpenClaw shells out to QMD for retrieval
- Runs fully locally via Bun + node-llama-cpp
- Auto-downloads GGUF models on first use

### 14.3 Setup

1. Install QMD: `bun install -g https://github.com/tobi/qmd`
2. Enable in config: `memory.backend = "qmd"`
3. Configure paths and collections

### 14.4 Configuration

```json5
{
  memory: {
    backend: "qmd",
    citations: "auto",
    qmd: {
      includeDefaultMemory: true,
      update: { interval: "5m", debounceMs: 15000 },
      limits: { maxResults: 6, timeoutMs: 4000 },
      searchMode: "search",  // "search" | "vsearch" | "query"
      paths: [
        { name: "docs", path: "~/notes", pattern: "**/*.md" }
      ]
    }
  }
}
```

### 14.5 Fallback

If QMD fails or the binary is missing, OpenClaw automatically falls back to the built-in SQLite manager.

---

## 15. Configuration Reference

### 15.1 Complete Memory Search Configuration

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        // Embedding provider
        provider: "openai",              // "local" | "openai" | "gemini" | "voyage" | "mistral" | "ollama"
        model: "text-embedding-3-small",
        fallback: "openai",             // fallback provider
        outputDimensionality: 3072,     // for gemini-embedding-2-preview

        // Remote settings
        remote: {
          baseUrl: "https://api.openai.com/v1/",
          apiKey: "YOUR_KEY",
          headers: {},
          batch: {
            enabled: false,
            concurrency: 2,
            wait: true,
            pollIntervalMs: 5000,
            timeoutMinutes: 30
          }
        },

        // Local settings
        local: {
          modelPath: "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/...",
          modelCacheDir: "~/.openclaw/models"
        },

        // Search settings
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            candidateMultiplier: 4,
            mmr: { enabled: false, lambda: 0.7 },
            temporalDecay: { enabled: false, halfLifeDays: 30 }
          }
        },

        // Indexing
        extraPaths: [],
        cache: { enabled: true, maxEntries: 50000 },
        sync: { watch: true },

        // Store
        store: {
          path: "~/.openclaw/memory/{agentId}.sqlite",
          vector: { enabled: true, extensionPath: null }
        },

        // Multimodal (Gemini only)
        multimodal: {
          enabled: false,
          modalities: ["image", "audio"],
          maxFileBytes: 10000000
        },

        // Experimental
        experimental: { sessionMemory: false },
        sources: ["memory"]
      }
    }
  }
}
```

### 15.2 Complete Compaction Configuration

```json5
{
  agents: {
    defaults: {
      compaction: {
        enabled: true,
        reserveTokens: 16384,
        keepRecentTokens: 20000,
        reserveTokensFloor: 20000,
        model: null,                    // optional: different model for summaries
        identifierPolicy: "strict",     // "strict" | "off" | "custom"
        identifierInstructions: "",     // for "custom" policy
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction. Store durable memories now.",
          prompt: "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

### 15.3 Complete Session Pruning Configuration

```json5
{
  agents: {
    defaults: {
      contextPruning: {
        mode: "cache-ttl",              // "off" | "cache-ttl"
        ttl: "5m",
        keepLastAssistants: 3,
        softTrimRatio: 0.3,
        hardClearRatio: 0.5,
        minPrunableToolChars: 50000,
        softTrim: { maxChars: 4000, headChars: 1500, tailChars: 1500 },
        hardClear: { enabled: true, placeholder: "[Old tool result content cleared]" },
        tools: { allow: [], deny: [] }  // wildcards supported
      }
    }
  }
}
```

---

## 16. Best Practices & Recommendations

### 16.1 For Memory File Management

1. **Write it down** — "Mental notes" don't survive sessions. If it matters, put it in a file.
2. **Daily logs for daily things** — Use `memory/YYYY-MM-DD.md` for event-driven notes.
3. **Curate MEMORY.md regularly** — Periodically review daily logs and promote important items.
4. **Keep MEMORY.md focused** — Remove outdated info that's no longer relevant.
5. **Back up with Git** — Make the workspace a private Git repo.

### 16.2 For Search Configuration

1. **Enable hybrid search** for best recall (both exact and semantic matching).
2. **Enable temporal decay** if you have months of daily notes.
3. **Enable MMR** if you see redundant search results.
4. **Use local embeddings** for privacy; remote for speed/quality.
5. **Set up embedding cache** to avoid re-embedding unchanged content.

### 16.3 For Session Management

1. **Set `dmScope: "per-channel-peer"`** for multi-user setups.
2. **Enable session maintenance** (`mode: "enforce"`) in production.
3. **Use `/compact`** when sessions feel stale.
4. **Use `/context list`** to inspect what's consuming the context window.
5. **Set disk budgets** (`maxDiskBytes`) for long-running deployments.

### 16.4 For Performance

1. **Batch indexing** for large corpora (OpenAI/Gemini/Voyage).
2. **sqlite-vec** for hardware-accelerated vector search.
3. **Embedding cache** to reduce API calls during reindexing.
4. **QMD backend** for local-first search with reranking.
5. **Reasonable pruneAfter + maxEntries** to bound maintenance cost.

---

## 17. Glossary

| Term | Definition |
|---|---|
| **Context Window** | Maximum tokens a model can see at once (e.g., 200K for Claude) |
| **Compaction** | Summarizing old conversation into a compact entry (persisted) |
| **Session Pruning** | Trimming old tool results in-memory only (not persisted) |
| **Memory Flush** | Silent pre-compaction turn to save critical data to disk |
| **Vector Embedding** | Numerical representation of text for semantic similarity search |
| **BM25** | Keyword-based ranking algorithm (exact token matching) |
| **Hybrid Search** | Combining vector (semantic) + BM25 (keyword) retrieval |
| **MMR** | Maximal Marginal Relevance — diversity-aware re-ranking |
| **Temporal Decay** | Score multiplier that favors recent documents |
| **JSONL** | JSON Lines — one JSON object per line (transcript format) |
| **Session Key** | Routing identifier for conversation buckets |
| **Session ID** | Unique identifier for a specific transcript file |
| **QMD** | Query Markdown — local search sidecar with BM25 + vectors + reranking |
| **sqlite-vec** | SQLite extension for hardware-accelerated vector operations |
| **Workspace** | The agent's home directory (`~/.openclaw/workspace`) |
| **NO_REPLY** | Convention for silent turns (user sees nothing) |
| **Evergreen files** | Non-dated memory files exempt from temporal decay |

---

## Appendix: Key File Locations

```
~/.openclaw/
├── openclaw.json                          # Main configuration
├── workspace/                             # Agent workspace (memory lives here)
│   ├── AGENTS.md                          # Operating instructions
│   ├── SOUL.md                            # Persona and tone
│   ├── USER.md                            # User profile
│   ├── IDENTITY.md                        # Agent identity
│   ├── TOOLS.md                           # Local tool notes
│   ├── HEARTBEAT.md                       # Periodic check tasks
│   ├── MEMORY.md                          # Curated long-term memory
│   └── memory/                            # Daily memory logs
│       ├── 2026-03-15.md
│       ├── 2026-03-16.md
│       └── ...
├── agents/<agentId>/
│   ├── sessions/
│   │   ├── sessions.json                  # Session store (metadata)
│   │   ├── <sessionId>.jsonl              # Conversation transcripts
│   │   └── ...
│   └── qmd/                               # QMD state (if enabled)
│       ├── xdg-config/
│       └── xdg-cache/
├── memory/<agentId>.sqlite                # Vector search index
└── credentials/                           # OAuth tokens, API keys
```

---

*This document covers OpenClaw's memory system as of March 2026. The system is actively evolving — check the [official docs](https://docs.openclaw.ai) for the latest updates.*
