from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(title="BOTCOP AI Inference Server")

class ThreatContext(BaseModel):
    anomaly_id: str
    log_stream: List[dict]
    graph_context: Optional[dict] = None

class ReasoningOutput(BaseModel):
    threat_category: str
    risk_score: int
    explanation: str
    mitigation: str

@app.post("/reason", response_model=ReasoningOutput)
async def reason_threat(context: ThreatContext):
    """
    RAG-based Threat Reasoning.
    In production, this would call Mistral 7B with the retrieved context.
    """
    # Simulate LLM processing time
    time.sleep(1)
    
    # Simple rule-based reasoning for the prototype if model is missing
    prompt = f"Analyze these logs: {context.log_stream}"
    
    # Logic to detect prompt injection in the 'prompt' field of logs (if any)
    for log in context.log_stream:
        if log.get("type") == "LLM_USAGE":
            if "ignore all previous instructions" in log.get("prompt", "").lower():
                return ReasoningOutput(
                    threat_category="Prompt Injection",
                    risk_score=95,
                    explanation="Detected 'Instruction Override' pattern in LLM usage log.",
                    mitigation="Block User, Reset Session, Sanitize Input"
                )

    return ReasoningOutput(
        threat_category="Credential Misuse",
        risk_score=75,
        explanation="Detected login from unknown IP following a lateral movement attempt.",
        mitigation="Enforce MFA, Revoke Active Tokens"
    )

@app.post("/detect-injection")
async def detect_injection(prompt: str):
    # Prompt Injection Defense logic
    malicious_patterns = ["ignore all previous", "system:", "admin:", "bypass"]
    is_malicious = any(p in prompt.lower() for p in malicious_patterns)
    return {"is_malicious": is_malicious, "score": 0.99 if is_malicious else 0.01}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
