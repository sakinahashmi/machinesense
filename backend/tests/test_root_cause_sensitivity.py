import pandas as pd
import pytest
from app.services.root_cause_engine import RootCauseEngine
from app.services.anomaly_engine import AnomalyEngine
from app.services.historical_matcher import HistoricalMatcher
from app.services.data_service import DataService


def test_baseline_cnc2847_ranking():
    """Verify Tool Wear is dynamically ranked #1 for CNC-2847 on CNC-07."""
    logs = DataService.get_machine_logs("CNC-07")
    insp = DataService.get_inspection_records("CNC-2847").iloc[0].to_dict()
    maint = DataService.get_maintenance_history("CNC-07")
    params = DataService.get_process_parameters("CNC-2847")

    anomalies = AnomalyEngine.detect_anomalies(logs, insp, params, "CNC-07")
    hist_matches = HistoricalMatcher.match_cases({
        "vib_ratio": 3.725 / 1.5,
        "power_pct_inc": ((5.31 - 4.2) / 4.2) * 100.0,
        "cycle_ratio": 1832 / 1500.0,
        "dim_dev": 0.42,
        "temp_c": 44.14
    }, machine_id="CNC-07", limit=5)

    rankings = RootCauseEngine.analyze(
        machine_id="CNC-07",
        component_id="CNC-2847",
        inspection_data=insp,
        machine_logs=logs,
        maintenance_history=maint,
        anomalies=anomalies,
        historical_matches=hist_matches,
        process_params=params
    )

    assert len(rankings) >= 5
    assert rankings[0].root_cause == "Tool Wear"
    assert rankings[0].confidence >= 80.0
    assert rankings[0].severity == "Critical"
    assert rankings[1].root_cause == "Excessive Vibration"


def test_sensitivity_shift_to_feed_rate():
    """
    Sensitivity Test:
    When tool cycle count is low (300 cycles) and feed rate deviates significantly (1650 mm/min),
    the ranking MUST dynamically switch: 'Incorrect Feed Rate' becomes #1.
    """
    # Synthetic test log with low tool cycles and normal power
    test_logs = pd.DataFrame([{
        "timestamp": "2026-09-15 14:00:00",
        "machine_id": "CNC-07",
        "spindle_speed": 6000,
        "feed_rate": 1650,
        "vibration": 1.4,
        "temperature": 38.0,
        "power_consumption": 4.1,
        "tool_id": "T-02",
        "cycle_count": 280,
        "machine_status": "Warning"
    }])

    insp = {
        "component_id": "TEST-PART-01",
        "machine_id": "CNC-07",
        "expected_value": 25.0,
        "actual_value": 25.35,
        "tolerance": 0.10,
        "deviation": 0.35,
        "result": "FAIL"
    }

    test_params = {
        "component_id": "TEST-PART-01",
        "feed_rate": 1650,  # 450 mm/min over baseline
        "coolant_temperature": 21.0
    }

    # No overdue maintenance for T-02
    test_maint = pd.DataFrame([{
        "maintenance_id": "MNT-9999",
        "machine_id": "CNC-07",
        "tool_id": "T-02",
        "date": "2026-09-10",
        "status": "Completed"
    }])

    anomalies = AnomalyEngine.detect_anomalies(test_logs, insp, test_params, "CNC-07")
    hist_matches = HistoricalMatcher.match_cases({
        "vib_ratio": 1.4 / 1.5,
        "power_pct_inc": 0.0,
        "cycle_ratio": 280 / 1500.0,
        "dim_dev": 0.35,
        "temp_c": 38.0
    }, machine_id="CNC-07", limit=5)

    rankings = RootCauseEngine.analyze(
        machine_id="CNC-07",
        component_id="TEST-PART-01",
        inspection_data=insp,
        machine_logs=test_logs,
        maintenance_history=test_maint,
        anomalies=anomalies,
        historical_matches=hist_matches,
        process_params=test_params
    )

    assert rankings[0].root_cause == "Incorrect Feed Rate"
    assert rankings[0].confidence >= 65.0
    # Tool Wear should drop significantly
    tw_rank = next(r for r in rankings if r.root_cause == "Tool Wear")
    assert tw_rank.confidence < 30.0


def test_sensitivity_shift_to_vibration():
    """
    Sensitivity Test:
    When dynamic vibration spikes (4.2 mm/s) with nominal feed rate and tool cycles,
    'Excessive Vibration' dynamically becomes the top root cause.
    """
    test_logs = pd.DataFrame([{
        "timestamp": "2026-09-15 14:00:00",
        "machine_id": "CNC-07",
        "spindle_speed": 6000,
        "feed_rate": 1200,
        "vibration": 4.25,  # extreme chatter
        "temperature": 39.0,
        "power_consumption": 4.3,
        "tool_id": "T-05",
        "cycle_count": 410,
        "machine_status": "Critical"
    }])

    insp = {
        "component_id": "TEST-PART-02",
        "machine_id": "CNC-07",
        "expected_value": 25.0,
        "actual_value": 25.28,
        "tolerance": 0.10,
        "deviation": 0.28,
        "result": "FAIL"
    }

    test_params = {
        "component_id": "TEST-PART-02",
        "feed_rate": 1200,
        "coolant_temperature": 21.0
    }

    test_maint = pd.DataFrame([{
        "maintenance_id": "MNT-9999",
        "machine_id": "CNC-07",
        "tool_id": "T-05",
        "date": "2026-09-10",
        "status": "Completed"
    }])

    anomalies = AnomalyEngine.detect_anomalies(test_logs, insp, test_params, "CNC-07")
    hist_matches = HistoricalMatcher.match_cases({
        "vib_ratio": 4.25 / 1.5,
        "power_pct_inc": 0.0,
        "cycle_ratio": 410 / 1500.0,
        "dim_dev": 0.28,
        "temp_c": 39.0
    }, machine_id="CNC-07", limit=5)

    rankings = RootCauseEngine.analyze(
        machine_id="CNC-07",
        component_id="TEST-PART-02",
        inspection_data=insp,
        machine_logs=test_logs,
        maintenance_history=test_maint,
        anomalies=anomalies,
        historical_matches=hist_matches,
        process_params=test_params
    )

    assert rankings[0].root_cause == "Excessive Vibration"
    assert rankings[0].confidence >= 70.0
    tw_rank = next(r for r in rankings if r.root_cause == "Tool Wear")
    assert tw_rank.confidence < 30.0

