# MachineSense
AI-Assisted Industrial Root Cause Analysis & Diagnostic Intelligence

---

## Overview

In precision manufacturing environments, diagnosing why a machined component failed quality inspection is often a complex, manual task. Quality and maintenance engineers must parse disconnected data streams: CNC machine telemetry, CAM process parameters, CMM dimensional inspection reports, maintenance logs, and historical non-conformance archives.

**MachineSense** is an evidence-driven diagnostic platform prototype designed to accelerate this investigation process. When a quality failure occurs (such as a dimensional out-of-tolerance defect on a CNC milling center), MachineSense correlates multi-source plant data to identify, score, and rank probable root-cause hypotheses. For each hypothesis, the platform presents supporting sensor evidence, affected engineering parameters, historical failure precedents, and actionable containment and preventive recommendations.

> **Note on Diagnostics:** MachineSense does not claim autonomous decision-making or definitive causal proof. The root-cause scoring engine produces prioritized, evidence-backed hypotheses to support quality engineers in their investigation workflow.

---

## Problem Statement

Modern manufacturing execution systems (MES) and quality control pipelines generate vast volumes of operational data, yet these systems typically operate in silos:

* **Machine Telemetry:** High-frequency spindle vibration, motor power draw, spindle RPM, and thermal data are captured by machine controllers and condition-monitoring sensors.
* **Process Parameters:** Programmed vs. actual feed rates, spindle overrides, depth of cut, and coolant delivery temperatures reside in CNC controller logs.
* **Quality Inspection:** Coordinate Measuring Machine (CMM) dimensional measurements, tolerance envelopes, and deviation magnitudes are stored in quality management systems (QMS).
* **Maintenance Records:** Tool cycle accumulation, insert replacement history, spindle service logs, and calibration schedules reside in computerized maintenance management systems (CMMS).
* **Historical Failure Cases:** Past non-conformance reports (NCRs) and corrective action archives are often stored in static incident databases.

When a part fails inspection, engineers must manually correlate these disparate records under time pressure. This fragmented workflow can lead to slow root-cause determination, extended machine downtime, recurring scrap production, and inconsistent shift-to-shift diagnosis. MachineSense addresses this challenge by providing an integrated analytical pipeline that correlates cross-source data into transparent, evidence-ranked diagnostic hypotheses.

---

## Key Capabilities

* **Multi-Source Data Correlation:** Ingests and correlates CNC telemetry, process parameters, dimensional inspection records, tool maintenance history, and historical failure archives.
* **Continuous Signal Normalization:** Transforms diverse physical dimensions (cycles, mm/s vibration, kW power draw, mm dimensional deviation) into continuous, non-saturating evidence scores in $[0, 1]$.
* **Multi-Parameter Anomaly Detection:** Identifies operational boundary breaches and parameter surges against nominal machine baselines.
* **Root-Cause Hypothesis Ranking:** Ranks candidate failure modes (e.g., Tool Wear, Excessive Vibration, Incorrect Feed Rate, Coolant Temperature Variation, Calibration Drift) based on weighted evidence aggregation.
* **Explainable Evidence Scoring:** Provides transparent breakdown of supporting signals with verifiable plant metrics and confidence badges.
* **Vectorized Historical Case Similarity:** Measures multi-feature similarity against past incident profiles using weighted distance matching.
* **Corrective & Preventive Action Matrix:** Recommends immediate operational containment actions and long-term preventive engineering measures.
* **Structured Investigation Summaries:** Synthesizes deterministic, physics-of-failure technical narratives for shift handover and audit logs (with optional LLM enhancement).
* **Machine Health & Fleet Telemetry Views:** Displays real-time operational status, health scores, active alerts, and telemetry history across monitored machining centers.
* **Interactive Investigation Workbench:** Offers multi-series synchronized telemetry trend charts with tolerance reference bands and failure point markers.

---

## How It Works

The MachineSense diagnostic pipeline processes manufacturing telemetry through the following stages:

