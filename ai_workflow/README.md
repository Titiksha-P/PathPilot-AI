# AI Career Decision Simulator — Orchestration Module

AI Automation module for **SIH25094 — One-Stop Personalized Career & Education Advisor**.

The repository implements the team’s fixed product flow:

```text
Student Profile
-> Career Recommendations
-> Explained Match
-> Compare Two Careers
-> Skill-Gap Analysis
-> 90-Day Learning Roadmap
```

The database, HTTP APIs, authentication, and frontend are separate team modules. The backend can import the functions documented in `docs/backend_handoff.md`.

## What is included

- Class 10 stream guidance
- Class 12 degree/course guidance and eligibility checks
- College career decision simulator
- Generic public demo student profile
- 40-career dataset loaded from `data/career_dataset.csv`
- Evidence-based deterministic ranking
- Top 3 recommendations: best fit, strong alternative, safe backup
- Two-career comparison
- Skill-gap analysis
- Personalized 90-day roadmap
- Google ADK/Gemini profile parsing for live mode
- Offline mode that needs no API key
- Backend-ready JSON and importable Python functions

## Architecture

```text
Unstructured student text
        |
Google ADK + Gemini Profile Parser (live mode only)
        |
Normalized StudentProfile
        |
Deterministic Python router
   |-- Class 10 stream matcher
   |-- Class 12 course + eligibility matcher
   `-- College career matcher using career_dataset.csv
        |
Top 3 selector + verification
        |
Explained recommendations
        |
Compare two careers
        |
Skill-gap analysis
        |
Personalized 90-day roadmap
        |
Backend-ready JSON
```

Only profile parsing uses Gemini. Scoring, ranking, eligibility, comparison, gap analysis, roadmap generation, and verification use deterministic Python.

## Shared career dataset

`data/career_dataset.csv` contains 40 career records with these source fields:

- career option and domain
- required skills
- minimum qualification
- optional/recommended certifications
- relevant courses/degrees
- entrance exams
- salary range in India
- common job roles
- recommended learning resources
- a 2026 trend note

The loader in `app/career_data.py` converts each row into the stable structure used by the matching engine.

**Data caution:** salary ranges and trend notes are taken directly from the supplied team dataset. They are suitable for the prototype but should be verified before production use.

## Generic college demo

The public demo does not use a team member’s personal profile.

```bash
python local_demo.py --college --full-flow
```

It uses `Demo College Student`, a fictional B.Sc Computer Science student with Python, SQL, statistics, Power BI, beginner machine learning, and two sample projects.

Expected recommendation set includes careers from the CSV such as:

- Data Scientist
- Business Analyst
- Prompt Engineer / GenAI Specialist

Exact scores come from the deterministic profile-evidence matcher.

## Setup

```bash
python -m venv .venv
```

Windows CMD:

```cmd
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Offline demos

```bash
python local_demo.py --class10
python local_demo.py --class12
python local_demo.py --college
python local_demo.py --college --full-flow
python local_demo.py --compare
```

Compare two careers from the CSV:

```bash
python local_demo.py --profile college_demo --career-compare data_scientist business_analyst
```

Generate a roadmap for one CSV career:

```bash
python local_demo.py --profile college_demo --roadmap ai_ml_engineer
```

Print complete JSON:

```bash
python local_demo.py --college --full-flow --json
```

## Backend integration imports

```python
from app.integration import (
    analyze_student,
    compare_two_careers,
    generate_roadmap,
    get_skill_gap_analysis,
    run_complete_flow,
)
```

Example:

```python
from app.integration import run_complete_flow

result = run_complete_flow(student_profile_dict)
```

See `docs/backend_handoff.md` for request/response contracts and endpoint suggestions.

## Live Google ADK parser

Copy `.env.example` to `.env`. Never commit `.env`.

```cmd
copy .env.example .env
```

Expected variables:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-flash-latest
```

Run the generic college profile:

```bash
python run_adk.py --stage college --profile data/profile_college_demo.txt
python run_adk.py --stage college --profile data/profile_college_demo.txt --full-flow
```

## Retry handling

The application retries temporary `429` and `503` failures up to three times using exponential delay, then returns a clean error. Offline mode remains available without Gemini.

## Tests

```bash
python -m pytest -q
```

The test suite covers:

- Class 10 and Class 12 guidance
- loading all 40 careers from the CSV
- generic public college profile
- evidence-based ranking
- false partial-word match prevention
- exactly three ranked recommendations
- comparison and CSV detail fields
- skill gaps
- all three roadmap phases
- backend adapters and JSON serialization
- CLI commands and Windows-safe output
- retry behaviour

## Main files

```text
app/schemas.py          Shared profile and output schemas
app/datasets.py         Class 10 and Class 12 pathway data
app/career_data.py      CSV career loader and career lookup
app/local_parser.py     Generic offline demo profiles
app/matcher.py          Deterministic scoring and ranking
app/comparison.py       Two-career comparison
app/skill_gaps.py       Prioritized missing-skill analysis
app/roadmap.py          90-day roadmap generator
app/orchestrator.py     Complete decision-simulator flow
app/integration.py      Backend import adapters
app/verifier.py         Output verification
data/career_dataset.csv Shared 40-career prototype dataset
```
