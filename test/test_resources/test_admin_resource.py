import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import sqlite3

from main import app
from config.app_config import AppConfig
from resources.auth_resource import oauth2_bearer, create_access_token

client = TestClient(app)

def test_register_employee(admin_dependency):
    emp_data = {
        "username" : "user@lmnop",  
        "role" : "admin"
    }
    response = client.post("/employee", json=emp_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("username") == emp_data["username"]
    assert response.json().get("role") == emp_data["role"]
    assert response.json().get("password_type") == AppConfig.DEFAULT_PASSWORD

def test_register_employee_negative(admin_dependency):
    emp_data = {
        "username" : "user@abcde",  
        "role" : "admin"
    }
    response = client.post("/employee", json=emp_data)
    assert response.status_code == status.HTTP_409_CONFLICT
