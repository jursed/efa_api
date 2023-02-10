import connexion
from connexion.resolver import RelativeResolver

app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml', resolver=RelativeResolver("efa_api"))
app.run(port=8080)