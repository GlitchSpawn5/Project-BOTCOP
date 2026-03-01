from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from backend.services.graph_engine import graph_engine
from backend.services.deception_mesh import deception_mesh
from typing import Dict, List

router = APIRouter()

class LogEvent(BaseModel):
    id: str
    timestamp: str
    type: str
    actor: str = None
    source_ip: str = None
    service: str = None
    details: str = None

active_events: List[dict] = []

@router.post("/ingest")
async def ingest_log(log: Dict, background_tasks: BackgroundTasks):
    """
    Primary endpoint for log ingestion from simulators.
    """
    # 1. Store in memory (for dashboard WebSocket mockup)
    active_events.insert(0, log)
    if len(active_events) > 100: active_events.pop()
    
    # 2. Check Deception Mesh (Honeypots)
    if log.get("endpoint"):
        check = deception_mesh.check_honeypot_access(log["endpoint"], log.get("source_ip", "0.0.0.0"))
        if check["triggered"]:
            # Trigger high-priority threat reasoning
            print(f"ALARM: Honeypot triggered by {log['source_ip']}")

    # 3. Process Graph in background
    background_tasks.add_task(graph_engine.process_log, log)
    
    return {"status": "received"}

@router.get("/")
async def get_recent_events():
    return active_events
