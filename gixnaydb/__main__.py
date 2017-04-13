#!/usr/bin/env python3

from gixnaydb import app
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
import gixnaydb.util as util
import json
import sys

print('== CONFIG ==')
print(json.dumps(util.config, indent=4))
print('==+------+==')


def assert_has(iterable, key):
    if key not in iterable:
        raise KeyError(key, iterable)


for key in ['ssl_options']:
    assert_has(util.config, key)
for key in ['certfile', 'keyfile']:
    assert_has(util.config['ssl_options'], key)

if '--debug' in sys.argv:
    app.run(host=(util.config.get('address') or '0.0.0.0'),
            port=(util.config.get('port') or '25562'),
            debug=True,
            ssl_context=tuple(util.config.get('ssl_options').values()))
else:
    http_server = HTTPServer(
        Application([
            (r'^.*', FallbackHandler, {
                'fallback': WSGIContainer(app)
            }),
        ]),
        ssl_options=util.config['ssl_options'])

    http_server.bind(**{
        option: util.config[option]
        for option in util.config if option in ('address', 'port')
    })
    http_server.start(0)
    IOLoop.instance().start()
