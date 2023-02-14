from efa_api.models_frontend import Tenant


def getTenant(name):
    # TODO
    return f"{name=}", 200


def getTenants():
    # TODO
    return "foo", 200


def createTenant(body):
    # TODO
    tenant = Tenant(**body)
    return repr(tenant), 200


def deleteTenant():
    # TODO
    ...


def updateTenant():
    # TODO
    ...
