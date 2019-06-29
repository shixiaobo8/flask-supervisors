#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	flask-scripts 定制脚本文件
	
"""
import sys
from flask_script import Command,Option
from flask_supervisor import socketio


class Hello(Command):

    def run(self):
        print("hello,flask_scripts")


class runsocketio(Command):
    help = description = 'Runs the Flask development server i.e. app.run()'

    def __init__(self,app=None,host='0.0.0.0', port=5000, use_debugger=None,
                 use_reloader=None, threaded=False, processes=1,
                 passthrough_errors=False, **options):

        self.app = app
        self.port = port
        self.host = host
        self.use_debugger = use_debugger
        self.use_reloader = use_reloader if use_reloader is not None else use_debugger
        self.server_options = options
        self.threaded = threaded
        self.processes = processes
        self.passthrough_errors = passthrough_errors

    def get_options(self):

        options = (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('--threaded',
                   dest='threaded',
                   action='store_true',
                   default=self.threaded),

            Option('--processes',
                   dest='processes',
                   type=int,
                   default=self.processes),

            Option('--passthrough-errors',
                   action='store_true',
                   dest='passthrough_errors',
                   default=self.passthrough_errors),

            Option('-d', '--debug',
                   action='store_true',
                   dest='use_debugger',
                   help='enable the Werkzeug debugger (DO NOT use in production code)',
                   default=self.use_debugger),
            Option('-D', '--no-debug',
                   action='store_false',
                   dest='use_debugger',
                   help='disable the Werkzeug debugger',
                   default=self.use_debugger),

            Option('-r', '--reload',
                   action='store_true',
                   dest='use_reloader',
                   help='monitor Python files for changes (not 100%% safe for production use)',
                   default=self.use_reloader),
            Option('-R', '--no-reload',
                   action='store_false',
                   dest='use_reloader',
                   help='do not monitor Python files for changes',
                   default=self.use_reloader),
        )
        return options


    def __call__(self, app, host, port, use_debugger, use_reloader,
                 threaded, processes, passthrough_errors):
        # we don't need to run the server in request context
        # so just run it directly

        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
                if sys.stderr.isatty():
                    print("Debugging is on. DANGER: Do not allow random users to connect to this server.",
                          file=sys.stderr)
        if use_reloader is None:
            use_reloader = use_debugger

        socketio.run(app=app,host=host,
                port=port,
                debug=use_debugger,
                use_reloader=use_reloader,
                **self.server_options)