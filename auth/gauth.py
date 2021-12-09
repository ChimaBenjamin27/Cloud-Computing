import os
from flask.helpers import flash
import google.auth.transport.requests
import requests
import settings

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from flask import session, abort, request, redirect
from pip._vendor import cachecontrol
from flask.blueprints import Blueprint


gauth = Blueprint("gauth", __name__, static_folder="../static/", template_folder="../templates/")

# Make sure the production lines are not commented out and development line are commented out when deploying to app engine

# Production Client Secret and Client ID
client_secret_file = os.path.join("client_secret.json")
GOOGLE_CLIENT_ID = '717596273398-r7ehfsk0p2esqlviejrnepo0fa0em5bj.apps.googleusercontent.com'

# Development Client Secret and Client ID
#client_secret_file = os.path.join("dev_client_secret.json")
#GOOGLE_CLIENT_ID = '132234238793-h50bqua3n7uku70qn464rshq82aft5jv.apps.googleusercontent.com'

print(client_secret_file)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
    redirect_uri= settings.GAuthRedirectURI)


#Authentication section




@gauth.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@gauth.route("/authorize")
def authorize():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")

@gauth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#End of Autnetication Section

