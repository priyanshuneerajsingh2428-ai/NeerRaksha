# NeerRaksha — Smart Community Health Monitoring & Early Warning System
**SIH 2025 | Problem ID: SIH25001**

A research-oriented, runnable prototype for community symptom surveillance, water-quality monitoring, explainable risk scoring, and early-warning workflows for rural communities.

> **Safety boundary:** This is a hackathon/research prototype using synthetic demonstration data. It is NOT a medical diagnostic system, does not establish that water is safe/unsafe, and must not be used to make clinical or public-health decisions without validation and authorization from qualified public-health professionals.

## 1. Problem statement

**Smart Community Health Monitoring and Early Warning System for Water-Borne Diseases in Rural Northeast India.**

The SIH 2025 challenge proposes a system that:
- Collects health reports from clinics, ASHA workers and community volunteers through mobile apps or SMS.
- Uses AI/ML to identify patterns and estimate potential outbreak risk from symptoms, water-quality reports and seasonal trends.
- Integrates water-testing kits or IoT sensors for parameters such as turbidity, pH and bacterial presence.
- Sends alerts to district health officials and local governance bodies.
- Provides a multilingual community reporting interface and dashboards for hotspots, interventions and resource allocation.

The official SIH 2025 problem list identifies the sponsor as the **Ministry of Development of North Eastern Region**, category **Software**, ID **SIH25001**.

## 2. What this prototype implements

- FastAPI backend with health-report and water-observation endpoints.
- A transparent, rule-based risk index combining recent symptom reports, water observations and rainfall/seasonal context.
- A scikit-learn model training script using explicitly synthetic data (optional experiment; not epidemiologically validated).
- Streamlit dashboard for village-level monitoring and alert review.
- Synthetic demo dataset.
- Basic tests and API documentation.
- Privacy-conscious data model: no patient names or phone numbers are required.

## 3. Architecture

```text
ASHA / Clinic / Community reporter
             |
      Mobile / SMS adapter
       (future integration)
             |
        FastAPI backend
       /       |        \
 Reports   Water data   Alert engine
       \       |        /
        Village risk index
              |
    Streamlit district dashboard
              |
     Human review & escalation
```

The demo uses a transparent risk index rather than claiming a validated outbreak prediction model. The ML training script is included to demonstrate an experimental workflow; it must not be treated as a deployable clinical/public-health model.

## 4. Quick start

### Requirements
- Python 3.10 or newer
- pip

### Install
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Start the API
```bash
uvicorn app.main:app --reload
```
Open:
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health
- Summary: http://127.0.0.1:8000/api/summary

### Start the dashboard (in another terminal)
```bash
streamlit run dashboard.py
```

The API loads demo data from `data/demo_*.csv` at startup and keeps it in memory while it runs. The dashboard reads current reports and water observations from the API, so keep the API running while using the dashboard. Restarting the API reloads the CSV demo data.

### Optional synthetic model experiment
```bash
python scripts/train_demo_model.py
```
This creates `scripts/demo_model.joblib` from generated synthetic examples. Its score is only a software-demo check, not an epidemiological evaluation or a deployable health model.

## 5. Example API requests

Create a symptom report:
```bash
curl -X POST http://127.0.0.1:8000/api/reports \
  -H "Content-Type: application/json" \
  -d '{
    "village": "Demo Village A",
    "report_date": "2026-10-30",
    "symptoms": ["diarrhea", "vomiting"],
    "case_count": 4,
    "reporter_role": "asha",
    "age_band": "adult"
  }'
```

Add a water observation:
```bash
curl -X POST http://127.0.0.1:8000/api/water-observations \
  -H "Content-Type: application/json" \
  -d '{
    "village": "Demo Village A",
    "observation_date": "2026-10-30",
    "ph": 6.8,
    "turbidity_ntu": 8.2,
    "tds_mg_l": 310,
    "coliform_detected": true,
    "source_type": "community_handpump"
  }'
```

Get village risk:
```bash
curl http://127.0.0.1:8000/api/risk/Demo%20Village%20A
```

## 6. Data dictionary