```text
Manufacturing Data (Telemetry, Inspection, Maintenance, Process Parameters, History)
    ↓
Data Service (Relational SQLite schema & indexed querying layer)
    ↓
Signal Normalization (Continuous mathematical mapping into bounded [0, 1] evidence)
    ↓
Anomaly Detection (Statistical deviation & nominal operating envelope evaluation)
    ↓
Historical Case Matching (Vectorized multi-feature similarity against incident database)
    ↓
Root Cause Scoring (Cause-specific weighted evidence aggregation)
    ↓
Recommendation Engine (Categorized immediate & preventive action generation)
    ↓
Investigation Summary (Deterministic physics-of-failure narrative synthesis)
    ↓
Dashboard & REST API (Interactive React interface & JSON service endpoints)
```

### Pipeline Stages

1. **Manufacturing Data Layer:** Ingests machine logs (vibration, power, temperature, cycles), inspection measurements (nominal, actual, deviation, tolerance), process parameters (feed rate, coolant temperature), and maintenance logs.
2. **Data Service:** Provides indexed query interfaces across relational database tables for high-performance retrieval by machine ID, component ID, and timestamp.
3. **Signal Normalization:** Evaluates raw physical values through continuous mathematical functions (logistic wear curves, exponential power/deviation functions) to generate standardized evidence scores between $0.0$ and $1.0$ without premature clipping.
4. **Anomaly Detection:** Flags telemetry parameters that breach standard operating ranges, computing percentage deviations and assigning severity tiers (Nominal, Warning, Critical).
5. **Historical Case Matching:** Computes weighted multi-feature Euclidean distance across vibration ratio, power surge percentage, cycle ratio, dimensional deviation, and temperature to find similar past plant incidents.
6. **Root Cause Scoring:** Combines normalized sensor signals, trend drift slopes, maintenance flags, and historical match scores using cause-specific weighting matrices to calculate candidate evidence scores.
7. **Recommendation Engine:** Maps identified failure modes to verified corrective actions, distinguishing between immediate containment and preventive maintenance actions.
8. **Investigation Summary:** Generates structured technical narratives combining dimensional failure specifics, primary physical failure mechanisms, and required interventions.
9. **Dashboard & REST API:** Serves findings through FastAPI endpoints consumed by a React-based industrial engineering dashboard.

---

## Root Cause Analysis Approach

The core diagnostic engine in MachineSense utilizes a **deterministic, multi-signal mathematical pipeline** rather than relying on an unconstrained large language model (LLM) for the diagnosis. This ensures repeatability, auditability, and explainability in industrial settings.

### Evidence Signals Evaluated

* **Dimensional Deviation ($S_{\text{dim}}$):** Ratio of measured part deviation to drawing tolerance band ($u = |\text{dev}| / \text{tol}$), normalized via exponential saturation curve.
* **Tool Cycle Accumulation ($S_{\text{cycles}}$):** Tool cycle count relative to rated replacement limit ($r = \text{cycles} / \text{max\_cycles}$), evaluated through a continuous logistic lifecycle function.
* **Spindle Power Draw ($S_{\text{power}}$):** Cutting torque surge relative to nominal milling baseline ($\Delta P / P_{\text{baseline}}$), modeling increased cutting resistance from blunted edges.
* **Dynamic Vibration ($S_{\text{vib}}$):** Spindle RMS vibration relative to ISO 10816 nominal alert limits ($2.00\text{ mm/s}$), normalized via continuous logistic response.
* **Feed Rate Deviation ($S_{\text{feed}}$):** Programmed feed rate deviation from CAM nominal baseline ($|\text{feed} - \text{nominal}|$).
* **Coolant Temperature ($S_{\text{coolant}}$):** Fluid delivery temperature outside optimal operating window ($19.0\text{--}23.0^\circ\text{C}$).
* **Maintenance Status ($S_{\text{maint}}$):** Overdue status flags and cycle accumulation ratio from CMMS records.
* **Historical Precedent ($S_{\text{hist}}$):** Geometric decaying aggregation of top corroborating historical failure matches.
* **Trend Drift:** Monotonic regression slope of power and vibration signals over preceding consecutive machining cycles.

### Candidate Score Formulation

Candidate root cause scores are computed by weighting relevant normalized evidence components:

$$\text{RawScore}(\text{Cause}) = \sum_{k} w_k \cdot S_k$$

For example, **Tool Wear** combines:
$$\text{RawScore}(\text{Tool Wear}) = 0.30 S_{\text{cycles}} + 0.25 S_{\text{power}} + 0.20 S_{\text{dim}} + 0.15 S_{\text{maint}} + 0.10 S_{\text{hist}}$$

