import base64
from flask import request, jsonify
from functools import wraps
from gixnaydb import util


class InvalidUsage(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


def requires_auth(f):
    @wraps(f)
    def decorated_requires_auth(*args, **kwargs):
        has_authorization_header = False
        auth = None
        try:
            auth = base64.decode(
                    request.headers['Authorization'].split(' ')[1])
            has_authorization_header = True
        except:
            return
        if not has_authorization_header:
            raise InvalidUsage("Missing Authorization field", 400)
        auth = base64.b64decode(auth)
        if not util.check_auth(auth):
            raise InvalidUsage("Invalid authorization", 401)
        return f(*args, **kwargs)
    return decorated_requires_auth


def nyi():
    raise InvalidUsage("Not yet implemented", 501)


def add_routes(add_route, routes, app):
    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        return jsonify(error.__dict__), error.status_code

    @add_route('/api/v1/test_error/<message>/<int:errnum>')
    def test_numeric(message, errnum):
        raise InvalidUsage(message, errnum)

    @add_route('/api/v1/test_error/<message>')
    def test_400(message):
        raise InvalidUsage(message)

    @add_route('/api/v1/routes')
    def return_thing():
        return jsonify(routes)

    @add_route('/api/v1/config')
    def get_config():
        return jsonify(util.config)

    @add_route('/api/v1/countries')
    def get_countries_list():
        return jsonify([country for country in util.get_countries()])

    @add_route('/api/v1/countries/name')
    def get_country_names():
        return jsonify([name for name in util.get_country_names()])

    @add_route('/api/v1/countries/by_<key>/<value>')
    def get_countries_by(key, value):
        if key not in util.dz_keys:
            raise InvalidUsage(f"Key not found: {key}")
        return jsonify([
            country for country in util.get_countries_by(key, value)])

    @add_route('/api/v1/countries/sort_by/<key>')
    def get_countries_sorted_by(key):
        if key not in util.dz_keys:
            raise InvalidUsage(f"Key not found: {key}")
        return jsonify([country for country in util.get_countries(key)])
