import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_chatbot_location_query(client):
    message = {"message": "What’s the weather in Oxford?"}
    response = client.post("/chatbot", data=json.dumps(message), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "Oxford" in data["response"]

def test_chatbot_invalid_location(client):
    message = {"message": "What’s the weather in Atlantis?"}
    response = client.post("/chatbot", data=json.dumps(message), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "specify a valid location" in data["response"] or "not found" in data["response"]
