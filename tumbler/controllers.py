#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2013 Gabriel Falcão <gabriel@buildbottv.com>
#
from __future__ import unicode_literals
import time
import logging
import requests
from urlparse import urljoin
from buildbottv import settings
from buildbottv.framework.http import json_response
from flask import (
    Blueprint,
    render_template,
)


module = Blueprint('web', __name__)
logger = logging.getLogger('buildbottv.web')


@module.context_processor
def inject_basics():
    return dict(
        settings=settings,
        static_url=lambda path: "{0}/{1}?{2}".format(

            settings.STATIC_BASE_URL.rstrip('/'),
            path.lstrip('/'),
            time.time()
        ),
    )


@module.route('/')
def index():
    return render_template('index.html')


class BuildBotApiProxy(object):
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.BUILDBOT_BASE_URL

    def make_url(self, path):
        return urljoin(self.base_url, path)

    def get_builds(self):
        return [self.get_last_build_for_builder_name(n)
                for n in self.get_builders()]

    def get_last_build_for_builder_name(self, name):
        url = self.make_url('json/builders/{0}/builds/_all'.format(name))
        response = requests.get(url, verify=False)

        data = response.json()
        if not data:
            return None

        latest_build = sorted(data.keys(), key=int)[-1]
        raw_build = data[latest_build]
        return self.raw_build_to_pretty_dict(raw_build)

    def raw_build_to_pretty_dict(self, raw_build):
        data = {}

        def retrieve_logs(name, url):
            response = requests.get(url + '/text', verify=False)

            if response.status_code == 404:
                return name, None

            return name, response.text

        def prettyfy_step(step):
            if not step['isFinished']:
                return

            started_at, finished_at = step['times']
            return {
                'name': step.pop('name'),
                'logs': dict([retrieve_logs(kind, url)
                              for kind, url in step['logs']]),
                'command': ' '.join(step['text']),
                'started_at': started_at,
                'finished_at': finished_at,
            }

        data = dict([(x[0], x[1]) for x in raw_build.pop('properties')])

        data['short_commit_message'] = data.get('commit_message', '\n').strip()

        data['reason'] = raw_build['reason']
        if raw_build['text']:
            status = raw_build['text'][0]
            data['status'] = status
            data['text'] = raw_build['text'][-1]

        data['name'] = raw_build['builderName']

        all_steps = [prettyfy_step(s) for s in raw_build.pop('steps')]
        completed_steps = [x for x in all_steps if x is not None]

        data['all_steps'] = all_steps
        data['completed_steps'] = completed_steps

        is_finished = all_steps == completed_steps
        data['is_finished'] = is_finished

        if is_finished:
            data['css_class'] = (
                status == 'failed' and 'alert-warning' or 'alert-success')
        else:
            data['css_class'] = 'alert-info'

        return data

    def get_builders(self):
        url = self.make_url('json/builders')
        response = requests.get(url, verify=False)
        try:
            data = response.json()
        except ValueError:
            logging.exception(
                'failed to retrieve url %s: %s', url, response.text)
            return []

        return data.keys()


@module.route('/api/builds')
def builds():
    proxy = BuildBotApiProxy()
    all_builds = proxy.get_builds()
    completed_builds = [x for x in all_builds if x is not None]

    data = {
        'all_builds': all_builds,
        'completed_builds': completed_builds
    }
    return json_response(data, 200)
