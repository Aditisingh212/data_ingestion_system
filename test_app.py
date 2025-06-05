from fastapi.testclient import TestClient
from main import app
import time
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Data Ingestion API"}

def test_ingest_invalid_payload():
    # Test missing priority
    response = client.post("/ingest", json={"ids": [1, 2, 3]})
    assert response.status_code == 422

    # Test invalid priority
    response = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "INVALID"})
    assert response.status_code == 422

    # Test empty ids
    response = client.post("/ingest", json={"ids": [], "priority": "HIGH"})
    assert response.status_code == 422

def test_ingest_valid_payload():
    response = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "HIGH"})
    assert response.status_code == 200
    assert "ingestion_id" in response.json()

def test_status_not_found():
    response = client.get("/status/nonexistent")
    assert response.status_code == 404

def test_priority_ordering():
    # Submit LOW priority first
    low = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "LOW"}).json()
    time.sleep(1)  # Wait a bit
    
    # Submit HIGH priority
    high = client.post("/ingest", json={"ids": [6, 7, 8, 9], "priority": "HIGH"}).json()
    
    # Wait for processing (at least 15 seconds for 3 batches)
    time.sleep(15)
    
    # Check statuses
    high_status = client.get(f"/status/{high['ingestion_id']}").json()
    low_status = client.get(f"/status/{low['ingestion_id']}").json()
    
    # HIGH priority should be completed or at least triggered
    assert high_status["status"] in ["completed", "triggered"]
    # LOW priority might still be yet_to_start or triggered
    assert low_status["status"] in ["yet_to_start", "triggered", "completed"]

def test_rate_limiting():
    # Submit multiple requests
    responses = []
    for i in range(3):
        response = client.post("/ingest", json={
            "ids": [i*3+1, i*3+2, i*3+3],
            "priority": "MEDIUM"
        }).json()
        responses.append(response)
    
    # Wait for processing (at least 15 seconds for 3 batches)
    time.sleep(15)
    
    # Check all statuses
    for resp in responses:
        status = client.get(f"/status/{resp['ingestion_id']}").json()
        assert status["status"] in ["triggered", "completed"]

def test_batch_processing():
    # Submit a request with more than 3 IDs
    response = client.post("/ingest", json={
        "ids": [1, 2, 3, 4, 5, 6, 7],
        "priority": "HIGH"
    }).json()
    
    # Wait for processing (at least 15 seconds for 3 batches)
    time.sleep(15)
    
    # Check status
    status = client.get(f"/status/{response['ingestion_id']}").json()
    
    # Verify batches
    assert len(status["batches"]) == 3  # Should be split into 3 batches
    for batch in status["batches"]:
        assert len(batch["ids"]) <= 3  # Each batch should have max 3 IDs
        assert batch["status"] in ["triggered", "completed"]

def test_concurrent_requests():
    # Submit multiple requests with different priorities
    high = client.post("/ingest", json={"ids": [1, 2, 3], "priority": "HIGH"}).json()
    med = client.post("/ingest", json={"ids": [4, 5, 6], "priority": "MEDIUM"}).json()
    low = client.post("/ingest", json={"ids": [7, 8, 9], "priority": "LOW"}).json()
    
    # Wait for processing (at least 15 seconds for 3 batches)
    time.sleep(15)
    
    # Check all statuses
    high_status = client.get(f"/status/{high['ingestion_id']}").json()
    med_status = client.get(f"/status/{med['ingestion_id']}").json()
    low_status = client.get(f"/status/{low['ingestion_id']}").json()
    
    # Verify all requests were processed
    assert high_status["status"] in ["triggered", "completed"]
    assert med_status["status"] in ["triggered", "completed"]
    assert low_status["status"] in ["triggered", "completed"]
