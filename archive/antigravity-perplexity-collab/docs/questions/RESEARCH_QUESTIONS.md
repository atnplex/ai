# Research Questions for Perplexity

> **Date**: 2026-02-03
> **Purpose**: Specific, well-formed questions for Perplexity research
> **Format**: Priority, artifacts needed, acceptance criteria

---

## Q1: Multi-Agent Orchestration Patterns

| Field | Value |
|-------|-------|
| **Priority** | P0 - Critical |
| **Question** | Best practices for multi-agent orchestration with model routing in 2025-2026. Focus on: state management across agents, cost-aware model selection algorithms, fault tolerance patterns. |
| **Artifacts Needed** | Current MCP config, model tiering strategy, cost constraints |
| **Acceptance Criteria** | Concrete architecture recommendation with: (1) state sync mechanism, (2) routing decision tree, (3) failover strategy, (4) 2+ academic citations |

---

## Q2: Tmpfs + SSOT Sync Architecture

| Field | Value |
|-------|-------|
| **Priority** | P0 - Critical |
| **Question** | Optimal architecture for homelab AI infrastructure with: tmpfs vs persistent storage trade-offs, SSOT sync strategies (GitHub → local with offline fallback), bootstrap sequence for cold starts with no internet. |
| **Artifacts Needed** | ATN_RUNTIME_FILESYSTEM_REQUIREMENTS.md, current VPS1 mount structure |
| **Acceptance Criteria** | (1) Decision matrix for tmpfs vs persist per path type, (2) sync algorithm with conflict resolution, (3) bootstrap flowchart, (4) recovery time estimates |

---

## Q3: MCP Server Architecture Patterns

| Field | Value |
|-------|-------|
| **Priority** | P1 - High |
| **Question** | MCP server architecture patterns for multi-provider load balancing: bidirectional state sync, session persistence across contexts, fault tolerance. |
| **Artifacts Needed** | Current MCP server list, usage patterns |
| **Acceptance Criteria** | (1) Recommended MCP topology, (2) state backend comparison, (3) session management strategy |

---

## Q4: Database Selection for Agent State

| Field | Value |
|-------|-------|
| **Priority** | P1 - High |
| **Question** | Database selection for AI agent state management: Redis vs PostgreSQL vs SQLite vs vector DB. Criteria: session persistence, vector similarity search, sub-10ms latency. |
| **Artifacts Needed** | Current postgres usage, state persistence requirements |
| **Acceptance Criteria** | (1) Comparison matrix with latency benchmarks, (2) Recommendation with justification, (3) Migration path if changing |

---

## Q5: Data Format for AI Consumption

| Field | Value |
|-------|-------|
| **Priority** | P1 - High |
| **Question** | Optimal data format for AI consumption: raw vs summarized storage, embedding strategies for semantic search, deduplication patterns. |
| **Artifacts Needed** | Current scratch folder structure, knowledge persistence patterns |
| **Acceptance Criteria** | (1) Storage format recommendation, (2) Embedding model recommendation, (3) Dedup algorithm for similar content |

---

## Q6: Free Tier Quota Maximization

| Field | Value |
|-------|-------|
| **Priority** | P1 - High |
| **Question** | Strategies for maximizing free tier quotas across multiple AI accounts: account rotation patterns, usage tracking and budget alerts, graceful degradation when limits hit. |
| **Artifacts Needed** | List of 15+ Google Pro accounts, Perplexity accounts, reset schedules |
| **Acceptance Criteria** | (1) Rotation algorithm, (2) Usage tracking schema, (3) Degradation decision tree |

---

## Q7: Token Optimization Techniques

| Field | Value |
|-------|-------|
| **Priority** | P2 - Medium |
| **Question** | Token optimization techniques: context compression algorithms, selective loading patterns, caching strategies for LLM interactions. |
| **Artifacts Needed** | Current context-compression skill, token usage patterns |
| **Acceptance Criteria** | (1) Compression algorithm comparison, (2) Cache invalidation strategy, (3) Estimated token savings |

---

## Q8: Secrets Management for AI Agents

| Field | Value |
|-------|-------|
| **Priority** | P0 - Critical |
| **Question** | Secrets management best practices for AI agents: BWS (Bitwarden Secrets) integration patterns, runtime fetching vs cached credentials, audit logging requirements. |
| **Artifacts Needed** | R69 secrets-management.md, BWS account structure |
| **Acceptance Criteria** | (1) Integration architecture, (2) Caching strategy with TTL, (3) Audit log schema |

---

## Question Batching Strategy

To minimize Perplexity API calls:

**Batch 1 (Architecture - Use sonar-reasoning-pro):**
- Q1 + Q3 (agent orchestration + MCP patterns)

**Batch 2 (Storage - Use sonar-reasoning-pro):**
- Q2 + Q4 + Q5 (tmpfs + database + data format)

**Batch 3 (Optimization - Use sonar):**
- Q6 + Q7 (quotas + tokens)

**Batch 4 (Security - Use sonar-reasoning-pro):**
- Q8 (secrets management)

**Estimated Cost:** 4 API calls × ~$0.02 = ~$0.08

---

*Document created for Perplexity collaboration.*
