from flask import session, abort
from flask.helpers import flash

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            flash("You need to login to view this")
            return abort(401) #authorisation required
        else:
            return function(*args, **kwargs)
    return wrapper