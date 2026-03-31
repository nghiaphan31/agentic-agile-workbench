---
doc_id: DOC-4
release: v2.5
status: Draft
title: Operations Guide
version: 1.0
date_created: 2026-03-31
authors: [Developer mode, Human]
previous_release: v2.4
cumulative: true
---

# DOC-4 -- Operations Guide (v2.5)

> **Status: DRAFT** -- This document is in draft for v2.5.0 release. It will be frozen upon QA approval.
> **Cumulative: YES** -- This document contains all operational guidance from v1.0 through v2.5.

---

## Table of Contents

1. [Environment Setup](#1-environment-setup)
2. [Daily Operations](#2-daily-operations)
3. [Release Procedures](#3-release-procedures)
4. [Troubleshooting](#4-troubleshooting)
5. [GitFlow Reference](#5-gitflow-reference)

---

## 1. Environment Setup

### 1.1 Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| VS Code | Latest | IDE |
| Roo Code | Latest | Agentic engine |
| Git | Latest | Version control |
| Python | 3.10+ | Proxy and scripts |
| Ollama | Latest | Local LLM |

### 1.2 Initial Setup

```powershell
# Clone the repository
git clone https://github.com/nghiaphan31/agentic-agile-workbench.git
cd agentic-agile-workbench

# Install Python dependencies
pip install -r requirements.txt

# Start the LLM proxy
python proxy.py

# Configure Roo Code to use localhost:8000 as API endpoint
```

---

## 2. Daily Operations

### 2.1 Session Start

1. Read `memory-bank/hot-context/activeContext.md`
2. Check `memory-bank/hot-context/progress.md` for current tasks
3. Review `docs/ideas/IDEAS-BACKLOG.md` for pending ideas

### 2.2 Session End

1. Update `memory-bank/hot-context/activeContext.md`
2. Update `memory-bank/hot-context/progress.md`
3. Commit changes with meaningful messages

### 2.3 Branch Workflow

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/IDEA-NNN-{slug}

# Work on feature...

# Push and create PR
git push -u origin feature/IDEA-NNN-{slug}
# Create PR via GitHub UI

# After PR approved, merge (DO NOT squash)
git checkout develop
git pull origin develop
git merge --no-ff feature/IDEA-NNN-{slug}
git push origin develop
```

---

## 3. Release Procedures

### 3.1 Creating a Release

1. **Create scoped branch:** `git checkout -b develop-vX.Y`
2. **Finalize scope:** Freeze all non-REFINED ideas
3. **Update docs:** Create `docs/releases/vX.Y/DOC-*-vX.Y-*.md`
4. **QA pass:** Run full coherence audit
5. **Human approval:** Get sign-off
6. **Tag:** `git tag vX.Y.0`
7. **Merge:** `git checkout master && git merge --ff develop-vX.Y`
8. **Push:** `git push origin master && git push origin vX.Y.0`
9. **Fast-forward develop:** `git checkout develop && git merge --ff master && git push origin develop`

### 3.2 Pre-Release Checklist

- [ ] All DOC-*-CURRENT.md pointers consistent
- [ ] All canonical docs meet minimum line counts
- [ ] CI passes on develop-vX.Y
- [ ] Human approved release
- [ ] Git tag created and pushed

---

## 4. Troubleshooting

### 4.1 Proxy Issues

| Symptom | Solution |
|---------|----------|
| Connection refused | Ensure `python proxy.py` is running |
| Model not found | Check model name in Roo Code settings |
| Auth errors | Verify API keys in `.env` |

### 4.2 Git Issues

| Symptom | Solution |
|---------|----------|
| Detached HEAD | `git checkout develop` |
| Diverged branches | `git fetch && git rebase origin/develop` |
| Push rejected | `git pull --rebase` then push |

---

## 5. GitFlow Reference

### 5.1 Branch Types

| Branch | Purpose | Created From | Merged To |
|--------|---------|--------------|-----------|
| `master` | Production frozen | -- | -- |
| `develop` | Wild mainline | `master` | `master` (at release) |
| `develop-vX.Y` | Scoped release | `develop` | `master` |
| `feature/*` | Single feature | `develop` or `develop-vX.Y` | Source branch |
| `hotfix/*` | Emergency fix | `master` tag | `master` + `develop` |

### 5.2 Merge Strategy

- **Prefer fast-forward merge**
- **NO squash merge** (preserves commit history)
- **NO --delete-branch** (keep for traceability)

---

*End of DOC-4-v2.5-Operations-Guide.md*
