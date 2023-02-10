def getTenant(name):
    return f"{name=}", 200


def getTenants():
    return "foo", 200


def createTenant(body):
    from model import Tenant
    tenant = Tenant(**body)
    return repr(tenant), 200


def deleteTenant():
    ...


def updateTenant():
    ...
