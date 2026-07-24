# Product & Integration Validation Checklist

Use this checklist before calling any PathPilot AI feature complete.

## Problem Alignment

- [ ] The feature solves a clearly stated student problem.
- [ ] The benefit can be explained without technical jargon.
- [ ] The feature helps the student decide, understand, compare, or act.
- [ ] The feature is not included only because it sounds impressive.

## UI/UX Alignment

- [ ] Every displayed field exists in the shared response schema.
- [ ] Loading, empty, error, and low-confidence states are designed.
- [ ] Recommendation explanations are visible and understandable.
- [ ] Comparison screens show trade-offs, not only scores.
- [ ] Roadmap screens present milestones and evidence of completion.

## Frontend Alignment

- [ ] Student inputs use the agreed field names.
- [ ] API requests match the documented contract.
- [ ] No recommendation score is calculated independently in the frontend.
- [ ] API errors are shown meaningfully to the user.
- [ ] The full journey works without manual data copying.

## Backend Alignment

- [ ] Student profiles can be created, fetched, and updated.
- [ ] Career data is validated before reaching the AI workflow.
- [ ] AI requests and responses are logged with request IDs.
- [ ] Responses pass JSON schema validation.
- [ ] Recommendations and roadmaps can be stored and retrieved.
- [ ] Error responses follow the common structure.

## AI Workflow Alignment

- [ ] Ranking uses the approved dimensions and weights.
- [ ] Match score and confidence are separate.
- [ ] Every explanation traces back to profile or career data.
- [ ] Missing skills are classified correctly.
- [ ] Roadmap steps map directly to essential skill gaps.
- [ ] The workflow avoids unsupported claims and invented data.

## Career Data Alignment

- [ ] Career records use stable identifiers.
- [ ] Required skills distinguish essential and optional skills.
- [ ] Qualifications, exams, resources, and salary information are sourced and structured.
- [ ] Missing data is represented honestly rather than guessed.
- [ ] Career fields match backend ingestion requirements.

## Career Decision Simulator

- [ ] The conclusion changes when student priorities change.
- [ ] Current readiness is separated from long-term potential.
- [ ] Both career paths show strengths and limitations.
- [ ] The comparison ends with a clear next action.
- [ ] No path is described as guaranteed or universally superior.

## Demo Readiness

- [ ] A student can complete the profile in under three minutes.
- [ ] The system returns three explained career recommendations.
- [ ] Two recommendations can be compared.
- [ ] Skill gaps are shown clearly.
- [ ] A personalized 90-day roadmap is generated.
- [ ] The team can explain how data moved through every layer.
- [ ] The demo has one prepared fallback profile in case of live-input failure.

## Final Product Question

Before approval, ask:

> Does this component help the student make a more informed, explainable, and actionable career decision?

If the answer is unclear, the component needs refinement.
