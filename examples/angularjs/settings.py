#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

SQLALCHEMY_URI = os.getenv('SQLALCHEMY_URI') or 'sqlite:///example.db'
