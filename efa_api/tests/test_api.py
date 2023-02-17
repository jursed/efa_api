import pytest
from efa_api import create_app
from flask import Flask
import json


@pytest.fixture()
def app():
    """Set up Flask app"""
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
    """Set up Flask test client"""
    yield app.test_client()


# TODO not sure how to parametrize fixtures, loading files should really be just one function
@pytest.fixture()
def tenant_a(app):
    """Load Tenant-A payload"""
    with open("efa_api/tests/data/create_tenant_a.json", "r") as fp:
        yield json.load(fp)


@pytest.fixture()
def tenant_b(app):
    """Load Tenant-B payload"""
    with open("efa_api/tests/data/create_tenant_b.json", "r") as fp:
        yield json.load(fp)


@pytest.fixture()
def tenant_malformed(app):
    """Load malformed Tenant payload"""
    with open("efa_api/tests/data/create_tenant_malformed.json", "r") as fp:
        yield json.load(fp)


@pytest.fixture()
def tenant_update_add(app):
    """Load Tenant-B payload"""
    with open("efa_api/tests/data/update_tenant_a_add.json", "r") as fp:
        yield json.load(fp)


@pytest.fixture()
def tenant_update_delete(app):
    """Load Tenant-B payload"""
    with open("efa_api/tests/data/update_tenant_a_add.json", "r") as fp:
        yield json.load(fp)


@pytest.fixture()
def tenant_update_update(app):
    """Load Tenant-B payload"""
    with open("efa_api/tests/data/update_tenant_a_add.json", "r") as fp:
        yield json.load(fp)


def test_create_delete(client, tenant_a, capsys):
    """Simple create and delete"""
    response_create = client.post("/tenant", json=tenant_a)
    assert response_create.status_code == 200
    # with capsys.disabled():
    #     print(f"{response_create.data=}")

    response_delete = client.delete("/tenant", query_string="name=Tenant-A")
    # with capsys.disabled():
    #     print(f"{response_delete.data=}")
    assert response_delete.status_code == 200


def test_create_duplicated(client, tenant_a):
    """Duplicated create attempt"""
    response_create = client.post("/tenant", json=tenant_a)
    assert response_create.status_code == 200
    response_create = client.post("/tenant", json=tenant_a)
    assert response_create.status_code == 409

    response_delete = client.delete("/tenant", query_string="name=Tenant-A")
    assert response_delete.status_code == 200


def test_create_two(client, tenant_a, tenant_b):
    """Create and delete two Tenants"""
    response_create_a = client.post("/tenant", json=tenant_a)
    assert response_create_a.status_code == 200
    response_create_b = client.post("/tenant", json=tenant_b)
    assert response_create_b.status_code == 200

    response_delete_a = client.delete("/tenant", query_string="name=Tenant-A")
    assert response_delete_a.status_code == 200
    response_delete_b = client.delete("/tenant", query_string="name=Tenant-B")
    assert response_delete_b.status_code == 200


# @pytest.mark.xfail
def test_create_malformed(client, tenant_malformed):
    """Attempt to create Tenant based on bad payload"""
    response_create = client.post("/tenant", json=tenant_malformed)
    assert response_create.status_code == 400


def test_get(client, tenant_a):
    """Create, get, then delete Tenant"""
    response_create = client.post("/tenant", json=tenant_a)
    assert response_create.status_code == 200

    response_get = client.get("/tenant", query_string="name=Tenant-A")
    assert response_get.status_code == 200

    response_delete = client.delete("/tenant", query_string="name=Tenant-A")
    assert response_delete.status_code == 200


def test_get_nonexistent(client):
    """Attempt to get nonexistent Tenant"""
    response_get = client.get("/tenant", query_string="name=NONEXISTENT")
    assert response_get.status_code == 404


def test_get_tenants(client):
    """Get list of all Tenants"""
    response_get = client.get("/tenants")
    assert response_get.status_code == 200


def test_update_tenant_add(
    client, tenant_a, tenant_update_add, tenant_update_update, tenant_update_delete
):
    """Update existing Tenant - add, then update, then delete VLAN"""
    response_create = client.post("/tenant", json=tenant_a)
    assert response_create.status_code == 200

    response_update1 = client.put("/tenant/Tenant-A", json=tenant_update_add)
    assert response_update1.status_code == 200
    response_update2 = client.put("/tenant/Tenant-A", json=tenant_update_update)
    assert response_update2.status_code == 200
    response_update3 = client.put("/tenant/Tenant-A", json=tenant_update_delete)
    assert response_update3.status_code == 200

    response_delete = client.delete("/tenant", query_string="name=Tenant-A")
    assert response_delete.status_code == 200