### Symptom reports
| Field | Meaning |
|---|---|
| village | Community/village label |
| report_date | Date observed/reported |
| symptoms | Symptom tags; not a diagnosis |
| case_count | Number of people represented by this report |
| reporter_role | asha, clinic, volunteer |
| age_band | optional coarse age group |

### Water observations
| Field | Meaning |
|---|---|
| ph | measured pH |
| turbidity_ntu | turbidity in NTU |
| tds_mg_l | total dissolved solids, mg/L |
| coliform_detected | whether test indicated coliform presence |
| source_type | water source category |

**Important:** TDS, pH and turbidity alone do not prove microbiological safety. The demo flags coliform detection as a warning input but does not infer a pathogen or disease.

## 7. Research methodology

1. **Community reporting:** Capture date, village, symptom categories, case count and reporter role. Minimize personally identifiable information.
2. **Water monitoring:** Record field-kit or sensor observations with timestamp, source identifier and quality-control metadata.
3. **Data quality:** Validate units, ranges, duplicates, missing values and implausible spikes. Keep source and timestamp provenance.
4. **Signal construction:** Aggregate counts by village and time window; compare with a local baseline; consider season/rainfall and water observations.
5. **Risk estimation:** This prototype uses a transparent heuristic score for demonstration. A future validated model could use time-series features and calibrated classification, but only with representative, de-identified, labelled surveillance data.
6. **Human-in-the-loop response:** Alerts are review prompts for authorized health officials, not automated declarations of outbreaks.
7. **Evaluation:** Measure sensitivity/recall, precision, false-alert rate, detection lead time, calibration, missing-data robustness, latency and usability. Evaluate by village/time split to avoid leakage.

## 8. Research questions

- Does combining symptom trends and water observations provide earlier warning than symptom counts alone?
- How robust are risk signals when community reports are delayed or incomplete?
- Which features contribute most to alert generation?
- Can offline-first data capture improve reporting completeness in low-connectivity settings?
- How can alerts be made interpretable and actionable for local health teams?

## 9. Limitations and responsible use

- Demo data is synthetic and does not represent real villages or disease incidence.
- The risk score is a software demonstration, not a validated epidemiological threshold.
- No clinical diagnosis, treatment recommendation or pathogen identification is provided.
- Field sensor values require calibration, quality assurance and interpretation against current applicable standards by competent authorities.
- Real deployment requires approvals, community consent, security review, data governance, local language testing, clinical/public-health validation and integration with authorized surveillance workflows such as IDSP/IHIP where approved.
- Do not upload identifiable patient records to a public GitHub repository.

## 10. Suggested future work

- Offline-first Android/PWA application with local encrypted queue and sync.
- SMS/IVR gateway for low-connectivity communities.
- GIS mapping with verified village coordinates and role-based access.
- Sensor gateway using MQTT and calibrated devices.
- Multilingual UI (Assamese, Bengali, Bodo, Manipuri, Khasi, Mizo, Nepali, etc.) after local translation review.
- Temporal models (baseline statistical methods first; then XGBoost/LightGBM or temporal neural models if data supports them).
- Model cards, data sheets, drift monitoring and external validation.

## 11. Repository structure

```text
SIH25001_Waterborne_Early_Warning/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── risk.py
│   └── store.py
├── data/
│   ├── demo_symptom_reports.csv
│   ├── demo_water_observations.csv
├── research/
│   └── research_report.md
├── scripts/
│   └── train_demo_model.py
├── tests/
│   └── test_risk.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## 12. Sources

- SIH 2025 problem-statement PDF listing SIH25001 and its sponsoring organization: https://www.driems.ac.in/wp-content/uploads/2025/09/Smart-India-Hackathon_PROBLEM-STATEMENTS.pdf
- SIH problem statement archive (third-party reproduction): https://sih2025probelmstatement.vercel.app/
- Government of India, Integrated Disease Surveillance Programme: https://idsp.mohfw.gov.in/
- National Centre for Disease Control, IDSP overview: https://ncdc.mohfw.gov.in/includes/About/CentresAndDivision/IDSP.php
- WHO/UNICEF Joint Monitoring Programme: https://washdata.org/

Always verify current official guidelines, standards and surveillance procedures before field use.
