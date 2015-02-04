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
import os
import traceback
from collections import OrderedDict
from sqlalchemy import Column
from flask import Flask, Blueprint
from flask.ext import sqlalchemy
from tumbler.models import MODELS, Model, ORM
from sqlalchemy.ext.declarative import declarative_base

MODULES = OrderedDict()


class SQLAlchemy(sqlalchemy.SQLAlchemy):
    def make_declarative_base(self):
        base = declarative_base(cls=Model, name='Model',
                                metaclass=ORM)
        base.query = sqlalchemy._QueryProperty(self)
        return base


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
        self.flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite://'
        self.collect_modules()
        self.db = SQLAlchemy(self.flask_app)

    def prepare_models(self):
        for name, ScopedModel in MODELS.items():
            attributes = {'__tablename__': ScopedModel.__tablename__}
            columns = dict([(k, v) for k, v in ScopedModel.__dict__.items() if isinstance(v, Column)])
            attributes['__columns__'] = columns
            attributes.update(columns)
            ScopedModel.Table = type(name, (self.db.Model,), attributes)
            ScopedModel.__session__ = self.db.session
            ScopedModel.__columns__ = columns

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
        self.prepare_models()
        self.db.create_all()
        self.flask_app.run(*args, **kw)


class ErrorHandlers(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def internal_error(self, exception):
        self.flask_app.logger.exception(
            "The Flask application suffered an internal error")

        return traceback.format_exc(exception), 500, {'content-type': 'text/plain'}
