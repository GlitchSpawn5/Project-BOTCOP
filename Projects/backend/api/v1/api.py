from fastapi import APIRouter
from backend.api.v1.endpoints import events, graph, threats, response, deception

api_router = APIRouter()
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
api_router.include_router(threats.router, prefix="/threats", tags=["threats"])
api_router.include_router(response.router, prefix="/response", tags=["response"])
api_router.include_router(deception.router, prefix="/deception", tags=["deception"])
