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
├── INTERVIEWER_GUIDE.md                      ← Modularization track
├── INTERVIEWER_GUIDE_DEPLOY_COMPLETE.md      ← Deploy track (single source: bugs, scorecard, Q&A)
├── Cloud_Architect_Assessment_Interviewer_Guide_Deploy.docx
├── Cloud_Architect_Assessment_Interviewer_Guide_Deploy.pdf
├── generate_docx.py
├── generate_pdf_fpdf.py
├── generate_pdf.py                           ← runs PDF + DOCX generation
├── SOLUTION_GUIDE.md
├── ANSWER_KEY_QUESTIONS.md
└── SCORECARD.md                              ← Modularization track
```

### Regenerate deploy guide outputs

From `interviewer_materials/`:

```sh
python generate_pdf.py
```

Share only `candidate_materials/` with candidates (includes `TESTING.md` for deploy-track verification).
