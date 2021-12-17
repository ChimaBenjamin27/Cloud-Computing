import traceback

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect
from db import database
from auth import mods
from gcpstorage import gcpstorage
from random import randint
from datetime import datetime

adminView = Blueprint("adminView", __name__, static_folder="../static/", template_folder="../templates/")


# This is the route for the view of the admin app
@adminView.route('/', methods=['POST', 'GET'])
def index():
    # if the submit method is a "POST" then we can determine that a form has been submitted
    if request.method == 'POST':
        # check the request for a form named 'content' (i/e in templates > index.html there is a form there with an action to submit to route '/' and called content)
        task_content = request.form['content']
        # create a new object with the database model we need based on the content of the html form
        new_task = database.todo(content=task_content)

        try:
            ## try to add the new object to the database and commit it then redirect to the home page. The redirect will be sent as GET
            database.db.session.add(new_task)
            database.db.session.commit()
            return redirect('/')
        except Exception as e:
            ## handle the error if something goes wrong trying to save to the new record to the database.
            ## this should probably redirect to a user friendly error page
            return traceback.print_tb(e.__traceback__, limit=None, file=None)
    # Otherwise if the request was submitted with a GET method then we can assume the load is loading fresh
    else:
        ## Query the database for a list of items we want to show
        tasks = database.todo.query.order_by(database.todo.date_created).all()
        ## then show index.html -- passing **locals() will take any local variables declared here, i/e tasks, and make it available to the HTML via JINJA.
        ## in index.html, we can reference tasks using jinja and build HTML accordingly
        return render_template('adminView.html', **locals())

## This route will delete a record from the database based on what's passed to it.
@adminView.route('/download/<int:id>', methods=['POST', 'GET'])
def download(id):
    ## look in the submitted request for any files. request.files is a dictionary of files that have been streamed to the server
    files = request.files.getlist('filestodownload')
    ## as the current form is multipart (i/e multiple file upload) we need to save each file that has been uploaded
    for download in files:
        ## give the new file a unique name by concatenating the ID of the task the file is for, appending the file name, the current date time and 4 random digits
        newFilename = str(id)+download.filename+str(datetime.now())+str(randint(1000, 9999))
        ## use the gcpstorage package to help upload so this file can stay clean and have loosely coupled relationships
        gcpstorage.upload_to_bucket(newFilename, download)
    return redirect('/adminView')