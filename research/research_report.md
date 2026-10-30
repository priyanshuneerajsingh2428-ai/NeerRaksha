# Research Report: NeerRaksha
## Smart Community Health Monitoring and Early Warning System for Water-Borne Diseases in Rural Northeast India

**Hackathon reference:** Smart India Hackathon 2025, SIH25001  
**Sponsor listed in the SIH problem-statement catalogue:** Ministry of Development of North Eastern Region  
**Category:** Software | **Theme:** MedTech / BioTech / HealthTech

## Abstract
Rural communities can face delays in recognizing clusters of acute gastrointestinal illness when community reporting, water-quality observations and public-health response workflows are fragmented. NeerRaksha is a proposed community-level surveillance and early-warning prototype that brings together de-identified symptom reports, water-source observations and contextual signals in a village-level review dashboard. The system is designed around low-bandwidth reporting, transparent indicators and human review by authorized public-health personnel. This implementation includes a FastAPI service, synthetic demonstration records, a rule-based signal score and a Streamlit dashboard. The score is deliberately described as a heuristic demonstration rather than a validated prediction. An operational system would require representative surveillance data, epidemiological validation, field sensor quality assurance, privacy safeguards and formal integration with government systems.

## 1. Problem definition and source-derived requirements
The published SIH25001 description calls for a smart health surveillance and early-warning system that can:
1. Collect health reports from local clinics, ASHA workers and community volunteers through mobile apps or SMS.
2. Use AI/ML to identify patterns and estimate potential outbreaks from symptoms, water-quality reports and seasonal trends.
3. Integrate water-testing kits or IoT sensors to monitor water-source contamination, with examples such as turbidity, pH and bacterial presence.
4. Provide timely alerts to district health officials and local governance bodies.
5. Include a multilingual community reporting interface and awareness campaigns.
6. Provide dashboards for hotspots, intervention tracking and resource allocation.

The SIH catalogue lists this as SIH25001, a software problem statement sponsored by the Ministry of Development of North Eastern Region. The above list reflects the published description; detailed operational specifications, data access, sensor protocols and evaluation thresholds are not supplied in that catalogue.

## 2. Proposed solution
NeerRaksha is a modular prototype with five layers:
- **Data acquisition:** health-worker symptom reports and water-quality observations.
- **Validation and storage:** schema validation, timestamp checks and minimized personal data.
- **Signal analysis:** village/time-window aggregation, transparent heuristic risk index and optional synthetic ML experiment.
- **Visualization:** village review queue, recent observations and factors contributing to a signal.
- **Response workflow:** human review by authorized officials; any alert should be confirmed and actioned through established public-health procedures.

## 3. Scope and non-goals
### In scope
- Capture aggregate symptom counts, symptom tags, village and date.
- Capture water observations and test metadata.
- Produce a transparent demonstration signal.
- Display village summaries and factors.
- Expose API endpoints for future mobile/SMS integration.

### Explicitly out of scope
- Diagnosing cholera, typhoid or any other disease.
- Declaring an outbreak automatically.
- Declaring water safe based only on pH, turbidity or TDS.
- Prescribing treatment.
- Replacing laboratory testing, clinicians, IDSP/IHIP or public-health authorities.

## 4. Why this problem matters
Water-related health risks are influenced by environmental conditions, water and sanitation infrastructure, seasonal variation, human exposure and reporting delays. A community-level system can help organize signals from multiple sources, but it only adds value if data quality, coverage, interpretation and response pathways are reliable. WHO drinking-water guidance frames water safety through risk management and independent surveillance; it should be consulted alongside applicable Indian standards and local public-health protocols.

India's Integrated Disease Surveillance Programme (IDSP) supports syndromic, presumptive and laboratory-confirmed surveillance. A real implementation should complement authorized surveillance channels rather than create a parallel, uncoordinated outbreak-reporting authority.

## 5. System architecture
```text
ASHA / ANM / Clinic / Community Volunteer
                 |
       Offline-first reporting UI
       (future PWA / Android / SMS)
                 |
            API Gateway
                 |
       Validation + Data Store
          /             \
 Symptom Reports     Water Observations
          \             /
        Time-window aggregation
                 |
       Risk signal / ML experiment
                 |
       District & block dashboard
                 |
       Human review by authorized
       public-health officials
                 |
     Existing response / surveillance
        procedures (e.g. IDSP/IHIP)
```

## 6. Data requirements
### 6.1 Symptom surveillance
Recommended minimum fields:
- village or approved administrative code
- report date and time
- symptom categories using a locally approved case definition
- aggregate count (avoid names where possible)
- reporting channel and reporter role
- age band only if justified and privacy-reviewed
- data-quality flag and correction history

The prototype uses generic symptom tags. They are not case definitions and must not be used to diagnose a disease.

### 6.2 Water-quality monitoring
Potential fields:
- water source ID and source type
- sampling timestamp and GPS only where appropriate and consented
- pH, turbidity, TDS and test result fields
- test method, kit/device ID, calibration date and operator
- units, quality-control status and laboratory confirmation reference

A pH, turbidity or TDS reading alone cannot establish microbiological safety. Microbiological indicators and appropriate laboratory methods are needed. The prototype's coliform flag is only a user-entered observation, not a sensor-derived pathogen identification.

### 6.3 Contextual data
Potential contextual features include rainfall, flood events, season, water-source interruptions, sanitation incidents and population denominators. These require authoritative, time-aligned data and documentation of spatial resolution.

## 7. Analytics methodology
### Stage A — data quality
Validate permitted values, units, missingness, duplicates, date order, source provenance and sensor calibration. Track missing observations explicitly; absence of reports must never be interpreted as absence of illness.

