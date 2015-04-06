#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# flake8: noqa
import os
from plant import Node
from nosql import routes

from tumbler.core import Web


root_node = Node(__file__).dir

application = Web(
    template_folder=root_node.join('templates'),
    static_folder=root_node.join('static'),
    static_url_path='/assets',
    use_sqlalchemy=False,
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8000, application).serve_forever()
