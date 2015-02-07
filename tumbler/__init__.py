#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json as basejson
from flask import Response, request

from tumbler.core import Registry
from tumbler.models import Model

version = '0.0.13'
tumbler = Registry()


from datetime import date, time, datetime


def json_converter(value):
    date_types = (datetime, date, time)
    if isinstance(value, date_types):
        value = value.isoformat()

    return str(value)


class json(object):
    @staticmethod
    def dumps(data, **kw):
        kw['default'] = json_converter
        return basejson.dumps(data, **kw)

    @staticmethod
    def loads(*args, **kw):
        return basejson.loads(*args, **kw)


def set_cors_into_headers(headers, allow_origin,
                          allow_credentials=True, max_age=60 * 5):
    """Takes flask.Response.headers and a string contains the origin
    to be allowed and modifies the given headers inline.

    >>> headers = {'Content-Type': 'application/json'}
    >>> set_cors_into_headers(headers, allow_origin='*')
    """
    headers['Access-Control-Allow-Origin'] = allow_origin
    headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', '*')

    headers['Access-Control-Allow-Methods'] = request.headers.get(
        'Access-Control-Request-Method', '*')

    headers['Access-Control-Allow-Credentials'] = (
        allow_credentials and 'true' or 'false')

    headers['Access-Control-Max-Age'] = max_age


def json_representation(data, code, headers):
    set_cors_into_headers(headers, allow_origin='*')
    return json_response(data, code, headers)


def json_response(data, status=200, headers={}):
    serialized = json.dumps(data, indent=2)
    headers['Content-Type'] = 'application/json'

    for key in headers.keys():
        value = headers.pop(key)
        headers[str(key)] = str(value)

    return Response(serialized, status=status, headers=headers)
