# ----------------------------
# !!!  Perform GEVENT monkey patch
# ----------------------------
from gevent import monkey
monkey.patch_all()

import pathlib
from flask import Flask as Webserver, render_template, request, session
from flask_cors import CORS
from requests import get, post, patch, delete, Request, Response

webserver = Webserver(__name__, template_folder=f"{pathlib.Path(__file__).parent}/../../view")
CORS(webserver)
