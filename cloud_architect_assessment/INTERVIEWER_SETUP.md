# Interviewer materials (local only)

Answer keys, scorecards, bug rubrics, and run-of-show guides are **not** in git.

## Setup (once per machine)

Copy your interviewer pack into this folder (from your team’s internal share — not the candidate repo):

```
cloud_architect_assessment/interviewer_materials/
```

That directory is listed in `.gitignore`. Git will never commit it.

## Expected local files

```
interviewer_materials/
├── INTERVIEWER_GUIDE.md
├── INTERVIEWER_GUIDE_DEPLOY.md
├── SOLUTION_GUIDE.md
├── ANSWER_KEY_QUESTIONS.md
├── SCORECARD.md
├── SCORECARD_DEPLOY.md
├── BUGS_AND_SOLUTIONS.md
├── DISCUSSION_QUESTIONS_DEPLOY.md
├── LEVELS_DEPLOY.md
└── ANALYSIS_DEPLOY.md
```

Share only `candidate_materials/` with candidates (includes `TESTING.md` for deploy-track verification).
