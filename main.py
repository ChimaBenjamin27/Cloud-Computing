# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
import os

from flask.helpers import url_for
from flask import Flask, render_template, request, redirect, session, abort
from flask_login.login_manager import LoginManager
from auth.gauth import gauth
from views.home import home
from views.adminView import adminView


#set environment variable to not need HTTPS for developing purposes
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    from db import database 
    
    # register a blueprint for authorization.
    app.register_blueprint(gauth, url_prefix="/auth")
    app.register_blueprint(home, url_prefix="")
    app.register_blueprint(adminView, url_prefix="/adminView")
    database.db.init_app(app)

    return app

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app = create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)
    #app.run(host='127.0.0.1', port=8050, debug=True)
else:
    app = create_app()
# [END gae_python3_app]
# [END gae_python38_app]
