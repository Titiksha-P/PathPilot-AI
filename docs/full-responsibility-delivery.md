# Titiksha — Full Product Intelligence & System Integration Delivery

## Role

**Product Intelligence & System Integration Lead**

This role owns the product rules and the shared system contract that keep UI/UX, frontend, backend, career data, and AI working as one product.

## 1. Problem Definition

Students do not primarily lack career information. They face fragmented guidance, generic recommendations, weak explanation, and no clear action plan. PathPilot AI addresses the complete decision gap:

- Which career fits the student?
- Why does it fit?
- What capabilities are already present?
- What is missing?
- How do two options compare?
- What should the student do over the next 90 days?

## 2. Product Journey

1. Student onboarding and consent
2. Profile creation
3. Interests, skills, subjects, goals, learning preferences, and constraints assessment
4. Explainable career ranking
5. Career detail and evidence view
6. Side-by-side Career Decision Simulator
7. Skill-gap analysis
8. Personalized 90-day roadmap
9. Progress review and feedback
10. Re-ranking and roadmap adaptation

## 3. Recommendation Logic

The deterministic baseline uses weighted components:

| Component | Weight |
|---|---:|
| Interest match | 25% |
| Current skill match | 20% |
| Education compatibility | 15% |
| Career-goal alignment | 15% |
| Learning-preference match | 10% |
| Future demand | 10% |
| Constraint fit | 5% |

Scores are normalized to 0–100. The implementation is available in `src/product_intelligence/scoring.py`.

The AI layer may enrich explanations and roadmaps, but it must not silently change the agreed scoring weights or output contract.

## 4. AI Output Specification

Each recommended career must contain:

- career identifier and name
- total match score
- confidence score
- component scores
- human-readable reasons
- matched skills
- missing skills
- qualifications and relevant exams
- recommended courses and resources
- immediate next steps
- 90-day roadmap
- evidence or data references when available

## 5. Shared JSON Contract

The canonical schemas are:

- `schemas/student-profile.schema.json`
- `schemas/recommendation-response.schema.json`

Runtime validation is implemented in `src/product_intelligence/contracts.py`.

The same contract must be used by:

- Kartik's frontend
- Aditya's backend APIs
- Aryan's AI workflow
- Adarsh's career-data mapping
- Ojaswi's screen content design

## 6. Career Decision Simulator

The simulator compares two careers across:

- personal fit
- current readiness
- learning effort
- education compatibility
- future opportunity
- constraint fit

The implementation is available in `src/product_intelligence/comparison.py`.

It supports informed choice; it must not present a career outcome as guaranteed.

## 7. Skill Gap & 90-Day Roadmap

The roadmap is split into three phases:

- Days 1–30: Foundation
- Days 31–60: Applied Practice
- Days 61–90: Portfolio & Readiness

Each phase contains focus skills, resources, a deliverable, and a success check. The implementation is available in `src/product_intelligence/roadmap.py`.

## 8. Cross-Team Integration Ownership

### Ojaswi — UI/UX
Uses the journey, fields, recommendation output, simulator dimensions, and roadmap structure defined here to design the screens.

### Kartik — Frontend
Collects the canonical student-profile input and renders the canonical recommendation response.

### Aditya — Backend
Persists profiles and results, exposes APIs, validates contracts, and bridges frontend, career data, and AI.

### Aryan — AI Workflow
Implements analysis, explanation generation, skill-gap enrichment, verification, and roadmap enrichment while conforming to the shared contract.

### Adarsh — Career Data
Supplies structured fields required by scoring, comparison, recommendation, and roadmap generation.

### Titiksha — Product Intelligence & Integration
Defines the problem, user journey, decision rules, schemas, expected outputs, feature behavior, acceptance criteria, demo story, and final integration checks.

## 9. Final Integration Gate

Before demo readiness, verify:

- UI fields match the canonical student schema.
- Frontend sends valid JSON accepted by the backend.
- Backend validates and persists the profile.
- Career data maps to the scoring fields.
- AI returns every required recommendation field.
- Scores and explanations do not contradict each other.
- Comparison uses the same career records as ranking.
- Roadmap addresses the identified missing skills.
- Frontend renders errors and incomplete results safely.
- The complete demo works from student input to final roadmap.

## 10. Runnable Technical Work

This contribution includes working Python modules, not documentation alone:

- deterministic scoring and confidence calculation
- ranked-career selection
- explanation generation
- student and recommendation contract validation
- frontend response assembly
- profile-based career comparison
- 90-day roadmap generation
- automated unit tests
- runnable example flow

Run locally:

```bash
python -m unittest discover -s tests -v
python examples/product_intelligence_demo.py
```

## Definition of Done

Titiksha's part is considered complete when the team can build against these rules without inventing incompatible inputs, outputs, ranking factors, comparison dimensions, or roadmap behavior independently.
