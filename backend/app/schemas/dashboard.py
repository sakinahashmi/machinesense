from typing import List, Dict, Any
from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    first_pass_yield: float
    first_pass_yield_delta: float
    active_investigations: int
    critical_anomalies: int
    machines_monitored: int
    healthy_machines_count: int
    warning_machines_count: int
    critical_machines_count: int


class RecentInvestigationItem(BaseModel):
    investigation_id: str
    component_id: str
    machine_id: str
    failure_type: str
    primary_root_cause: str
    confidence: float
    severity: str
    status: str
    created_at: str


class FleetInsightItem(BaseModel):
    id: str
    type: str  # Critical, Warning, Optimization, Trend
    title: str
    description: str
    machine_id: str
    tool_id: str
    timestamp: str
    action_text: str


class DashboardOverviewResponse(BaseModel):
    metrics: DashboardMetrics
    machines: List[Dict[str, Any]]
    recent_investigations: List[RecentInvestigationItem]
    fleet_insights: List[FleetInsightItem]
    inspection_pass_rate_trend: List[Dict[str, Any]]
