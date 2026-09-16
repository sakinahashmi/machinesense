from typing import List, Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="/api/insights", tags=["AI Insights"])


@router.get("", response_model=Dict[str, Any])
def get_ai_insights():
    fleet_patterns = [
        {
            "id": "PAT-01",
            "category": "Tool Degradation Pattern",
            "severity": "Critical",
            "confidence": 94.8,
            "title": "Tool Wear Accelerated Beyond 1,450 Cycles",
            "insight": "Statistical analysis of 240 recent machining runs confirms that Solid Carbide End Mills show exponential flank wear once cycle count exceeds 1,450 cycles. Dimensional deviations rise by +340% between 1,500 and 1,850 cycles.",
            "impacted_machines": ["CNC-07", "CNC-04", "CNC-01"],
            "impacted_tools": ["T-14", "T-09", "T-11"],
            "recommended_action": "Implement automatic tool change lock at 1,400 cycles across all 3-axis and 5-axis machines."
        },
        {
            "id": "PAT-02",
            "category": "Vibration & Surface Quality",
            "severity": "Warning",
            "confidence": 88.2,
            "title": "5-Axis Harmonic Chatter Correlation",
            "insight": "Machine CNC-03 experienced 4 minor surface roughness flags during high feed-rate roughing (feed > 1250 mm/min). Sensor telemetry correlates vibration spikes with hydraulic fixture pressure dips.",
            "impacted_machines": ["CNC-03"],
            "impacted_tools": ["T-07"],
            "recommended_action": "Service hydraulic clamping pump pressure regulator on CNC-03."
        },
        {
            "id": "PAT-03",
            "category": "Thermal Growth Dynamics",
            "severity": "Info",
            "confidence": 82.5,
            "title": "Morning Shift Thermal Stabilization Lag",
            "insight": "First 3 components machined on CNC-06 during morning shift (06:00 - 07:00) display slight dimensional undersize (-0.04 mm) due to cold spindle warmup lag.",
            "impacted_machines": ["CNC-06"],
            "impacted_tools": ["All"],
            "recommended_action": "Enforce 15-minute automated spindle warmup cycle before morning production runs."
        }
    ]

    anomaly_distribution = [
        {"name": "Tool Wear", "count": 28, "percentage": 46.7, "color": "#f59e0b"},
        {"name": "Excessive Vibration", "count": 14, "percentage": 23.3, "color": "#ef4444"},
        {"name": "Incorrect Feed/Speed", "count": 8, "percentage": 13.3, "color": "#3b82f6"},
        {"name": "Coolant Temp Variation", "count": 6, "percentage": 10.0, "color": "#06b6d4"},
        {"name": "Calibration Drift", "count": 4, "percentage": 6.7, "color": "#10b981"},
    ]

    return {
        "fleet_patterns": fleet_patterns,
        "anomaly_distribution": anomaly_distribution,
        "total_patterns_detected": len(fleet_patterns)
    }
