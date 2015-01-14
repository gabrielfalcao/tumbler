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
import sys
import logging
import argparse
import coloredlogs
import importlib
from tumbler.core import Web


parser = argparse.ArgumentParser(prog='Tumbler')
parser.add_argument(
    '--log-level',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='DEBUG')
parser.add_argument('command')


def tumbler_run():
    parser = argparse.ArgumentParser(
        prog='tumbler run',
        description='runs the server')
    parser.add_argument('controller',
                        nargs="+", help='the path to the controllers file')

    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--templates-path', default='templates')
    parser.add_argument('--static-path', default='static')
    parser.add_argument('--static-url', default='/assets')
    parser.add_argument('--port', type=int, help='the port number',
                        default=8000)
    parser.add_argument('--host', help='the host name', default='localhost')
    args = parser.parse_args(sys.argv[2:])

    server = Web(
        template_folder=args.templates_path,
        static_folder=args.static_path,
        static_url_path=args.static_url,
    )
    for cname in args.controller:
        name, exc = os.path.splitext(cname)
        importlib.import_module('.{0}'.format(name))

    server.run(port=args.port, host=args.host)


def tumbler_shell():
    from IPython import embed
    embed()


def tumbler_test(kind):
    import sure
    destination = 'tests/{0}'.format(kind)
    if not os.path.exists(destination):
        os.makedirs(destination)
    os.execvp('nosetests', [
        'nosetests',
        '-s',
        '--rednose',
        '--stop',
        '-v',
        destination,
    ])
    sure


def tumbler_unit():
    tumbler_test('unit')


def tumbler_functional():
    tumbler_test('functional')


def main():
    args = parser.parse_args(sys.argv[1:2])

    log_level = getattr(logging, args.log_level, 'INFO')
    coloredlogs.install(level=log_level)

    HANDLERS = {
        'run': tumbler_run,
        'shell': tumbler_shell,
        'unit': tumbler_unit,
        'functional': tumbler_functional,
    }
    HANDLERS[args.command]()


if __name__ == '__main__':
    main()
