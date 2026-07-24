# Backend Handoff — AI Automation Module

This document defines the Python contract the backend can call. This repository intentionally does not contain the production database or HTTP framework.

## Product flow

```text
Student Profile
-> Ranked Career Recommendations
-> Explained Match
-> Compare Two Careers
-> Skill-Gap Analysis
-> 90-Day Learning Roadmap
```

## Stable Python imports

```python
from app.integration import (
    analyze_student,
    compare_two_careers,
    generate_roadmap,
    get_skill_gap_analysis,
    run_complete_flow,
)
```

Each function accepts either a validated `StudentProfile` object or a plain dictionary matching the schema. Each function returns a JSON-serializable dictionary.

## 1. Analyze student

```python
result = analyze_student(student_profile_dict)
```

Suggested endpoint:

```text
POST /api/recommendations
```

The response contains the normalized profile, exactly three ranked pathways, evidence, explanations, missing requirements, and verification.

## 2. Compare two careers

```python
result = compare_two_careers(
    student_profile_dict,
    "data_scientist",
    "business_analyst",
)
```

Suggested endpoint:

```text
POST /api/careers/compare
```

Example request:

```json
{
  "student_profile": {},
  "career_id_1": "data_scientist",
  "career_id_2": "business_analyst"
}
```

The response includes:

- match score
- matched and missing skills
- supporting evidence
- minimum qualification
- certifications
- relevant courses/degrees
- entrance exams
- salary range
- common job roles
- learning resources
- future-scope/trend note
- source dataset filename
- current better-fit option and explanation

## 3. Skill-gap analysis

```python
result = get_skill_gap_analysis(student_profile_dict, "ai_ml_engineer")
```

Suggested endpoint:

```text
POST /api/skill-gaps
```

## 4. Generate roadmap

```python
result = generate_roadmap(student_profile_dict, "ai_ml_engineer")
```

Suggested endpoint:

```text
POST /api/roadmaps
```

The roadmap always contains:

1. Days 1–30 — Foundations
2. Days 31–60 — Applied project
3. Days 61–90 — Portfolio and readiness

## 5. Complete career-decision flow

```python
result = run_complete_flow(student_profile_dict)
```

Suggested endpoint:

```text
POST /api/decision-simulator
```

By default, the flow compares the top two recommendations and creates skill-gap analysis plus a roadmap for the best-fit career.

Optional explicit selection:

```python
result = run_complete_flow(
    student_profile_dict,
    career_id_1="data_scientist",
    career_id_2="business_analyst",
    roadmap_career_id="data_scientist",
)
```

## Career dataset

The college matcher loads `data/career_dataset.csv`. The CSV has 40 rows and is normalized by `app/career_data.py`.

Stable IDs are generated from the career title. Examples:

```text
data_scientist
ai_ml_engineer
prompt_engineer_genai_specialist
cybersecurity_analyst
full_stack_developer
ui_ux_designer
business_analyst
```

The backend can read the same normalized list by importing:

```python
from app.career_data import CAREERS, get_career
```

Salary and trend fields are supplied by the team CSV and should be verified before production release.

## Input validation and error mapping

| Python error | Suggested HTTP status | Meaning |
|---|---:|---|
| `pydantic.ValidationError` | 422 | Student profile does not match the schema |
| `ValueError: Unknown career` | 404 | Career ID is not in the current dataset |
| `ValueError: ...different careers` | 400 | Both comparison IDs are the same |
| `ValueError: ...college-stage profile` | 400 | Full career simulator requires a college profile |

Suggested error response:

```json
{
  "error": {
    "code": "INVALID_PROFILE",
    "message": "Student profile validation failed",
    "details": []
  }
}
```

## Generic demo files

- `data/profile_college_demo.txt`
- `data/sample_student_profile.json`
- `data/sample_decision_simulation.json`
- `data/career_dataset.csv`

## Verification commands

```bash
python -m pytest -q
python local_demo.py --college --full-flow
python local_demo.py --profile college_demo --career-compare data_scientist business_analyst
python local_demo.py --profile college_demo --roadmap ai_ml_engineer
```
