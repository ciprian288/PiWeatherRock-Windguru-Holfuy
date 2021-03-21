# -*- coding: utf-8 -*-
# Copyright (c) 2020 Gene Liverman <gene@technicalissues.us>
# Distributed under the MIT License (https://opensource.org/licenses/MIT)


###############################################################################
#   Raspberry Pi Weather Display Config Page Plugin
#   Original By: github user: metaMMA          2020-03-15
###############################################################################

# standard imports
import os
import json

# third-party imports
import cherrypy

with open(os.path.join(os.path.dirname(__file__), 'html/config.html'), 'r') as f:
    html = f.read()


class Config:
    """ Configuration page for PiWeatherRock. """

    def __init__(self, config_file):
        self.config_file = config_file

    @cherrypy.expose()
    def index(self):
        return html

    @cherrypy.tools.json_in()
    @cherrypy.expose
    def upload(self):
        dst = self.config_file

        input_json = cherrypy.request.json
        with open(dst, 'w') as f:
            json.dump(input_json, f, indent=2, separators=(',', ': '))
        self.index()


    @cherrypy.expose
    def log(self):
        with open(f"{os.getcwd()}/.log", "r") as f:
            log = f.read()
        return f"""
            <html>
                <head>
                    <title>PiWeatherRock Log</title>
                    <link rel="stylesheet" href="style.css" type="text/css" />
                </head>
                <body>
                    <a href="index">< Back to Configuration Page</a>
                    <div class="page_title">PiWeatherRock Log</div>
                    <br>
                    <div class="log">
                        <br>
                        <a href="#anchor">Jump to latest log entry</a>
                        <br>
                        <div id="scroller">
                            <!-- append content here -->
                            <pre>{log}</pre>
                            <br>
                            <button onclick="javascript:window.location.reload(true)" class="refresh">Refresh Log</button>
                            <br>
                            <br>
                            <div><a href="index">< Back to Configuration Page</a></div>
                            <div id="anchor"></div>
                        </div>
                    </div>
                </body>
            </html>"""


def main(config_file):
    cherrypy.quickstart(Config(config_file), config={
        'global': {
            'server.socket_port': 8888,
            'server.socket_host': '0.0.0.0'
        },
        '/serialize_script.js': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(
                os.path.dirname(__file__), "html/serialize_script.js")
        },
        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(
                os.path.dirname(__file__), "html/style.css")
        },
        '/chancetstorms.png': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(
                os.path.dirname(__file__), "icons/256/chancetstorms.png")
        },
        '/bg.png': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(
                os.path.dirname(__file__), "icons/bg.png")
        },
        '/config.json': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': config_file
        }
    })
