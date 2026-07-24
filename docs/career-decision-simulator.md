# Career Decision Simulator

## Purpose

The Career Decision Simulator is PathPilot AI's signature feature. It helps a student compare two realistic pathways using their own profile instead of relying on generic pros-and-cons lists.

## Inputs

- student profile
- Career A
- Career B
- student's top priority
- available weekly learning time
- budget and location constraints

## Comparison Dimensions

| Dimension | Description |
|---|---|
| Personal Fit | Alignment with interests, goals and preferred subjects |
| Current Readiness | Existing skills and education compatibility |
| Skill-Gap Size | Number and importance of missing essential skills |
| Learning Effort | Estimated effort required to reach an entry milestone |
| Constraint Fit | Compatibility with time, budget and location |
| Evidence Path | How quickly the student can build proof through projects or assessments |
| Long-Term Goal Fit | Alignment with the student's stated future priorities |

## Required Output

```json
{
  "career_a": {
    "career_id": "career_uiux",
    "fit_score": 88,
    "readiness_score": 72,
    "essential_gaps": ["user_research", "prototyping"],
    "estimated_weekly_effort": 7
  },
  "career_b": {
    "career_id": "career_data_science",
    "fit_score": 78,
    "readiness_score": 48,
    "essential_gaps": ["python", "statistics", "machine_learning"],
    "estimated_weekly_effort": 11
  },
  "decision_summary": "UI/UX Design is the stronger immediate fit because it uses more of the student's existing strengths. Data Science better supports the student's analytical interest but requires a larger technical foundation.",
  "recommended_for_now": "career_uiux",
  "recommended_for_long_term_exploration": "career_data_science"
}
```

## UX Presentation

The comparison screen should include:

- side-by-side career cards
- profile-based strengths for each path
- missing essential skills
- learning effort indicator
- readiness meter
- trade-off statement
- "Why this conclusion?" expandable explanation
- actions to select a path or generate both roadmaps

## Decision Language Rules

Use:

- "stronger immediate fit"
- "requires more preparation"
- "better aligned with your stated priority"
- "contains a constraint conflict"

Avoid:

- "this is your perfect career"
- "you will definitely succeed"
- "this career is objectively better"

## Acceptance Criteria

The simulator is successful when:

1. its conclusion changes when the student's priorities change,
2. it explains trade-offs rather than only displaying scores,
3. every comparison field can be traced to profile or career data,
4. it distinguishes current readiness from long-term potential,
5. it gives the student a clear next action.
