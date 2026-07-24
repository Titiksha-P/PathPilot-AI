# Career Guidance Agent Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable three-agent Google ADK demo for evidence-based career guidance from resume text.

**Architecture:** A SequentialAgent runs a resume parser, deterministic career matcher tool, and verifier. A local offline runner mirrors the contracts for demonstrations without an API key.

**Tech Stack:** Python 3.10+, Google ADK, Gemini 3.5 Flash, Pydantic, pytest.

## Global Constraints
- Use exactly three agents.
- Return exactly three ranked careers.
- Preserve evidence from the resume for each recommendation.
- Use a fixed dataset of ten diverse careers.
- Keep PDF extraction outside Week 1 scope.

---

### Task 1: Schemas and career dataset
- [x] Define Pydantic input/output contracts.
- [x] Add ten diverse career profiles.
- [x] Add tests for dataset shape and schema validation.

### Task 2: Deterministic evidence-based matcher
- [x] Implement normalized skill/context scoring.
- [x] Return top three scores, reasons, evidence, and missing skills.
- [x] Add tests proving different portfolios receive different results.

### Task 3: Verification logic
- [x] Check score order, bounds, evidence, and missing skills.
- [x] Add passing and failing verification tests.

### Task 4: Google ADK orchestration
- [x] Define Parser, Matcher, and Verification LlmAgents.
- [x] Connect them with SequentialAgent and output keys.
- [x] Use Gemini 3.5 Flash and structured outputs.

### Task 5: Offline demo and documentation
- [x] Add Aryan resume sample and two contrasting sample portfolios.
- [x] Add CLI commands for one profile and comparison mode.
- [x] Add README, environment example, and sample output.
