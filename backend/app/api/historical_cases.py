from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from app.services.data_service import DataService

router = APIRouter(prefix="/api/historical-cases", tags=["Historical Cases"])


@router.get("", response_model=List[Dict[str, Any]])
def get_historical_cases(
    search: Optional[str] = None,
    machine_id: Optional[str] = None,
    root_cause: Optional[str] = None,
    limit: int = Query(default=60, le=100)
):
    cases = DataService.get_historical_cases(limit=limit)

    filtered = cases
    if search:
        s = search.lower()
        filtered = [
            c for c in filtered
            if s in c.get("case_id", "").lower()
            or s in c.get("root_cause", "").lower()
            or s in c.get("evidence", "").lower()
            or s in c.get("failure_type", "").lower()
        ]

    if machine_id:
        filtered = [c for c in filtered if c.get("machine_id") == machine_id]

    if root_cause:
        filtered = [c for c in filtered if root_cause.lower() in c.get("root_cause", "").lower()]

    return filtered


@router.get("/{case_id}", response_model=Dict[str, Any])
def get_historical_case(case_id: str):
    cases = DataService.get_historical_cases()
    for c in cases:
        if c.get("case_id") == case_id:
            return c
    raise HTTPException(status_code=404, detail=f"Historical case {case_id} not found")
