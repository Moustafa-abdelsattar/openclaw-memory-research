# 🦞 Lobster Memory: How AI Agents Remember

**A Deep Dive into Memory Systems — OpenClaw vs Claude Code vs Antigravity**

---

## 🧠 The Core Problem: AI Amnesia

Every AI model wakes up with **zero memory**. No matter how smart it is, it forgets everything after each conversation. The "memory problem" is the #1 challenge in building useful AI agents.

**Three tools, three philosophies** for solving it:

| | OpenClaw 🦞 | Claude Code 🟠 | Antigravity 🚀 |
|---|---|---|---|
| **What it is** | Self-hosted autonomous AI agent | Terminal-based coding assistant | Google's agent-first IDE |
| **Memory philosophy** | Persistent, multi-layered, always-on | Session-scoped, code-focused | Hierarchical, IDE-integrated |
| **Core metaphor** | "Your AI has a journal and a brain" | "Your AI has a notepad per project" | "Your AI has a knowledge base" |

---

## 🔑 Key Insight #1: Memory Architecture

### OpenClaw — Two-Layer Human-Like Memory

```
MEMORY.md (long-term)     ← Curated wisdom, like human long-term memory
memory/YYYY-MM-DD.md      ← Daily journal, like short-term memory
```

- **Daily logs** capture what happened today (append-only)
- **MEMORY.md** distills patterns, preferences, and durable facts
- Agent reads today + yesterday on startup → instant continuity
- Security: MEMORY.md is **never loaded in group chats** (prevents data leakage)

### Claude Code — Hierarchical Project Memory

```
~/.claude/CLAUDE.md        ← User-wide preferences
./CLAUDE.md                ← Project instructions (shared with team)
./CLAUDE.local.md          ← Personal project overrides
```

- Recursively searches upward from working directory
- Supports `@path` imports (up to 5 levels deep)
- `/init` bootstraps memory by analyzing the codebase
- **Resets between sessions by design** — fresh context each time

### Antigravity — Knowledge Base Memory

```
GEMINI.md                  ← Project-wide rules and persona
Hierarchical context       ← Global → Project → Sub-directory
Knowledge base             ← Learned patterns from interactions
```

- Agents save useful context to a persistent knowledge base
- Develops "permanent memory" that adapts over time
- No manual training needed — learns from usage

### ⚡ Insight

> **OpenClaw** treats memory as a personal diary system — intimate, cumulative, always growing.  
> **Claude Code** treats memory as project documentation — clean, shared, resettable.  
> **Antigravity** treats memory as an evolving knowledge graph — automatic, adaptive, IDE-bound.

---

## 🔑 Key Insight #2: Memory Retrieval

How does each system *find* the right memory when it needs it?

### OpenClaw — Hybrid Vector + Keyword Search

OpenClaw uses a **dual retrieval system** that's significantly more advanced:

1. **Vector search** (semantic): "Mac Studio gateway host" finds "the machine running the gateway"
2. **BM25 search** (keyword): Finds exact tokens like commit hashes, error codes, env vars
3. **Weighted merge**: `finalScore = 0.7 × vectorScore + 0.3 × textScore`

**Plus two post-processing stages:**

- **MMR re-ranking** — removes near-duplicate results, maximizes diversity
- **Temporal decay** — recent memories rank higher (half-life: 30 days)

**Supported embedding providers:** Local (offline), OpenAI, Gemini, Voyage, Mistral, Ollama

### Claude Code — Context Window + File Search

- Relies on the model's **1M token context window** as primary "memory"
- Auto-compaction summarizes older context when window fills
- No vector search — memory is what's in CLAUDE.md files + conversation
- Auto Memory: Claude saves notes for itself across sessions (build commands, debug insights)

### Antigravity — Artifact-Based + Knowledge Base

- Agents generate **Artifacts** (task lists, plans, screenshots, recordings)
- Knowledge base learns from interactions automatically
- No explicit vector search documented — relies on IDE context + persistent state

### ⚡ Insight

> OpenClaw's hybrid search is the **most sophisticated retrieval system** of the three. It can find memories by meaning OR by exact match, and it actively fights redundancy and staleness. Claude Code relies more on brute-force context (huge window), while Antigravity auto-learns but with less user control.

---

## 🔑 Key Insight #3: What Happens When Memory Gets Full?

Every system hits a wall when conversations get too long. Here's how each handles it:

### OpenClaw — Three-Layer Defense

```
Layer 1: Session Pruning     → Trims old tool outputs (in-memory only)
Layer 2: Memory Flush         → Silent save-to-disk before compaction
Layer 3: Auto-Compaction      → Summarizes old conversation, persists summary
```

**The Memory Flush is unique to OpenClaw:**
- When context is ~4000 tokens from the limit, a **silent turn** fires
- The agent writes critical info to disk **before** compaction erases it
- User sees nothing (NO_REPLY) — it's fully automatic
- Prevents the "compaction amnesia" problem

### Claude Code — Compaction + Large Window

- **1M token window** means compaction is rare
- When needed: auto-compaction summarizes older context
- `/compact` for manual trigger with custom instructions
- Previous thinking blocks auto-stripped to save space

### Antigravity — Knowledge Base Persistence

- Agents save important context to persistent knowledge base
- Less documented compaction mechanism
- Relies more on agent autonomy to decide what's worth remembering

### ⚡ Insight

> OpenClaw's **pre-compaction memory flush** is a genuinely novel approach. It's like a human frantically writing notes before falling asleep — ensuring nothing critical is lost. Claude Code's approach is "just have a bigger brain" (1M tokens). Antigravity delegates the problem to the agent itself.

