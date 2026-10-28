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



def test_get_events_id(api_client):
    id = 2
    response = api_client.get(f"/api/events/{id}")
    assert response.status_code == 200
    assert "event" in response.json()
    assert response.json()["event"]["id"] == 2
    assert response.json()["event"]["location"] == "venue_a"
    assert response.json()["event"]["capacity"] == 10
    assert response.json()["event"]["address"] == "address_a"

def test_get_event_by_id_not_found(api_client):
    response = api_client.get("/api/events/99999")
    assert response.status_code == 404

def test_get_event_by_id_not_found(api_client):
    response = api_client.get("/api/events/rubbuebirwe")
    assert response.status_code == 400
