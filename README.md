# NivoTime Benefits Intelligence Suite — Live Company Project

MBA Live Company Project (PGDM E-Business, 2025–27) for **NivoTime**, proposing an
AI-powered **Benefits Intelligence Suite** sold primarily through mid-size insurance
brokers. This repository holds the final strategy report, the derived Product
Requirements Document (PRD) for a dashboard/prototype, and the AI/ML simulation code
behind both documents — reproducible end to end.

## What's in here

| Folder | Contents |
|---|---|
| `report/` | Final strategic report — source markdown, the financial model, all 12 figures, the docx build pipeline, and the compiled deliverable (`report/output/`) |
| `prd/` | Product Requirements Document for the dashboard/prototype — source markdown, the AI/ML simulation, 9 screen mockups + 6 diagrams, the docx build pipeline, and the compiled deliverable (`prd/output/`) |
| `data/` | `synthetic_employer_groups.csv` — the 600-row synthetic dataset the AI/ML models are trained and tested on |
| `notebooks/` | `NivoTime_AI_Simulation_Colab.ipynb` — a Colab-ready notebook version of the AI/ML simulation, so the models can be re-run and inspected interactively without any local setup |

## The two deliverables

1. **`report/output/NivoTime_Final_Report.docx` / `.pdf`** — the Live Company Project
   report: industry and company diagnosis, the flagship product recommendation (the
   Benefits Intelligence Suite), go-to-market and sales engine, a 6-model AI/ML layer,
   a 3-year financial model (Downside/Base/Upside), and a validation plan.
2. **`prd/output/NivoTime_PRD_Dashboard_Prototype.docx` / `.pdf`** — a buildable PRD
   derived from the report: 10 screens, functional/AI/data/non-functional requirements,
   a chart catalogue, a sprint plan, and a full traceability matrix back to the report's
   recommendations.

## Important note on the data

**All AI/ML results in both documents are trained on a synthetic dataset**
(`data/synthetic_employer_groups.csv`), generated to match published aggregate
statistics (e.g. IRDAI mean premium/life, typical claims ratios) — not on real
NivoTime or client data, which was not available for this project. Every model
result is genuinely computed (real scikit-learn models, real out-of-sample
metrics) but is explicitly labelled in both documents as **proof of mechanics,
not proof of real-world accuracy**. See `prd/src/prd_part3.md` (Section 7) and
`prd/src/prd_part4.md` (Appendix A) for the full disclosure and the generation
rules.

## Reproducing the AI/ML simulation

```bash
pip install -r requirements.txt
python prd/src/sim.py
```

This regenerates `data/synthetic_employer_groups.csv` and the model metrics
(renewal-forecast accuracy, peer-matching output, plan-simulator sensitivities,
claims-anomaly precision/recall) that Section 7 of the PRD and the dashboard
mockups are built from. Or open `notebooks/NivoTime_AI_Simulation_Colab.ipynb`
directly in Google Colab — no local install needed.

## Reproducing the figures and documents

Figure generation only needs the Python packages in `requirements.txt`:

```bash
python report/src/figures.py     # -> report/assets/fig/*.png
python prd/src/prd_figs.py       # -> prd/assets/fig/*.png (reuses some report figures)
```

Rebuilding the `.docx`/`.pdf` deliverables additionally needs three system tools —
[pandoc](https://pandoc.org/installing.html), LibreOffice (headless `soffice`, for
docx→pdf rendering), and Poppler's `pdftoppm`/`pdftotext` (for page-render QA and
TOC page-number resolution). With those installed:

```bash
python report/src/build.py   # markdown -> docx via pandoc, then python-docx post-processing
python report/src/toc.py     # resolves and fixes the table-of-contents page numbers
python prd/src/build_prd.py
python prd/src/toc_prd.py
```

`report/src/fixxml.py` / `prd/src/fixxml.py` is a general-purpose OOXML
element-reordering and validation-repair script, written for this project to make
python-docx's post-processed output pass strict schema validation (correct child-element
ordering for `pPr`, `rPr`, `tcPr`, `tblPr`, `settings`, etc.) — reusable on any
docx built the same way.

## Author

Anvesha — PGDM (E-Business) 2025–27, WeSchool. `anvesharajsingh@gmail.com`
