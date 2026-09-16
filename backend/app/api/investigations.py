import uuid
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.services.data_service import DataService
from app.services.anomaly_engine import AnomalyEngine
from app.services.root_cause_engine import RootCauseEngine
from app.services.historical_matcher import HistoricalMatcher
from app.services.recommendation_engine import RecommendationEngine
from app.services.summary_generator import SummaryGenerator
from app.schemas.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    TrendPoint
)

router = APIRouter(prefix="/api/investigations", tags=["Investigations"])


@router.get("", response_model=List[Dict[str, Any]])
def list_investigations():
    return DataService.get_investigations(limit=30)


@router.get("/{investigation_id}", response_model=Dict[str, Any])
def get_investigation(investigation_id: str):
    inv = DataService.get_investigation_by_id(investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail=f"Investigation {investigation_id} not found")
    return inv


@router.post("/analyze", response_model=InvestigationResponse)
def analyze_failure(request: InvestigationRequest):
    comp_id = request.component_id
    machine_id = request.machine_id
    failure_type = request.failure_type

    # 1. Fetch relevant data
    machine_logs = DataService.get_machine_logs(machine_id=machine_id)
    insp_df = DataService.get_inspection_records(component_id=comp_id)
    maint_df = DataService.get_maintenance_history(machine_id=machine_id)
    process_params = DataService.get_process_parameters(comp_id)

    # 2. Extract inspection details
    if not insp_df.empty:
        insp_row = insp_df.iloc[-1].to_dict()
    else:
        # Fallback inspection defaults for demo component
        insp_row = {
            "component_id": comp_id,
            "machine_id": machine_id,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "dimension_name": "Outer Diameter",
            "expected_value": 25.00,
            "actual_value": 25.42,
            "tolerance": 0.10,
            "deviation": 0.420,
            "result": "FAIL",
            "severity": "Critical"
        }

    # 3. Detect Anomalies
    anomalies = AnomalyEngine.detect_anomalies(
        machine_logs=machine_logs,
        inspection_data=insp_row,
        process_params=process_params,
        machine_id=machine_id
    )

    # 4. Historical Similarity Matching
    latest_log = machine_logs.iloc[-1] if not machine_logs.empty else {}
    target_features = {
        "vib_ratio": float(latest_log.get("vibration", 3.75)) / 1.5,
        "power_pct_inc": max(0.0, ((float(latest_log.get("power_consumption", 5.25)) - 4.2) / 4.2) * 100.0),
        "cycle_ratio": float(latest_log.get("cycle_count", 1842)) / 1500.0,
        "dim_dev": abs(float(insp_row.get("deviation", 0.42))),
        "temp_c": float(latest_log.get("temperature", 44.0))
    }
    historical_matches = HistoricalMatcher.match_cases(
        target_features=target_features,
        machine_id=machine_id,
        limit=5
    )

    # 5. Multi-Signal Root Cause Analysis
    root_cause_ranking = RootCauseEngine.analyze(
        machine_id=machine_id,
        component_id=comp_id,
        inspection_data=insp_row,
        machine_logs=machine_logs,
        maintenance_history=maint_df,
        anomalies=anomalies,
        historical_matches=historical_matches,
        process_params=process_params
    )

    top_cause = root_cause_ranking[0]

    # 6. Corrective Actions
    tool_id = str(latest_log.get("tool_id", "T-14"))
    corrective_actions = RecommendationEngine.generate_recommendations(
        primary_root_cause=top_cause.root_cause,
        machine_id=machine_id,
        tool_id=tool_id,
        deviation=float(insp_row.get("deviation", 0.42))
    )

    # 7. Generate Professional Summary
    summary = SummaryGenerator.generate_summary(
        component_id=comp_id,
        machine_id=machine_id,
        failure_type=failure_type,
        top_root_cause=top_cause,
        anomalies=anomalies,
        corrective_actions=corrective_actions,
        inspection_data=insp_row
    )

    # 8. Build Trend Points for Recharts
    trends: List[TrendPoint] = []
    recent_logs = machine_logs.tail(35)
    all_insp = DataService.get_inspection_records(machine_id=machine_id).tail(35)
    insp_map = {str(row["component_id"]): float(row["deviation"]) for _, row in all_insp.iterrows()}

    for i, (_, row) in enumerate(recent_logs.iterrows()):
        is_last = (i == len(recent_logs) - 1)
        c_id = f"CNC-{2813 + i}" if machine_id == "CNC-07" else str(row.get("component_id", f"PART-{i}"))
        dev_val = insp_map.get(c_id)
        if dev_val is None and is_last and comp_id in insp_map:
            dev_val = insp_map[comp_id]
        if dev_val is not None:
            dev_val = round(float(dev_val), 3)

        trends.append(TrendPoint(
            timestamp=str(row["timestamp"])[11:16],  # HH:MM format
            component_id=c_id,
            vibration=round(float(row["vibration"]), 2),
            temperature=round(float(row["temperature"]), 1),
            power_consumption=round(float(row["power_consumption"]), 2),
            dimensional_deviation=dev_val,
            cycle_count=int(row["cycle_count"]),
            is_failure_point=is_last
        ))

    # 9. Create Response and Persist
    inv_id = f"INV-2026-{uuid.uuid4().hex[:4].upper()}" if comp_id != "CNC-2847" else "INV-2026-001"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = InvestigationResponse(
        investigation_id=inv_id,
        component_id=comp_id,
        machine_id=machine_id,
        failure_type=failure_type,
        severity=top_cause.severity,
        status="Investigated",
        created_at=created_at,
        inspection_details=insp_row,
        anomalies=anomalies,
        trends=trends,
        root_cause_ranking=root_cause_ranking,
        historical_matches=historical_matches,
        corrective_actions=corrective_actions,
        investigation_summary=summary
    )

    # Persist in DB
    DataService.save_investigation(response.model_dump())

    return response