### Stage B — descriptive surveillance
Aggregate report counts by village and time window. Normalize by population only where reliable denominators exist. Compare current values with local historical baselines and account for reporting volume.

### Stage C — anomaly detection and forecasting
Begin with interpretable baselines:
- rolling averages and seasonal baselines
- control charts or robust z-scores
- Poisson/negative-binomial count models where assumptions fit
- logistic regression or gradient-boosted trees for labelled outcomes

Only consider LSTM, temporal convolution, graph neural networks or spatial-temporal models when the volume, quality and geographic coverage of longitudinal labelled data justify them. Complex models cannot compensate for weak labels or biased surveillance.

### Stage D — multimodal/environmental fusion
Combine clinical/syndromic and environmental features only after aligning location, timestamps and uncertainty. Keep feature provenance and expose which observations contributed to each signal.

### Stage E — human review
Signals should enter a review queue. An authorized health professional determines whether verification, water sampling, community communication or other action is appropriate.

## 8. Prototype risk score
The included API uses a deliberately simple rule-based index from 0 to 100. It adds points for recent reported case volume and selected water-observation flags. The thresholds are arbitrary demonstration values, not public-health thresholds, and are not calibrated to incidence, population, seasonality or laboratory-confirmed outcomes. The dashboard labels results as LOW/MODERATE/HIGH only to exercise the interface. Do not use this score in field decisions.

## 9. Model development plan
The included training script generates artificial data from a toy mathematical rule and trains a Random Forest pipeline. This demonstrates code structure only. It is not trained on real epidemiological data and its metrics have no public-health meaning.

For a research-grade model:
1. Obtain approved, de-identified, representative data through authorized health partners.
2. Define the target outcome with epidemiologists (e.g. verified outbreak signal within a defined horizon).
3. Split by geography and time, not random rows alone, to reduce leakage.
4. Compare naive seasonal baseline, statistical model and ML models.
5. Report sensitivity/recall, precision, specificity, false alerts per village-week, lead time, calibration and subgroup performance.
6. Quantify uncertainty and assess missing-data robustness.
7. Conduct external validation in a separate district/state before any operational trial.

## 10. Evaluation plan
| Dimension | Suggested measure | Why it matters |
|---|---|---|
| Outbreak signal detection | Sensitivity/recall | Avoid missing potential events |
| Alert quality | Precision and false alerts per village-week | Avoid alert fatigue |
| Timeliness | Detection lead time | Potential response window |
| Probability quality | Brier score / calibration curve | Trustworthy risk estimates |
| Data quality | Missingness, duplicate rate, reporting delay | Operational reliability |
| Equity | Performance by geography/language/connectivity | Avoid excluding remote communities |
| System performance | API latency, uptime, offline sync success | Field feasibility |
| Usability | Task completion, reporting time, user feedback | Community adoption |

Do not claim a model is accurate without a defined test set, baseline, confidence intervals and external validation.

## 11. Privacy, security and ethics
- Collect the minimum information required; prefer aggregate counts.
- Do not store patient names, phone numbers or exact addresses in the demo.
- Use informed consent and local-language explanations for any real data collection.
- Apply role-based access, encryption in transit and at rest, audit logs and retention limits.
- Restrict village-level or small-cell displays that could re-identify individuals.
- Do not publish identifiable or sensitive health data to GitHub.
- Complete institutional ethics, legal and public-health approvals before research involving people or real health records.

## 12. Deployment considerations for rural Northeast India
- Offline-first forms with encrypted local queue and reliable synchronization.
- Low-bandwidth API payloads and SMS/IVR fallback where authorized.
- Local language support validated by native speakers and community health workers.
- Solar/battery-aware sensor nodes and documented maintenance/calibration.
- Clear source metadata, timestamp synchronization and data-quality status.
- Training and escalation procedures for ASHA/ANM/clinic users.
- GIS only with verified coordinates and access controls.

## 13. Limitations
This repository is a working software prototype, not a field-ready surveillance platform. It uses synthetic records, in-memory storage and heuristic risk scoring. It does not integrate a real SMS gateway, sensor hardware, GIS maps, official surveillance APIs or a validated ML model. It has no authentication/authorization layer and must not be exposed publicly as a production health service.

## 14. Future research
- Offline-first PWA/Android client and encrypted synchronization.
- SMS/IVR reporting gateway with consent and language support.
- Sensor integration using MQTT and calibration metadata.
- Spatial-temporal modelling only after suitable data access and validation.
- Explainability and uncertainty display for all model-generated signals.
- Interoperability with approved government surveillance systems.
- Prospective pilot study with ethics approval and public-health partner oversight.

## 15. References and resources
1. Smart India Hackathon 2025 problem statement catalogue, SIH25001: https://www.driems.ac.in/wp-content/uploads/2025/09/Smart-India-Hackathon_PROBLEM-STATEMENTS.pdf
2. SIH 2025 problem statement archive: https://sih2025probelmstatement.vercel.app/
3. National Centre for Disease Control, Integrated Disease Surveillance Programme: https://ncdc.mohfw.gov.in/includes/About/CentresAndDivision/IDSP.php
4. WHO, Guidelines for Drinking-water Quality (2026 edition): https://www.who.int/publications/i/item/9789240121225
5. WHO/UNICEF Joint Monitoring Programme: https://washdata.org/

## 16. Conclusion
NeerRaksha demonstrates how community symptom reporting and water observations can be organized into an explainable review workflow. Its primary contribution at this stage is an end-to-end prototype and a transparent research plan. The next scientific step is not to make the score look more sophisticated; it is to secure ethically approved, representative data, define a public-health outcome with domain experts, compare against simple baselines and validate performance across time and geography.
