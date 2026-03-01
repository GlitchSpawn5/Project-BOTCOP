from fastapi import APIRouter
from backend.services.graph_engine import graph_engine

router = APIRouter()

@router.get("/")
async def get_graph():
    """
    Returns nodes and links for the dashboard visualization.
    """
    try:
        return graph_engine.get_graph_data()
    except Exception as e:
        # Return mock data for the prototype if Neo4j is not running
        return {
            "nodes": [
                {"id": 1, "label": "User", "properties": {"name": "admin"}},
                {"id": 2, "label": "Service", "properties": {"name": "auth-service"}},
                {"id": 3, "label": "IP", "properties": {"address": "192.168.1.50"}}
            ],
            "links": [
                {"source": 1, "target": 2, "type": "ACCESSED"},
                {"source": 1, "target": 3, "type": "LOGGED_IN"}
            ]
        }
