import pandas as pd
from app.services.anomaly_engine import AnomalyEngine


def test_vibration_and_power_anomalies():
    # Synthetic logs with elevated vibration & power
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

    anomalies = AnomalyEngine.detect_anomalies(
        machine_logs=logs,
        inspection_data=insp,
        machine_id="CNC-07"
    )

    param_names = [a.parameter for a in anomalies]
    assert any("Vibration" in p for p in param_names)
    assert any("Power" in p for p in param_names)
    assert any("Tool Life" in p for p in param_names)
    assert any("Dimensional" in p for p in param_names)

    # Check that tool life anomaly is Critical
    tool_anomaly = next(a for a in anomalies if "Tool Life" in a.parameter)
    assert tool_anomaly.severity == "Critical"
    assert tool_anomaly.actual_value == 1842.0
