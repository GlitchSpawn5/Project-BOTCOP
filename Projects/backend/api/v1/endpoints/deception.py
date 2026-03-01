from fastapi import APIRouter
from backend.services.deception_mesh import deception_mesh

router = APIRouter()

@router.get("/honeypots")
async def get_honeypots():
    return {"endpoints": deception_mesh.honeypot_endpoints}

@router.post("/decoys/generate")
async def generate_decoy(context: str = "general"):
    decoy = deception_mesh.generate_decoy_credential(context)
    return decoy

@router.get("/decoys/active")
async def get_active_decoys():
    return deception_mesh.active_decoys
