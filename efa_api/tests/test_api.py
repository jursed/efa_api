import pytest
from efa_api import create_app
from flask import Flask
import json


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def create_tenant_payload(app):
    with open("efa_api/tests/create_tenant.json", "r") as fp:
        return json.load(fp)


def test_create_tenant(client, create_tenant_payload):
    # TODO
    response = client.post("/tenant", json=create_tenant_payload)
    assert b"OK" in response.data
