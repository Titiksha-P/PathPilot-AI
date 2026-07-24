# Adaptive Career & Education Guidance Orchestration Design

## Purpose

Build an orchestration prototype for SIH25094 that supports Class 10, Class 12, and college students without overlapping with frontend or UI work.

## Architecture

The live path uses one Google ADK/Gemini profile-parser agent for unstructured input. All scoring, eligibility, ranking, safe-backup selection, and verification are deterministic Python stages backed by curated local datasets. The offline path skips Gemini entirely and runs stable sample profiles.

## Flows

- Class 10: marks + aptitude + interests + preferences → top three stream pathways.
- Class 12: stream + subjects + marks + entrance readiness + constraints → top three course pathways.
- College: education + skills + projects + interests → top three career pathways using portfolio evidence.

## Output contract

Every result returns a best fit, strong alternative, and safe/affordable backup with a score, evidence, eligibility, missing requirements, duration, cost category, trade-offs, outcomes, and next actions.

## Reliability

Gemini is never used for scoring or verification. Temporary 429/503 errors are retried at most three times with exponential backoff, then converted to a short user-facing error. API keys are loaded only from environment variables.
