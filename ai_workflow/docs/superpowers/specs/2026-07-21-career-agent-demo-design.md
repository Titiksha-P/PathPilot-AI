# Career Guidance Agent Demo — Design

## Goal
Build a small Google ADK demo that accepts resume text, extracts an evidence-backed profile, compares it against a fixed and diverse career dataset, returns the top three career matches, and verifies that every recommendation is supported by portfolio evidence.

## Scope
- Three sequential agents: Resume Parser, Career Matcher, Verification Agent.
- Resume text input for Week 1; PDF upload is future work.
- Fixed dataset of ten diverse careers.
- Output: top three careers with score, reasons, evidence, and missing skills.
- Local deterministic demo works without an API key; ADK mode uses Gemini.

## Architecture
1. Resume Parser Agent converts resume text to `ResumeProfile` JSON and preserves evidence.
2. Career Matcher Agent calls a deterministic scoring tool over the fixed dataset, preventing broad-skill-only recommendations.
3. Verification Agent checks evidence coverage, score bounds, missing-skill consistency, and returns an approved or rejected result.
4. `Workflow` graph stores intermediate outputs in ADK session state through typed workflow node outputs.

## Personalization Strategy
Scoring uses four dimensions:
- 40% demonstrated skills
- 30% project/capability evidence
- 15% interests
- 15% education alignment

A skill only contributes strongly when it appears in a project, certification, or education context. The system therefore differentiates portfolios that share broad labels such as Python or AI.

## Error Handling
- Empty resume input is rejected.
- Parser output must satisfy Pydantic schemas.
- Career scores are clamped to 0–100.
- Verification rejects recommendations with no evidence or invalid score ordering.
- Local demo remains available when no Gemini API key is configured.