---

## 🔑 Key Insight #4: Scope & Multi-Channel

### OpenClaw — Lives Everywhere

- **WhatsApp, Telegram, Discord, iMessage, Web** — all simultaneously
- Memory is **cross-channel** — tell it something on WhatsApp, it remembers on Discord
- Session isolation: group chats get separate sessions (security)
- Heartbeats: proactively checks email, calendar, weather without being asked
- **Cron jobs**: scheduled tasks with their own isolated sessions

### Claude Code — Lives in Your Terminal/IDE

- Terminal, VS Code, Desktop app, Web
- Memory is **per-project** (CLAUDE.md hierarchy)
- No cross-application memory
- Reactive only — does what you tell it, when you tell it

### Antigravity — Lives in the IDE

- Modified VS Code (Editor View + Manager View)
- Integrated browser agent for end-to-end testing
- Memory is **per-project** with IDE-level persistence
- Multi-agent orchestration within the IDE

### ⚡ Insight

> OpenClaw is the **only one designed as a life-wide agent** — it's not just a coding tool, it's a personal assistant that happens to code. Claude Code and Antigravity are developer tools first and foremost.

---

## 🔑 Key Insight #5: Security & Privacy

| Concern | OpenClaw | Claude Code | Antigravity |
|---|---|---|---|
| **Data location** | Your machine (self-hosted) | Anthropic's servers | Google's servers |
| **Memory isolation** | MEMORY.md blocked in group chats | Per-project CLAUDE.local.md | IDE-level isolation |
| **Multi-user safety** | `dmScope` per-channel-peer isolation | N/A (single user) | N/A (single user) |
| **Cost model** | Free software + API costs ($6-200/mo) | $20/mo subscription | Free (preview) |

### ⚡ Insight

> OpenClaw offers the **strongest data sovereignty** — your memories never leave your machine. But this comes with responsibility: you manage the security. Claude Code and Antigravity trade control for convenience.

---

## 🔑 Key Insight #6: Advanced Memory Features (OpenClaw-Specific)

These features have **no equivalent** in Claude Code or Antigravity:

1. **Multimodal Memory** — Index images and audio alongside text (via Gemini Embedding 2)
2. **Session Memory Search** (experimental) — Search past conversation transcripts
3. **QMD Backend** — Local-first search sidecar with BM25 + vectors + reranking
4. **Embedding Cache** — Avoid re-embedding unchanged content (up to 50K entries)
5. **Batch Indexing** — Async bulk embedding via OpenAI/Gemini Batch API (cheaper + faster)
6. **sqlite-vec Acceleration** — Hardware-accelerated vector search
7. **Temporal Decay** — Exponential recency boost (configurable half-life)
8. **MMR Diversity** — Maximal Marginal Relevance to avoid redundant results
9. **Memory Citations** — `Source: <path#line>` for verifiable recall

---

## 📊 Final Comparison Matrix

| Dimension | OpenClaw 🦞 | Claude Code 🟠 | Antigravity 🚀 |
|---|---|---|---|
| **Memory persistence** | ⭐⭐⭐⭐⭐ Always-on, cross-session | ⭐⭐⭐ Auto-memory + CLAUDE.md | ⭐⭐⭐⭐ Knowledge base |
| **Retrieval sophistication** | ⭐⭐⭐⭐⭐ Hybrid + MMR + decay | ⭐⭐⭐ Context window + files | ⭐⭐⭐ KB lookup |
| **Context management** | ⭐⭐⭐⭐⭐ Flush + prune + compact | ⭐⭐⭐⭐ 1M window + compact | ⭐⭐⭐ Agent-managed |
| **Multi-channel** | ⭐⭐⭐⭐⭐ WA/TG/Discord/iMsg/Web | ⭐⭐ Terminal/IDE/Web | ⭐⭐ IDE only |
| **Coding ability** | ⭐⭐⭐⭐ Via sub-agents | ⭐⭐⭐⭐⭐ Native, best-in-class | ⭐⭐⭐⭐⭐ Native, multi-agent |
| **Ease of setup** | ⭐⭐ Self-hosted, technical | ⭐⭐⭐⭐ Install and go | ⭐⭐⭐⭐ Download IDE |
| **Data privacy** | ⭐⭐⭐⭐⭐ Fully local | ⭐⭐⭐ Cloud-dependent | ⭐⭐⭐ Cloud-dependent |
| **Proactive behavior** | ⭐⭐⭐⭐⭐ Heartbeats, cron, auto | ⭐ Reactive only | ⭐⭐⭐ Agent autonomy |

---

## 💡 Bottom Line

> **OpenClaw** is the most comprehensive memory system — built for a **persistent, always-on AI companion** that remembers across channels, sessions, and time. It's the choice when you want an AI that truly *knows* you.
>
> **Claude Code** is the most powerful **coding** memory system — optimized for project context, developer workflows, and massive context windows. It's the choice when you want the best code assistant.
>
> **Antigravity** is the most **autonomous** development environment — agents that learn, plan, and verify independently. It's the choice when you want AI to handle full engineering tasks end-to-end.

**They're not competitors — they're different tools for different jobs. And OpenClaw can orchestrate the other two as sub-agents.** 🦞

---

*Research compiled March 2026. Sources: OpenClaw docs (docs.openclaw.ai), Anthropic docs (claude.com), Google Antigravity docs (antigravity.google), community research.*
