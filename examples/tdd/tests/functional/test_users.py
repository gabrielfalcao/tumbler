#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from sure import scenario
from datetime import datetime
from freezegun import freeze_time
from tumbler.core import Web
from timeless.models import User


def prepare_db(context):
    context.web = Web()
    context.web.prepare_models()
    context.web.db.create_all()


def cleanup_db(context):
    context.web.db.drop_all()


@freeze_time("2005-01-01")
@scenario(prepare_db, cleanup_db)
def test_create_user(context):
    ('Creating a user should work')

    result = User.create(
        email=u'bar@bar.com',
        password='foobar'
    )

    result.to_dict().should.equal({
        'date_added': datetime(2005, 1, 1, 0, 0),
        'email': u'bar@bar.com',
        'id': 1,
        'name': None,
        'password': u'foobar'
    })
