from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MachineSense Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
