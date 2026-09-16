from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class InvestigationRequest(BaseModel):
    component_id: str = "CNC-2847"
    machine_id: str = "CNC-07"
    failure_type: str = "Dimensional Inspection Failure"


class AnomalyItem(BaseModel):
    parameter: str
    normal_range: str
    actual_value: float
    deviation_pct: float
    severity: str  # Critical, Warning, Nominal
    timestamp: str
    machine_id: str
    explanation: str


class EvidenceItem(BaseModel):
    category: str  # TOOL USAGE, ANOMALY, TREND, MAINTENANCE, HISTORICAL, PROCESS
    title: str
    badge: str  # Confirmed, Strong Evidence, Supporting Evidence, Context
    description: str
    metrics: Dict[str, Any]


class RootCauseScore(BaseModel):
    root_cause: str
    confidence: float  # Percentage 0-100 (Evidence-weighted diagnostic score)
    root_cause_score: Optional[float] = None  # Exact normalized evidence score
    evidence_score: Optional[float] = None  # Alias for transparent evidence scoring
    confidence_level: str  # HIGH CONFIDENCE, MEDIUM-HIGH, MEDIUM, LOW
    severity: str  # Critical, Warning, Info
    score_breakdown: Dict[str, float]
    evidence: List[EvidenceItem]
    affected_parameters: List[str]
    supporting_records: List[Dict[str, Any]]
    recommended_actions: List[str]


class HistoricalMatch(BaseModel):
    case_id: str
    machine_id: str
    failure_type: str
    root_cause: str
    similarity_score: float  # Percentage 0-100
    evidence: str
    corrective_action: str
    resolution_time: float


class CorrectiveActionItem(BaseModel):
    type: str  # Immediate or Preventive
    priority: str  # High, Medium, Standard
    action: str
    reason: str
    expected_impact: str
    target_component_or_tool: str


class TrendPoint(BaseModel):
    timestamp: str
    component_id: Optional[str] = None
    vibration: float
    temperature: float
    power_consumption: float
    dimensional_deviation: Optional[float] = None
    cycle_count: Optional[int] = None
    is_failure_point: bool = False


class InvestigationSummary(BaseModel):
    component_id: str
    machine_id: str
    failure_type: str
    primary_root_cause: str
    confidence: float
    root_cause_score: Optional[float] = None
    evidence_score: Optional[float] = None
    severity: str
    key_evidence: List[str]
    recommended_immediate_action: str
    preventive_recommendation: str
    technical_narrative: str
    generated_by: str  # Deterministic Engine or LLM (OpenAI/Gemini)



class InvestigationResponse(BaseModel):
    investigation_id: str
    component_id: str
    machine_id: str
    failure_type: str
    severity: str
    status: str
    created_at: str
    inspection_details: Dict[str, Any]
    anomalies: List[AnomalyItem]
    trends: List[TrendPoint]
    root_cause_ranking: List[RootCauseScore]
    historical_matches: List[HistoricalMatch]
    corrective_actions: List[CorrectiveActionItem]
    investigation_summary: InvestigationSummary
