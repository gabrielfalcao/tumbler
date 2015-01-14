#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Response, request

from tumbler.core import Registry

version = '0.0.2'
tumbler = Registry()


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


def json_response(data, code, headers={}):
    serialized = json.dumps(data, indent=2)
    headers['Content-Type'] = 'application/json'

    for key in headers.keys():
        value = headers.pop(key)
        headers[str(key)] = str(value)

    return Response(serialized, status=code, headers=headers)
