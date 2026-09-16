from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class MachineSummary(BaseModel):
    machine_id: str
    model: str
    axes: int
    status: str  # Nominal, Warning, Critical
    health_score: int  # 0 - 100
    current_tool: str
    vibration: float
    temperature: float
    power_consumption: float
    last_maintenance: str
    active_issues: List[str]
    cycle_utilization_pct: float


class MachineTelemetryPoint(BaseModel):
    timestamp: str
    vibration: float
    temperature: float
    power_consumption: float
    spindle_speed: int
    feed_rate: int
    cycle_count: int
    status: str


class MachineDetail(BaseModel):
    machine_id: str
    model: str
    axes: int
    status: str
    health_score: int
    current_tool: str
    nominal_power: float
    nominal_vib: float
    nominal_temp: float
    latest_telemetry: MachineTelemetryPoint
    recent_telemetry: List[MachineTelemetryPoint]
    recent_inspections: List[Dict[str, Any]]
    recent_maintenance: List[Dict[str, Any]]
    active_alerts: List[str]