The raw score is mapped into a percentage $[5.0\%, 99.0\%]$ for display.

> **Important Semantic Definition:** The resulting score is formally termed an **Evidence Score**. The evidence score represents the strength of the available supporting signals in the prototype. It is not a calibrated probability of causality.

---

## Example Investigation: CNC-2847

The prototype includes a reference investigation scenario based on component `CNC-2847` machined on 5-axis center `CNC-07`:

### Inspection & Telemetry Inputs

* **Component:** `CNC-2847` (Outer Diameter specification: $25.00 \pm 0.10\text{ mm}$)
* **Inspection Result:** $25.420\text{ mm}$ (Deviation: $+0.420\text{ mm}$, 4.2x tolerance limit, **FAIL**)
* **Machine:** `CNC-07` (Hermle C42 5-Axis Machining Center)
* **Cutting Tool:** `T-14` (Solid Carbide End Mill)
* **Tool Cycles:** $1,832\text{ cycles}$ (Rated threshold: $1,500\text{ cycles}$, $+22.1\%$ overage)
* **Spindle Vibration:** $3.73\text{ mm/s}$ (Nominal limit: $2.00\text{ mm/s}$)
* **Spindle Power:** $5.31\text{ kW}$ ($+26.4\%$ over $4.20\text{ kW}$ baseline)
* **Temperature:** $44.1^\circ\text{C}$ (Nominal: $38.0^\circ\text{C}$)
* **Spindle Speed:** $6,002\text{ RPM}$ (Nominal: $6,000\text{ RPM}$)
* **Feed Rate:** $1,196\text{ mm/min}$ (Nominal: $1,200\text{ mm/min}$)
* **Maintenance Flag:** Maintenance ticket for Tool `T-14` flagged as **OVERDUE**

### Engine Output & Hypothesis Ranking

| Rank | Candidate Root Cause | Evidence Score | Confidence Level | Severity |
| :---: | :--- | :---: | :---: | :---: |
| **#1** | **Tool Wear** | **87.3%** | **HIGH CONFIDENCE** | **Critical** |
| **#2** | Excessive Vibration | 70.1% | MEDIUM-HIGH | Warning |
| **#3** | Machine Calibration Drift | 35.3% | LOW | Info |
| **#4** | Coolant Temperature Variation | 34.6% | LOW | Info |
| **#5** | Incorrect Feed Rate | 26.6% | LOW | Info |

### Key Supporting Evidence Generated
* **Tool Usage:** Tool `T-14` reached 1,832 cycles (normalized wear evidence: `0.832`).
* **Power Anomaly:** Spindle power draw surged $+26.4\%$ to 5.31 kW (normalized cutting force evidence: `0.831`).
* **Dimensional Trend:** $+0.420\text{ mm}$ deviation breaches tolerance envelope (normalized deviation evidence: `0.940`).
* **Maintenance Record:** Work order flagged as overdue (maintenance factor: `0.90`).
* **Historical Corroboration:** Corroborating incident `#CASE-104` matched with weighted similarity score of `0.950`.

### Actions Recommended
* **Immediate Containment:** Lock out machine `CNC-07`, replace End Mill `T-14`, and execute optical tool setter length/diameter recalibration. Quarantine the preceding 15 machined parts for CMM re-inspection.
* **Preventive Measure:** Lower automatic tool-cycle replacement warning threshold from 1,500 to 1,400 cycles in the CNC controller.

---

## Technology Stack

### Frontend
* **Core Framework:** React 18 / Vite
* **Styling:** Vanilla Tailwind CSS (Dark industrial enterprise theme)
* **Visualizations:** Recharts (Multi-series synchronized telemetry trend charts, reference limits, anomaly markers)
* **Icons:** Lucide React
* **Routing:** React Router v6
* **HTTP Client:** Axios

### Backend
* **API Framework:** Python 3.9+ / FastAPI / Uvicorn
* **Data Processing & Modeling:** Pandas, NumPy, Scikit-learn
* **Data Validation:** Pydantic v2
* **Database:** SQLite (Indexed relational tables)
* **Testing:** pytest, HTTPX TestClient

### AI & Analytics Architecture
* **Primary RCA Engine:** 100% deterministic Python analytics, continuous mathematical normalizers, and vectorized similarity scoring.
* **Optional LLM Integration:** Optional LLM-assisted natural language narrative synthesis if an API key is configured.
* **Offline Operation:** The entire core RCA pipeline, scoring engine, anomaly detection, historical matching, and UI function fully offline without external API dependencies.

