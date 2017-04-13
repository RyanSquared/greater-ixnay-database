from flask import Flask
from gixnaydb import rest

app = Flask(__name__)
routes = []


def add_route(route, methods=['GET']):
    print(route, repr(methods))
    routes.append((route, ','.join(methods)))
    return app.route(route, methods=methods)


rest.add_routes(add_route, routes, app)
