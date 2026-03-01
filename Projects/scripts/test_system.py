import httpx
import pytest

BASE_URL = "http://localhost:8000/api/v1"

def test_root():
    response = httpx.get("http://localhost:8000/")
    assert response.status_code == 200
    assert "BOTCOP" in response.json()["message"]

def test_event_ingestion():
    log = {
        "id": "test_id",
        "timestamp": "2024-03-01T00:00:00",
        "type": "IAM_LOGIN",
        "actor": "test_user",
        "status": "SUCCESS",
        "source_ip": "127.0.0.1"
    }
    response = httpx.post(f"{BASE_URL}/events/ingest", json=log)
    assert response.status_code == 200

def test_threat_list():
    response = httpx.get(f"{BASE_URL}/threats/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_graph_data():
    response = httpx.get(f"{BASE_URL}/graph/")
    assert response.status_code == 200
    assert "nodes" in response.json()