---

## Project Structure

```text
machinesense/
├── backend/
│   ├── app/
│   │   ├── api/                     # REST API routers (health, dashboard, machines, investigations, etc.)
│   │   ├── models/                  # Database models
│   │   ├── schemas/                 # Pydantic schemas for RCA, telemetry, and KPIs
│   │   ├── services/                # Core analytics, signal normalizers, anomaly & scoring engines
│   │   │   ├── signal_normalizer.py     # Continuous mathematical signal normalization functions
│   │   │   ├── root_cause_engine.py     # Multi-signal evidence scoring engine
│   │   │   ├── anomaly_engine.py        # Telemetry anomaly detection
│   │   │   ├── historical_matcher.py    # Vectorized historical similarity matcher
│   │   │   ├── recommendation_engine.py # Action matrix generator
│   │   │   ├── summary_generator.py     # Technical narrative generator
│   │   │   └── data_service.py          # Relational SQLite querying layer
│   │   ├── config.py                # Application configuration and settings
│   │   ├── database.py              # SQLite database initialization & CSV loaders
│   │   └── main.py                  # FastAPI application entrypoint & lifespan
│   ├── data/                        # Source manufacturing CSV datasets (logs, inspection, maintenance)
│   ├── tests/                       # Pytest test suite (normalization, sensitivity, API, health)
│   ├── pytest.ini                   # Pytest configuration
│   └── requirements.txt             # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── common/                  # Navbar, Sidebar, MetricCard, StatusBadge, LoadingOverlay
│   │   │   ├── dashboard/               # MachineHealthGrid, RecentInvestigationsTable, FleetInsightAlerts
│   │   │   ├── investigation/           # Header, RootCauseRankList, EvidencePanel, TrendCharts, ActionMatrix
│   │   │   └── machines/                # MachineTelemetryModal
│   │   ├── pages/                   # Application views (Dashboard, Investigations, Machines, Maintenance, Insights)
│   │   ├── services/                # API client integration
│   │   ├── App.jsx                  # Application routing & layout
│   │   └── main.jsx                 # Frontend entrypoint
│   ├── package.json                 # Node.js dependencies and scripts
│   ├── vite.config.js               # Vite build configuration
│   └── tailwind.config.js           # Tailwind CSS theme configuration
└── README.md                        # Technical project documentation
```

---

## API Overview

The FastAPI backend exposes the following REST endpoints:

### System & Health
* `GET /` — Service status, application version, and documentation link.
* `GET /health` — Service health status and current UTC timestamp.

### Dashboard & Fleet Overview
* `GET /api/dashboard/overview` — Plant-wide KPIs (First Pass Yield, active investigations, critical alerts), machine health status list, recent investigations, and 7-day rolling pass rate trend.

### Machines & Telemetry
* `GET /api/machines` — Summary list of all monitored CNC machining centers with health scores, operating status, current tooling, and cycle utilization.
* `GET /api/machines/{machine_id}` — Detailed machine view including recent 40-point telemetry history, inspection logs, maintenance records, and active alerts.

### Root Cause Investigations
* `GET /api/investigations` — List of recent investigation records with primary findings and evidence scores.
* `GET /api/investigations/{investigation_id}` — Full investigation report by unique investigation ID.
* `POST /api/investigations/analyze` — Executes the multi-signal RCA pipeline for a specified component ID, machine ID, and failure mode. Returns ranked root-cause hypotheses, supporting evidence items, synchronized trend telemetry, historical matches, corrective actions, and executive summary.

### Maintenance & Tooling
* `GET /api/maintenance` — Tool cycle wear tracker across all active tools, overdue replacement alerts, and recent maintenance event history.

### Historical Knowledge Base
* `GET /api/historical-cases` — Search and filter historical failure records by keyword, machine ID, or root-cause category.
* `GET /api/historical-cases/{case_id}` — Retrieve details of a specific historical incident report.

### Systemic Insights
* `GET /api/insights` — Statistical pattern correlations across fleet telemetry and root-cause frequency distributions.

---

## Running Locally

### Prerequisites
* Python 3.9+ installed
* Node.js 18+ and npm installed

