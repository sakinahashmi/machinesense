import pandas as pd
from app.services.anomaly_engine import AnomalyEngine
from app.services.root_cause_engine import RootCauseEngine
from app.services.historical_matcher import HistoricalMatcher
from app.database import init_db


def test_flagship_demo_root_cause_is_tool_wear():
    # Ensure database/CSVs are initialized
    init_db()

    logs = pd.DataFrame([{
        "timestamp": "2026-09-15 14:00:00",
        "machine_id": "CNC-07",
        "spindle_speed": 6000,
        "feed_rate": 1200,
        "vibration": 3.75,
        "temperature": 44.0,
        "power_consumption": 5.25,
        "tool_id": "T-14",
        "cycle_count": 1842,
        "machine_status": "Critical"
    }])

    insp = {
        "component_id": "CNC-2847",
        "machine_id": "CNC-07",
        "expected_value": 25.00,
        "actual_value": 25.42,
        "tolerance": 0.10,
        "deviation": 0.420
    }

    maint = pd.DataFrame([{
        "maintenance_id": "MNT-1019",
        "machine_id": "CNC-07",
        "tool_id": "T-14",
        "date": "2026-09-13",
        "maintenance_type": "Tool Replacement",
        "cycle_count": 1842,
        "technician_note": "OVERDUE",
        "status": "Overdue"
    }])

    anomalies = AnomalyEngine.detect_anomalies(logs, insp, machine_id="CNC-07")
    hist_matches = HistoricalMatcher.match_cases(
        {"vib_ratio": 2.5, "power_pct_inc": 18.4, "cycle_ratio": 1.22, "dim_dev": 0.42, "temp_c": 44.0},
        machine_id="CNC-07"
    )

    ranking = RootCauseEngine.analyze(
        machine_id="CNC-07",
        component_id="CNC-2847",
        inspection_data=insp,
        machine_logs=logs,
        maintenance_history=maint,
        anomalies=anomalies,
        historical_matches=hist_matches
    )

    # Validate #1 ranked root cause is Tool Wear
    top_cause = ranking[0]
    assert top_cause.root_cause == "Tool Wear"
    assert top_cause.confidence >= 80.0
    assert top_cause.confidence_level == "HIGH CONFIDENCE"
    assert len(top_cause.evidence) >= 3

    # Check that Excessive Vibration is ranked second
    assert ranking[1].root_cause == "Excessive Vibration"
