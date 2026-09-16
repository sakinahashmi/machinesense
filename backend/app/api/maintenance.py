from typing import List, Dict, Any
from fastapi import APIRouter
from app.services.data_service import DataService

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])


@router.get("", response_model=Dict[str, Any])
def get_maintenance_overview():
    maint_df = DataService.get_maintenance_history()
    records = maint_df.to_dict(orient="records") if not maint_df.empty else []

    overdue_alerts = [
        {
            "alert_id": "ALT-MNT-01",
            "machine_id": "CNC-07",
            "tool_id": "T-14",
            "type": "Tool Replacement Overdue",
            "severity": "Critical",
            "current_cycles": 1842,
            "max_threshold": 1500,
            "overdue_by_cycles": 342,
            "last_replaced": "21 days ago",
            "impact": "Dimensional out-of-tolerance (Outer Diameter +0.42mm)",
            "action_required": "Replace carbide end mill and recalibrate tool offset immediately."
        },
        {
            "alert_id": "ALT-MNT-02",
            "machine_id": "CNC-03",
            "tool_id": "T-07",
            "type": "Spindle Vibration Inspection Overdue",
            "severity": "Warning",
            "current_cycles": 1380,
            "max_threshold": 1400,
            "overdue_by_cycles": 0,
            "last_replaced": "14 days ago",
            "impact": "Harmonic chatter resonance on 5-axis rotary table",
            "action_required": "Perform hydraulic chuck cylinder pressure test."
        }
    ]

    tool_wear_tracker = [
        {"tool_id": "T-14", "machine_id": "CNC-07", "type": "End Mill", "cycles": 1842, "max_cycles": 1500, "wear_pct": 122.8, "status": "Critical"},
        {"tool_id": "T-07", "machine_id": "CNC-03", "type": "Face Mill", "cycles": 1180, "max_cycles": 1200, "wear_pct": 98.3, "status": "Warning"},
        {"tool_id": "T-03", "machine_id": "CNC-01", "type": "Drill", "cycles": 890, "max_cycles": 1800, "wear_pct": 49.4, "status": "Nominal"},
        {"tool_id": "T-09", "machine_id": "CNC-04", "type": "Boring Bar", "cycles": 720, "max_cycles": 1400, "wear_pct": 51.4, "status": "Nominal"},
        {"tool_id": "T-11", "machine_id": "CNC-02", "type": "End Mill", "cycles": 640, "max_cycles": 1500, "wear_pct": 42.7, "status": "Nominal"},
        {"tool_id": "T-18", "machine_id": "CNC-06", "type": "Reamer", "cycles": 510, "max_cycles": 1600, "wear_pct": 31.9, "status": "Nominal"},
    ]

    return {
        "overdue_alerts": overdue_alerts,
        "tool_wear_tracker": tool_wear_tracker,
        "recent_history": records[:25],
        "total_maintenance_records": len(records)
    }
