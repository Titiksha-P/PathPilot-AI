# Recommendation Logic Framework

## Purpose

This document defines the **product logic** that Aryan's AI workflow should implement. It separates decision design from technical execution so that recommendations remain explainable, testable, and consistent across the application.

## Match Dimensions

The first version of PathPilot AI uses seven dimensions:

| Dimension | Weight | Meaning |
|---|---:|---|
| Interest Alignment | 25% | How strongly the career connects with the student's expressed interests |
| Skill Alignment | 20% | How closely current skills match the career's requirements |
| Subject Alignment | 10% | Whether preferred subjects support the path |
| Education Compatibility | 10% | Whether the student's current stage can realistically enter the pathway |
| Career Goal Alignment | 15% | Fit with goals such as creativity, stability, impact, income, or growth |
| Learning Preference Fit | 10% | Fit with how the student prefers to learn and work |
| Constraint Compatibility | 10% | Practical fit with time, cost, location, accessibility, or other constraints |

```text
Career Match Score =
(Interest × 0.25)
+ (Skill × 0.20)
+ (Subject × 0.10)
+ (Education × 0.10)
+ (Goal × 0.15)
+ (Learning Preference × 0.10)
+ (Constraint Fit × 0.10)
```

Each component is scored from 0 to 100 before weighting.

## Confidence Is Not the Match Score

Match score and confidence must remain separate.

- **Match score** describes how well the available profile aligns with a career.
- **Confidence** describes how reliable that score is based on profile completeness and consistency.

Example:

- Match score: 88
- Confidence: Medium
- Reason: Student supplied strong interest data but limited evidence of current skills.

## Recommendation Rules

A career recommendation must:

1. cite at least three profile-based reasons,
2. identify at least one possible limitation or uncertainty,
3. separate matched skills from missing skills,
4. provide an actionable next step,
5. avoid claiming guaranteed success,
6. avoid ranking a career highly when a hard constraint makes it unrealistic.

## Skill-Gap Classification

Each career skill is classified as:

- `matched` — supported by student evidence,
- `partial` — related experience exists but is incomplete,
- `missing_essential` — required for entry or progress,
- `missing_optional` — valuable but not immediately necessary.

## Career Comparison Logic

When comparing Career A and Career B, the system should explain:

- which career better matches the current profile,
- which requires less learning effort,
- which better satisfies the student's highest-priority goal,
- which has fewer constraint conflicts,
- what trade-off the student would accept by choosing either path.

The comparison should return a contextual conclusion such as:

> Career A is the stronger immediate fit because it uses more of your current skills. Career B may better satisfy your long-term goal, but it requires a larger technical foundation.

## Roadmap Generation Rules

The 90-day roadmap must be based on the student's `missing_essential` skills.

Each phase should contain:

- learning objective,
- specific action,
- suggested resource type,
- evidence of completion,
- estimated weekly effort,
- milestone outcome.

The roadmap must not be a generic list of course titles.

## Guardrails

- Do not use personality stereotypes as deterministic evidence.
- Do not treat salary as the only success indicator.
- Do not conceal uncertainty.
- Do not recommend paths that violate stated constraints without clearly flagging the conflict.
- Do not invent qualifications, exams, salary data, or resources absent from the approved career dataset.

## Acceptance Criteria

The recommendation layer is valid only when:

- identical input produces structurally consistent output,
- every reason can be traced to an input or dataset field,
- match score breakdown totals correctly,
- roadmap items map to identified gaps,
- comparison reflects the student's stated priorities,
- frontend can render the response without additional interpretation.
