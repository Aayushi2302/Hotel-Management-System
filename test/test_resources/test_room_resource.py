import pytest
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import sqlite3

from main import app
from config.app_config import AppConfig
from resources.auth_resource import oauth2_bearer, create_access_token

room_client = TestClient(app)

def test_create_room(admin_dependency):
    room_data = {
        "room_no" : 12,
        "floor_no" : 5,
        "charges" : 5000
    }
    response = room_client.post("/room", json=room_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["room_no"] == room_data["room_no"]
    assert response.json()["floor_no"] == room_data["floor_no"]
    assert response.json()["charges"] == room_data["charges"]
    assert response.json()["status"] == AppConfig.ROOM_STATUS_AVAILABLE

def test_get_all_rooms(admin_dependency):
    response = room_client.get("/room")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["room_id"] == "ROOM12345"
    assert response.json()[0]["room_no"] == 15
    assert response.json()[0]["floor_no"] == 2
    assert response.json()[0]["charges"] == 2500
    assert response.json()[0]["status"] == AppConfig.ROOM_STATUS_AVAILABLE

def test_update_room_status(admin_dependency):
    room_data = {
        "room_no" : 12,
        "floor_no" : 5,
        "status" : AppConfig.ROOM_STATUS_BOOKED
    }
    response = room_client.patch("/room", json=room_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["room_no"] == 12
    assert response.json()["floor_no"] == 5
    assert response.json()["status"] == AppConfig.ROOM_STATUS_BOOKED

def test_room_not_exist_update(admin_dependency):
    room_data = {
        "room_no" : 15,
        "floor_no" : 1,
        "status" : AppConfig.ROOM_STATUS_BOOKED
    }
    response = room_client.patch("/room", json=room_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource which you are looking for does not exist."

def test_room_status_available_update(admin_dependency):
    room_data = {
        "room_no" : 15,
        "floor_no" : 2,
        "status" : AppConfig.ROOM_STATUS_AVAILABLE
    }
    response = room_client.patch("/room", json=room_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Resource is already available."

def test_get_all_available_room(reception_dependency):
    response = room_client.get("/room/available")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["room_id"] == "ROOM12345"
    assert response.json()[0]["room_no"] == 15
    assert response.json()[0]["floor_no"] == 2
    assert response.json()[0]["charges"] == 2500

def test_get_preferred_price_room(reception_dependency):
    response = room_client.get("/room/preferred?price=3000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["room_id"] == "ROOM12345"
    assert response.json()[0]["room_no"] == 15
    assert response.json()[0]["floor_no"] == 2
    assert response.json()[0]["charges"] == 2500