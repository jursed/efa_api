import pydantic
from efa_api.models_frontend import Tenant, TenantList, TenantUpdate
from flask import Response

tenants: dict[str, Tenant] = dict()  # {"tenant_name": Tenant(), ...}


def _new_tenant_id():
    """Generate new Tenant ID

    Helper function that returns the maximum of existing IDs, incremented by 1.

    Returns:
        int: A new Tenant ID
    """
    if tenants == {}:
        return 0
    else:
        return max(t.id for t in tenants.values()) + 1


def _res(response, status):
    """Simple wrapper around flask.Response"""
    response = response.json()
    return Response(response, status, mimetype="application/json")


def get_tenant(name):
    """Get Tenant by provided name

    Args:
        name: name of Tenant

    Returns:
        HTTP 200: Tenant object in JSON format
        HTTP 404: Tenant name nonexistent
    """
    try:
        return _res(tenants[name], 200)
    except KeyError:
        return Response(f"Tenant with {name=} not found", 404)


def get_tenants():
    """Get list of all existing Tenants

    Returns:
        HTTP 200: JSON list of Tenant objects
    """
    tenant_list = TenantList()
    tenant_list.tenant = [t.dict() for t in tenants.values()]
    return _res(tenant_list, 200)


def create_tenant(body):
    """Create a new Tenant

    Args:
        body: Tenant object in JSON form

    Returns:
        HTTP 200: Successful creation
        HTTP 400: Tenant failed to create (malformed request)
        HTTP 409: Duplicated Tenant name
    """
    try:
        tenant = Tenant(**body)
        tenant.id = _new_tenant_id()
    except pydantic.ValidationError as e:
        return Response("Tenant creation failed", 400)
    if tenant.name in tenants:
        return Response(f"Tenant with {tenant.name=} already exists", 409)
    else:
        tenants[tenant.name] = tenant
        return _res(tenant, 200)


def delete_tenant(name):
    """Delete an existing Tenant

    Args:
        name: name of Tenant to be deleted

    Returns:
        HTTP 200: Successful deletion
        HTTP 404: Tenant name nonexistent
    """
    try:
        response = _res(tenants[name], 200)
        del tenants[name]
        return response
    except KeyError:
        return Response(f"Tenant with {name=} not found", 404)


def update_tenant(tenant_name, body):
    """Update a Tenant's specific setting

    Args:
        name: name of Tenant to be updated
        body: TenantUpdate object in JSON form

    Returns:
        HTTP 200: Update successfully applied
        HTTP 404: Tenant name nonexistent
    """
    # XXX This endpoint spec seems broken to me
    name = tenant_name
    try:
        tu = TenantUpdate(**body)
    except pydantic.ValidationError:
        # TODO
        ...
    try:
        tenant = tenants[name]
    except KeyError:
        return f"Tenant with {name=} not found", 404
    req_tenant = tu.tenant
    req_op = tu.operation
    match req_op:
        case req_op.vlan_update:
            tenant.vlan_range = req_tenant.vlan_range
        case req_op.vlan_add:
            if tenant.vlan_range is None:
                tenant.vlan_range = req_tenant.vlan_range
            else:
                # Dumb handling - just append the string
                tenant.vlan_range += "," + req_tenant.vlan_range
        case req_op.vlan_delete:
            tenant.vlan_range = None
    return _res(tenants[name], 200)
