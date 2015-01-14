#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <tumbler - flask bootstrapper>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
import traceback
from flask import Flask, Blueprint

MODULES = OrderedDict()


class Module(object):
    def __init__(self, name):
        self.name = name
        self.handlers = OrderedDict()
        MODULES[name] = self

    def make_decorator(self, method, regex):
        def decorator(func):
            self.handlers[method, regex] = func
            return func

        return decorator

    def get(self, regex):
        return self.make_decorator('GET', regex)

    def post(self, regex):
        return self.make_decorator('POST', regex)

    def put(self, regex):
        return self.make_decorator('PUT', regex)

    def patch(self, regex):
        return self.make_decorator('PATCH', regex)

    def head(self, regex):
        return self.make_decorator('HEAD', regex)

    def options(self, regex):
        return self.make_decorator('OPTIONS', regex)

    def delete(self, regex):
        return self.make_decorator('DELETE', regex)


class Registry(object):
    def module(self, name):
        return Module(name)


class Web(object):
    def __init__(self, *args, **kwargs):
        self.assets = None
        self.commands_manager = None
        self.flask_app = Flask(__name__, *args, **kwargs)
        self.collect_modules()

    def enable_error_handlers(self):
        handler_for = ErrorHandlers(self.flask_app)
        self.add_error_handler(500, handler_for.internal_error)

    def add_error_handler(self, status_code, callback):
        handler = self.flask_app.errorhandler(status_code)
        return handler(callback)

    def __call__(self, environ, start_response):
        """Making this class behave like a WSGI app, forwarding the
        call to flask"""
        return self.flask_app(environ, start_response)

    def collect_modules(self):
        for name, module in MODULES.items():
            blueprint = Blueprint(name, module.name)
            for (method, regex), func in module.handlers.items():
                blueprint.add_url_rule(regex, methods=[method], view_func=func)
            self.flask_app.register_blueprint(blueprint)

    def run(self, *args, **kw):
        self.enable_error_handlers()
        self.flask_app.run(*args, **kw)


class ErrorHandlers(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def internal_error(self, exception):
        self.flask_app.logger.exception(
            "The Flask application suffered an internal error")
        return traceback.format_exc(exception), 500
