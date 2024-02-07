import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import sqlite3

from main import app

auth_client = TestClient(app)

def test_login_positive():
    credentials = {
        "username" : "user@abcde",
        "password" : "Abcde@12345"
    }
    response = auth_client.post("/login", json=credentials)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User login successfully"

def test_login_negative():
    credentials = {
        "username" : "user@abcde",
        "password" : "Abcde@123"
    }
    response = auth_client.post("/login", json=credentials)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid login."