import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from app.schemas.investigation import AnomalyItem

# Baseline nominal specifications
NOMINAL_RANGES = {
    "vibration": {"min": 1.0, "max": 2.0, "unit": "mm/s", "name": "Spindle Vibration"},
    "power_consumption": {"min": 3.8, "max": 4.6, "unit": "kW", "name": "Power Consumption"},
    "temperature": {"min": 35.0, "max": 42.0, "unit": "°C", "name": "Machine Temperature"},
    "spindle_speed": {"min": 5800, "max": 6200, "unit": "RPM", "name": "Spindle Speed"},
    "feed_rate": {"min": 1150, "max": 1250, "unit": "mm/min", "name": "Feed Rate"},
    "coolant_temperature": {"min": 19.0, "max": 23.0, "unit": "°C", "name": "Coolant Temperature"},
    "cycle_count": {"max_limit": 1500, "unit": "cycles", "name": "Tool Cycle Count"}
}


class AnomalyEngine:
    @staticmethod
    def detect_anomalies(
        machine_logs: pd.DataFrame,
        inspection_data: Optional[Dict[str, Any]] = None,
        process_params: Optional[Dict[str, Any]] = None,
        machine_id: str = "CNC-07"
    ) -> List[AnomalyItem]:
        anomalies: List[AnomalyItem] = []

        if machine_logs.empty:
            return anomalies

        latest_log = machine_logs.iloc[-1]
        ts = str(latest_log.get("timestamp", ""))

        # 1. Vibration Anomaly
        vib = float(latest_log.get("vibration", 1.4))
        vib_cfg = NOMINAL_RANGES["vibration"]
        if vib > vib_cfg["max"]:
            dev_pct = round(((vib - vib_cfg["max"]) / vib_cfg["max"]) * 100, 1)
            sev = "Critical" if vib >= 3.0 else "Warning"
            anomalies.append(AnomalyItem(
                parameter="Spindle Vibration",
                normal_range=f"{vib_cfg['min']} - {vib_cfg['max']} {vib_cfg['unit']}",
                actual_value=round(vib, 2),
                deviation_pct=dev_pct,
                severity=sev,
                timestamp=ts,
                machine_id=machine_id,
                explanation=f"Spindle vibration ({vib:.2f} mm/s) exceeds maximum tolerance of {vib_cfg['max']} mm/s by +{dev_pct}%. Dynamic imbalance or excessive cutting chatter detected."
            ))

        # 2. Power Consumption Anomaly
        power = float(latest_log.get("power_consumption", 4.2))
        power_cfg = NOMINAL_RANGES["power_consumption"]
        if power > power_cfg["max"]:
            dev_pct = round(((power - power_cfg["max"]) / power_cfg["max"]) * 100, 1)
            sev = "Critical" if power >= 5.0 else "Warning"
            anomalies.append(AnomalyItem(
                parameter="Power Consumption",
                normal_range=f"{power_cfg['min']} - {power_cfg['max']} {power_cfg['unit']}",
                actual_value=round(power, 2),
                deviation_pct=dev_pct,
                severity=sev,
                timestamp=ts,
                machine_id=machine_id,
                explanation=f"Spindle motor load ({power:.2f} kW) surged by +{dev_pct}%. Elevated cutting resistance indicates severe tool flank wear or chip clogging."
            ))

        # 3. Machine Temperature
        temp = float(latest_log.get("temperature", 38.0))
        temp_cfg = NOMINAL_RANGES["temperature"]
        if temp > temp_cfg["max"]:
            dev_pct = round(((temp - temp_cfg["max"]) / temp_cfg["max"]) * 100, 1)
            sev = "Critical" if temp >= 48.0 else "Warning"
            anomalies.append(AnomalyItem(
                parameter="Machine Temperature",
                normal_range=f"{temp_cfg['min']} - {temp_cfg['max']} {temp_cfg['unit']}",
                actual_value=round(temp, 2),
                deviation_pct=dev_pct,
                severity=sev,
                timestamp=ts,
                machine_id=machine_id,
                explanation=f"Machine thermal telemetry is elevated ({temp:.1f} °C vs max {temp_cfg['max']} °C). Potential thermal spindle expansion."
            ))

        # 4. Tool Cycle Count / Tool Usage
        tool_id = str(latest_log.get("tool_id", "T-14"))
        cycles = int(latest_log.get("cycle_count", 0))
        max_rec = 1500  # standard limit for End Mill
        if cycles > max_rec:
            dev_pct = round(((cycles - max_rec) / max_rec) * 100, 1)
            sev = "Critical" if cycles >= 1750 else "Warning"
            anomalies.append(AnomalyItem(
                parameter=f"Tool Life ({tool_id})",
                normal_range=f"≤ {max_rec} cycles",
                actual_value=float(cycles),
                deviation_pct=dev_pct,
                severity=sev,
                timestamp=ts,
                machine_id=machine_id,
                explanation=f"Cutting tool {tool_id} has accumulated {cycles} machining cycles, exceeding the manufacturer replacement limit of {max_rec} cycles by +{dev_pct}%."
            ))

        # 5. Dimensional Inspection Deviation
        if inspection_data:
            dev = float(inspection_data.get("deviation", 0.0))
            tol = float(inspection_data.get("tolerance", 0.10))
            nom = float(inspection_data.get("expected_value", 25.00))
            actual_dim = float(inspection_data.get("actual_value", 25.00))
            if abs(dev) > tol:
                dev_pct = round((abs(dev) / tol) * 100, 1)
                sev = "Critical" if abs(dev) >= tol * 2 else "Warning"
                anomalies.append(AnomalyItem(
                    parameter="Dimensional Deviation",
                    normal_range=f"±{tol:.2f} mm (24.90 - 25.10 mm)",
                    actual_value=round(actual_dim, 3),
                    deviation_pct=dev_pct,
                    severity=sev,
                    timestamp=ts,
                    machine_id=machine_id,
                    explanation=f"Outer diameter measured {actual_dim:.3f} mm with a deviation of +{dev:.3f} mm, breaching upper tolerance limit (+{tol:.2f} mm)."
                ))

        # 6. Coolant Temperature Check
        if process_params:
            coolant = float(process_params.get("coolant_temperature", 21.0))
            c_cfg = NOMINAL_RANGES["coolant_temperature"]
            if coolant > c_cfg["max"] or coolant < c_cfg["min"]:
                dev_pct = round(((coolant - c_cfg["max"]) / c_cfg["max"]) * 100, 1)
                anomalies.append(AnomalyItem(
                    parameter="Coolant Temperature",
                    normal_range=f"{c_cfg['min']} - {c_cfg['max']} {c_cfg['unit']}",
                    actual_value=round(coolant, 1),
                    deviation_pct=dev_pct,
                    severity="Warning",
                    timestamp=ts,
                    machine_id=machine_id,
                    explanation=f"Coolant delivery temperature ({coolant:.1f} °C) is outside optimum operating window."
                ))

        return anomalies
