from fastapi.testclient import TestClient
from main import app

def test_get_events(api_client):
    response = api_client.get("/api/events")

    assert response.status_code == 200
    assert "events" in response.json()
    assert len(response.json()["events"]) == 5
    assert response.json()["events"][0]["title"] == "event_e"
    events = response.json()["events"]
    start_times = [event["starts_at"] for event in events]
    assert start_times == sorted(start_times)