### 1. Backend Setup

1. Open PowerShell or a terminal and navigate to `backend`:
   ```powershell
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```powershell
   pip install -r requirements.txt
   ```

4. Launch the FastAPI development server:
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

5. Verify backend operation:
   * Status: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   * Interactive OpenAPI Documentation (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2. Frontend Setup

1. Open a second terminal and navigate to `frontend`:
   ```powershell
   cd frontend
   ```

2. Install Node dependencies:
   ```powershell
   npm install
   ```

3. Start the Vite development server:
   ```powershell
   npm run dev
   ```

4. Open the application in your browser:
   * Dashboard URL: [http://localhost:5173/](http://localhost:5173/)

---

## Testing

The backend includes an automated test suite executed via `pytest`:

```powershell
cd backend
.\venv\Scripts\pytest.exe tests -v
```

### Test Suite Verification Areas
* **Signal Normalization Tests (`test_signal_normalization.py`):** Validates continuous mathematical properties, monotonicity ($\partial S / \partial x \ge 0$), and asymptotic boundary conditions across tool cycles, vibration, power surges, dimensional deviation, feed rates, coolant temperatures, maintenance states, and decaying historical aggregation.
* **Sensitivity & Dynamic Ranking Tests (`test_root_cause_sensitivity.py`):** Verifies that changing operating conditions correctly shifts diagnostic rankings (e.g., elevated vibration dynamically promotes Excessive Vibration to #1; feed rate override promotes Incorrect Feed Rate to #1).
* **Anomaly Detection Engine Tests (`test_anomaly_engine.py`):** Validates threshold evaluation and severity classification across telemetry streams.
* **Investigation API Integration Tests (`test_investigations_api.py`):** Tests end-to-end payload generation, score consistency, and persistence for `POST /api/investigations/analyze`.
* **Service Health Tests (`test_health.py`):** Verifies system availability and metadata endpoints.

---

## Engineering Assumptions & Limitations

* **Synthetic Prototype Data:** Telemetry streams, maintenance records, and CMM inspection measurements are synthetically generated prototype datasets structured to demonstrate real-world physical correlation patterns.
* **Configured Reference Baselines:** Operating limits (e.g., 1,500 cycle tool life, 2.00 mm/s vibration threshold, 4.20 kW baseline power) are configured reference parameters for this prototype, not universal industry specifications.
* **Evidence Scores vs. Probabilities:** Evidence scores reflect weighted multi-signal corroboration strength within the prototype model. They are not statistically calibrated frequentist or Bayesian probabilities of causality.
* **Hypothesis Generation:** Engine outputs represent prioritized diagnostic hypotheses indicating supporting evidence to guide engineering evaluation, not definitive causal proof.
* **Production Requirements:** Deploying MachineSense in an active production facility would require:
  * Plant-specific baseline calibration across individual machine tool models and materials.
  * Direct integration with production MES, QMS (CMM interfaces), and CMMS (SAP PM / Maximo) systems.
  * Integration with high-frequency industrial IoT protocols (OPC-UA, MTConnect, MQTT).
  * Role-based access control (RBAC), user authentication, and tamper-evident audit logs for regulatory compliance (e.g., ISO 9001 / IATF 16949).
  * Domain-expert review workflows for validating diagnostic outputs before taking corrective actions.

---

## Future Improvements

* **Production Database Migration:** Transition from SQLite to PostgreSQL / TimescaleDB for time-series telemetry scaling.
* **Industrial Protocol Connectors:** Native support for OPC-UA, MQTT, and MTConnect streaming protocols from Fanuc, Siemens Sinumerik, and Heidenhain controllers.
* **Automated CMMS Work Order Dispatch:** Bi-directional API integration to auto-generate tool replacement work orders upon anomaly confirmation.
* **Closed-Loop Offset Compensation:** Integration with CNC controllers to send automated tool wear offset adjustments prior to tolerance breach.
* **Empirical Machine Learning Models:** Training supervised and semi-supervised failure classification models on validated empirical plant datasets.
* **Hybrid Retrieval-Augmented Incident Matching:** Combining dense vector embeddings and BM25 hybrid search for historical failure case retrieval.
* **Security & Governance:** Enterprise OAuth2 / SAML authentication, fine-grained RBAC, and quality audit trails.

---

## License

License to be added.
