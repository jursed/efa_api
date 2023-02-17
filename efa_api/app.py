import connexion  # type: ignore
from efa_api import handlers


def create_app(test_config=None):
    connex_app = connexion.FlaskApp(__name__)
    api = connex_app.add_api(
        "openapi_frontend.yaml" if test_config is None else test_config.OPENAPI_SPEC,
        resolver=connexion.resolver.RelativeResolver(handlers),
        resolver_error=501,
        validate_responses=True,
        # strict_validation=True  # N/A for OAS3, see https://github.com/spec-first/connexion/issues/837
    )
    app = connex_app.app

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    return app
