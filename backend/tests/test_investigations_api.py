from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_endpoint_demo_failure():
    payload = {
        "component_id": "CNC-2847",
        "machine_id": "CNC-07",
        "failure_type": "Dimensional Inspection Failure"
    }
    response = client.post("/api/investigations/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["component_id"] == "CNC-2847"
    assert data["machine_id"] == "CNC-07"
    assert len(data["root_cause_ranking"]) >= 4
    assert data["root_cause_ranking"][0]["root_cause"] == "Tool Wear"
    assert data["root_cause_ranking"][0]["confidence"] > 80.0
    assert len(data["anomalies"]) >= 3
    assert len(data["historical_matches"]) >= 2
    assert len(data["corrective_actions"]) >= 2
    assert data["investigation_summary"]["primary_root_cause"] == "Tool Wear"
    assert len(data["trends"]) > 10


def test_dashboard_overview_endpoint():
    response = client.get("/api/dashboard/overview")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert data["metrics"]["machines_monitored"] == 8
    assert len(data["machines"]) == 8


def test_machines_list_endpoint():
    response = client.get("/api/machines")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8


def test_machine_detail_endpoint():
    response = client.get("/api/machines/CNC-07")
    assert response.status_code == 200
    data = response.json()
    assert data["machine_id"] == "CNC-07"
    assert data["status"] == "Critical"
