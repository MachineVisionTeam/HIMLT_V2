# HIMLT — Survival Analysis Module

Survival Analysis integration for the **Hybrid Interactive Machine Learning Tool (HMLT)**
for Histopathology Image Analysis.

After nuclei prediction, the tool computes the percentage of positive (malignant epithelial)
nuclei per slide, stores it in the patient clinical survival database, and generates
Kaplan–Meier survival curves with a log-rank p-value.

## Folder Structure

```
HIMLT_V2_survival/
├── backend/
│   ├── app.py                    # Flask backend with /api/survival/km endpoint
│   ├── histomics_integration.py  # Redis-based ML bridge
│   └── settings.py               # Settings module
├── frontend/
│   └── App.tsx                   # React UI with KM plot SVG
├── data_prep/
│   └── merge_survival_data.py    # Joins nuclei CSV + TCGA clinical TSV → CSV
├── .env.example                  # Template for environment variables
├── .gitignore
└── README.md
```

## Workflow

1. **Nuclei prediction** runs on a TCGA slide via the existing HMLT pipeline.
2. **Backend** computes `pct_pos_nuclei = positive_count / total_nuclei`.
3. Value stored in the MySQL `patient_clinical_survival` table.
4. The `/api/survival/km` endpoint:
   - Pulls all patients with `pct_pos_nuclei IS NOT NULL`.
   - Splits patients into High/Low groups by median cutoff.
   - Computes KM curves and a log-rank p-value.
   - Returns JSON.
5. **Frontend** renders the two KM curves as an SVG plot with Plotly-style legend.

## API

**Endpoint:** `GET /api/survival/km`

**Response:**
```json
{
  "success": true,
  "median_cutoff": 0.1092,
  "p_value": 0.8756,
  "high_group": {
    "name": "High pct_pos_nuclei",
    "n": 47,
    "curve": [[0, 1.0], [108, 0.978], ...]
  },
  "low_group": {
    "name": "Low pct_pos_nuclei",
    "n": 46,
    "curve": [[0, 1.0], [147, 0.978], ...]
  }
}
```

## Database

MySQL database: `nuclei`

Table: `patient_clinical_survival`

```sql
CREATE TABLE patient_clinical_survival (
  patient_id VARCHAR(20) PRIMARY KEY,
  age FLOAT,
  sex VARCHAR(10),
  ethnicity VARCHAR(100),
  race VARCHAR(50),
  cancer_type_detailed VARCHAR(150),
  histologic_type VARCHAR(200),
  OS_time_days FLOAT,
  OS_event INT,
  pct_pos_nuclei FLOAT
);
```

## Running

**Backend:**
```bash
cd backend
python app.py
```
Runs on `127.0.0.1:5000`.

**Frontend (React + Vite):**
```bash
cd frontend
npm install
npm run build
```
Then deploy `dist/` to the web server.

## Dataset

- **Cohort:** TCGA-GBM
- **Patients merged:** 93
- **Mean pct_pos_nuclei:** 14.83%
- **Deceased / Alive:** 78 / 15
