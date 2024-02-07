import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import sqlite3

from main import app
from config.app_config import AppConfig

customer_client = TestClient(app)

def test_register_customer(reception_dependency):
    cust_data = {
        "name" : "Tanya Verma",
        "age" : 35,
        "gender" : "F",
        "email" : "vermatanya@gmail.com",
        "mobile_number" : "9635784520"
    }
    response = customer_client.post("/customer", json=cust_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == cust_data["name"]
    assert response.json()["age"] == cust_data["age"]
    assert response.json()["gender"] == "Female"
    assert response.json()["email"] == cust_data["email"]
    assert response.json()["mobile_number"] == cust_data["mobile_number"]
    assert response.json()["status"] == AppConfig.STATUS_ACTIVE

def test_get_all_customers(reception_dependency):
    response = customer_client.get("/customer")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["cust_id"] == "CUST12345"
    assert response.json()[0]["name"] == "Dev Mishra"
    assert response.json()[0]["age"] == 25
    assert response.json()[0]["gender"] == "Male"
    assert response.json()[0]["email"] == "dev25mishra@gmail.com"
    assert response.json()[0]["mobile_number"] == "7456369852"
    assert response.json()[0]["status"] == AppConfig.STATUS_ACTIVE

def test_deactiavte_customer(reception_dependency):
    response = customer_client.patch("/customer/dev25mishra@gmail.com")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["cust_email"] == "dev25mishra@gmail.com"
    assert response.json()["status"] == AppConfig.STATUS_INACTIVE

def test_customer_not_exist(reception_dependency):
    response = customer_client.patch("/customer/shyam23@gmail.com")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert  response.json()["detail"] == "Resource which you are looking for does not exist."

def test_customer_already_inactive(reception_dependency):
    response = customer_client.patch("/customer/dev25mishra@gmail.com")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert  response.json()["detail"] == "Resource is already inactive."
