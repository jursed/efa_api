import connexion


def create_app():
    connex_app = connexion.FlaskApp(__name__)
    api = connex_app.add_api("openapi.yaml", resolver=connexion.resolver.RelativeResolver("handlers"), resolver_error=501)
    app = connex_app.app

    return connex_app


if __name__ == "__main__":
    create_app().run(port=8080, debug=True)
