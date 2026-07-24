# Career Decision Simulator Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Complete Aryan's AI Automation module with deterministic two-career comparison, skill-gap analysis, a personalized 90-day roadmap, and a stable backend handoff contract.

**Architecture:** Preserve the current StudentProfile -> rank_pathways -> verify_guidance pipeline. Add focused deterministic services that reuse the existing career matcher and career dataset, then compose them in a new `run_decision_simulator` orchestration entry point. Expose JSON-serializable adapter functions for Aditya's backend without adding a web framework or database to Aryan's repository.

**Tech Stack:** Python 3.11+, Pydantic 2, pytest; Google ADK remains limited to live profile parsing.

## Global Constraints

- Do not use or commit `Career_Dataset_Week1-1.csv`.
- Do not add a database, web framework, frontend, authentication, or deployment code.
- Keep all comparison, scoring, gap analysis, roadmap generation, and verification deterministic and offline-capable.
- Do not invent salary or future-scope facts when the current local dataset does not provide them; return explicit unavailable values.
- Keep all existing CLI commands and tests backward compatible.

---

### Task 1: Public career lookup and extended schemas

**Files:**
- Modify: `app/career_data.py`
- Modify: `app/schemas.py`
- Test: `tests/test_decision_simulator.py`

**Interfaces:**
- Produces: `get_career(career_id: str) -> dict`
- Produces: `CareerComparison`, `SkillGapAnalysis`, `LearningRoadmap90Day`, and `CareerDecisionSimulation` Pydantic contracts.

- [x] Write failing tests for unknown career lookup and schema invariants.
- [x] Run the focused tests and confirm they fail for missing interfaces.
- [x] Implement the lookup and schemas with validators for distinct careers and exactly three roadmap phases.
- [x] Run the focused tests and confirm they pass.

### Task 2: Career comparison and skill-gap analysis

**Files:**
- Modify: `app/matcher.py`
- Create: `app/comparison.py`
- Create: `app/skill_gaps.py`
- Test: `tests/test_decision_simulator.py`

**Interfaces:**
- Produces: `score_career(profile: StudentProfile, career_id: str) -> PathwayMatch`
- Produces: `compare_careers(profile: StudentProfile, career_id_1: str, career_id_2: str) -> CareerComparison`
- Produces: `analyze_skill_gaps(profile: StudentProfile, career_id: str) -> SkillGapAnalysis`

- [x] Write failing behavioral tests for Aryan's comparison, unknown/same career validation, and a career with missing skills.
- [x] Run the focused tests and confirm expected failures.
- [x] Implement minimal deterministic services using the existing scoring evidence.
- [x] Run the focused tests and confirm they pass.

### Task 3: Personalized 90-day roadmap

**Files:**
- Create: `app/roadmap.py`
- Test: `tests/test_decision_simulator.py`

**Interfaces:**
- Consumes: `analyze_skill_gaps(profile, career_id)` and the local career record.
- Produces: `generate_90_day_roadmap(profile: StudentProfile, career_id: str) -> LearningRoadmap90Day`

- [x] Write a failing test requiring three exact phases, personalized skills, deliverables, and no unsupported salary claims.
- [x] Run the focused test and confirm it fails.
- [x] Implement the three-phase roadmap: foundations, applied project, portfolio/readiness.
- [x] Run the focused test and confirm it passes.

### Task 4: Complete orchestration and backend adapters

**Files:**
- Modify: `app/orchestrator.py`
- Create: `app/integration.py`
- Modify: `app/__init__.py`
- Test: `tests/test_decision_simulator.py`

**Interfaces:**
- Produces: `run_decision_simulator(profile, career_id_1=None, career_id_2=None, roadmap_career_id=None) -> CareerDecisionSimulation`
- Produces JSON adapters: `analyze_student`, `compare_two_careers`, `get_skill_gap_analysis`, `generate_roadmap`, `run_complete_flow`.

- [x] Write failing tests for default top-two comparison, best-fit roadmap, dict input validation, and JSON-serializable output.
- [x] Run the focused tests and confirm they fail.
- [x] Implement orchestration and adapters without adding HTTP/database code.
- [x] Run the focused tests and confirm they pass.

### Task 5: CLI, documentation, examples, and complete verification

**Files:**
- Modify: `local_demo.py`
- Modify: `README.md`
- Create: `docs/backend_handoff.md`
- Create: `data/sample_student_profile.json`
- Generate: `data/sample_decision_simulation.json`
- Modify: `tests/test_cli.py`

**Interfaces:**
- Produces CLI options: `--full-flow`, `--career-compare CAREER_1 CAREER_2`, and `--roadmap CAREER_ID`.
- Produces an import contract and sample JSON for Aditya's backend.

- [x] Write failing CLI tests for the complete flow, two-career comparison, and roadmap output.
- [x] Run the focused CLI tests and confirm they fail.
- [x] Implement CLI output, documentation, and sample files.
- [x] Run all tests with `python -m pytest -q` and require a clean pass.
- [x] Run `python local_demo.py --college --full-flow` and `python local_demo.py --profile aryan --career-compare ai_agent_developer data_analyst --roadmap ai_agent_developer --json`.
- [x] Package the verified repository as a new ZIP.
