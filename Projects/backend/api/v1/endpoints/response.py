from fastapi import APIRouter
from backend.services.response_engine import response_engine

router = APIRouter()

@router.post("/execute")
async def execute_action(threat_id: str, action: str):
    """
    Execute a mitigation action for a specific threat.
    """
    # Mock data for data-driven actions
    mock_data = {"actor": "suspicious_user", "service": "k8s-pod-123", "source_ip": "5.6.7.8"}
    
    result = await response_engine.execute_mitigation({
        "threat_category": "Manual Action",
        "mitigation": action,
        "risk_score": 100, # Manual actions override risk checks
        **mock_data
    })
    return result

@router.post("/mode")
async def toggle_mode(mode: str):
    response_engine.set_mode(mode)
    return {"status": "SUCCESS", "current_mode": response_engine.mode}
