# Adaptive Career Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the Week 1 resume demo into a tested adaptive orchestration prototype for Class 10, Class 12, and college students.

**Architecture:** Use one Google ADK/Gemini agent only to parse unstructured input into a shared StudentProfile. Route the profile through deterministic Python matching, eligibility, top-three selection, and verification stages.

**Tech Stack:** Python 3.11+, Pydantic 2, Google ADK 2.x, pytest.

## Global Constraints

- No UI, frontend, authentication, deployment, or uploaded CSV dataset.
- No hardcoded API keys.
- Exactly three explainable pathways per result.
- Retry only HTTP 429 and 503, maximum three attempts.

---

### Task 1: Shared profile and output contracts
- [x] Add one StudentProfile schema for all stages.
- [x] Add pathway, recommendation, verification, and final-result schemas.

### Task 2: Curated prototype datasets
- [x] Add diverse streams and course pathways.
- [x] Extend the career dataset with duration, cost, trade-offs, and actions.

### Task 3: Deterministic guidance engines
- [x] Implement stage routing, scoring, eligibility, ranking, and safe-backup selection.
- [x] Implement evidence-backed college portfolio matching.

### Task 4: Verification and retry handling
- [x] Verify IDs, evidence, score order, roles, eligibility, and completeness.
- [x] Add exponential retry handling and clean failure messages for 429/503.

### Task 5: Live and offline entry points
- [x] Keep one ADK profile-parser agent.
- [x] Add Class 10, Class 12, college, and comparison CLI commands.

### Task 6: Tests and documentation
- [x] Add adaptive guidance, CLI, eligibility, verification, retry, and offline tests.
- [x] Update README, architecture diagram, sample profiles, and security files.
