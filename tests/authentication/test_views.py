import os
import json

import jwt
import pytest
from django.test import Client


def test_user_registration_endpoint_missing_fields() -> None:
    client = Client()

    response = client.post(
        "/api/auth/register/",
        {
            "email": "adelaide@example.com",
            "first_name": "Adelaide",
            "surname": "Doe",
        },
        content_type="application/json",
    )
    assert json.loads(response.content) == {
        "status": "error",
        "data": {
            "password": "field_required",
            "national_id": "field_required",
            "gender": "field_required",
            "date_of_birth": "field_required",
            "phone_number": "field_required",
        },
        "message": "",
    }


@pytest.mark.django_db
def test_user_registration_endpoint_proper_data(patient_default_fields_fixture) -> None:
    client = Client()

    patient_default_fields_fixture["email"] = "john@example.com"
    patient_default_fields_fixture["password"] = "some-password"
    response = client.post(
        "/api/auth/register/",
        patient_default_fields_fixture,
        content_type="application/json",
    )
    response_json = json.loads(response.content)
    patient_default_fields_fixture["date_joined"] = response_json["data"]["date_joined"]
    patient_default_fields_fixture["is_active"] = True
    patient_default_fields_fixture.pop("password")
    assert response_json == {
        "status": "success",
        "data": patient_default_fields_fixture,
        "message": "Created successfully.",
    }

    # attempt to register user with the same data
    patient_default_fields_fixture["password"] = "some-password"
    response = client.post(
        "/api/auth/register/",
        patient_default_fields_fixture,
        content_type="application/json",
    )
    response_json = json.loads(response.content)
    assert response_json == {
        "status": "error",
        "data": {"uuid": "unique_key_violation"},
        "message": "",
    }


@pytest.mark.django_db
def test_patient_login(patient_fixture):
    client = Client()

    # login failure
    response = client.post(
        "/api/auth/login/",
        {
            "email": "john@example.com",
            "password": "wrong-password",
        },
        content_type="application/json",
    )
    response_json = json.loads(response.content)
    assert response_json == {
        "status": "error",
        "data": {"message": "login_failed"},
        "message": "",
    }

    # login success
    response = client.post(
        "/api/auth/login/",
        {
            "email": "john@example.com",
            "password": "some-password",
        },
        content_type="application/json",
    )
    response_json = json.loads(response.content)
    assert response_json["status"] == "success"
    decoded_token = jwt.decode(
        response_json["data"]["token"],
        response_json["data"]["public_key"],
        algorithms=[response_json["data"]["algorithm"]],
    )
    assert decoded_token["sub"] == patient_fixture.uuid
    assert decoded_token["roles"] == "PATIENT"


@pytest.mark.django_db
def test_doctor_login_roles(doctor_fixture, health_worker_fixture):
    client = Client()
    response = client.post(
        "/api/auth/login/",
        {
            "email": "jane@example.com",
            "password": "some-password",
        },
        content_type="application/json",
    )
    response_json = json.loads(response.content)
    assert response_json["status"] == "success"
    decoded_token = jwt.decode(
        response_json["data"]["token"],
        response_json["data"]["public_key"],
        algorithms=[response_json["data"]["algorithm"]],
    )
    assert decoded_token["sub"] == doctor_fixture.uuid
    assert decoded_token["roles"] == "PATIENT HEALTH_WORKER"


def test_get_public_key():
    client = Client()
    response_json = json.loads(client.get("/api/auth/public-key/").content)
    assert response_json["data"]["algorithm"] == "RS384"
    assert response_json["data"]["public_key"] == os.environ["JWT_PUBLIC_KEY"]
