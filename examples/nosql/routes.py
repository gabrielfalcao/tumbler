#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@buildbottv.com>
#
from __future__ import unicode_literals
from datetime import datetime
from tumbler import json_response, tumbler
from flask import render_template

web = tumbler.module(__name__)


@web.get('/')
def index():
    return render_template('index.html')


@web.get('/api/clock')
def clock():
    return json_response({'datetime': datetime.utcnow().isoformat()})
