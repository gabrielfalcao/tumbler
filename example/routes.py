#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@buildbottv.com>
#
from __future__ import unicode_literals

from tumbler import json_response, tumbler
from flask import render_template, request

from example.models import Person

web = tumbler.module(__name__)


def get_customers():
    return [p.to_dict() for p in Person.all()]


@web.get('/')
def index():
    return render_template('index.html')


@web.get('/api/time')
def access():
    return json_response(get_customers())


@web.post('/api/time')
def create():
    if request.json is None:
        return 'Missing user and email', 400

    if len(request.json.get('name', '').strip()) == 0:
        return 'Missing user name', 400

    if '@' not in request.json.get('email', '').strip():
        return 'Invalid email', 400

    Person.create(**request.json)
    return json_response(get_customers())
