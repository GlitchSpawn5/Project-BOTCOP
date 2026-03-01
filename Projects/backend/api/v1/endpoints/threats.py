from fastapi import APIRouter
import httpx
from backend.core.config import settings
from typing import List

router = APIRouter()

@router.get("/")
async def get_threats():
    """
    Fetch detected threats and their AI reasoning.
    """
    # In a real system, this would fetch from PostgreSQL.
    # For the prototype, we simulate a call to the Mistral Inference Server.
    threats = [
        {
            "id": "th_1",
            "category": "Credential Misuse",
            "risk_score": 85,
            "explanation": "Multiple login failures from a non-standard IP (1.2.3.4) for user 'hr_manager'.",
            "mitigation": "Enforce MFA and revoke active tokens."
        },
        {
            "id": "th_2",
            "category": "Prompt Injection",
            "risk_score": 98,
            "explanation": "Detected instruction override pattern in 'llm-gateway' logs.",
            "mitigation": "Block user 'sales_rep' and sanitize all future inputs."
        }
    ]
    return threats

@router.post("/analyze/{anomaly_id}")
async def analyze_with_ai(anomaly_id: str, logs: List[dict]):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ML_INFERENCE_URL}/reason",
            json={"anomaly_id": anomaly_id, "log_stream": logs}
        )
        return response.json()
