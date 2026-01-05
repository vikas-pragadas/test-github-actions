# tests/test_app.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home_route():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Welcome to the API"}

def test_hello_route():
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello word"}
