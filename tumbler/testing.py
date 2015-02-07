#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from sure import scenario
from freezegun import freeze_time
from tumbler.core import Web


def prepare_db(context):
    context.web = Web()
    context.web.prepare_models()
    context.web.db.create_all()


def cleanup_db(context):
    context.web.db.drop_all()


def database_test(freeze_at='2015-02-25'):
    freeze_the = freeze_time(freeze_at)
    return freeze_the(scenario(prepare_db, cleanup_db))
