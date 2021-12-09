import traceback

from flask.blueprints import Blueprint
from flask import Flask, render_template, request, redirect
from db import database
from auth import mods
from gcpstorage import gcpstorage
from random import randint
from datetime import datetime

home = Blueprint("home", __name__, static_folder="../static/", template_folder="../templates/")


# The default (aka home) route for the app
@home.route('/', methods=['POST', 'GET'])
def index():
    # if the subnit method is a "POST" then we can determine that a form has been submitted
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
        return render_template('index.html', **locals())

## This route will delete a record from the database based on what's passed to it.
@home.route('/delete/<int:id>')
def delete(id):
    ## Take the id which is passed in the request query parameters and query the database for it
    ## return the record if it exists, otherwise redirect to a 404 page
    task_to_delete = database.todo.query.get_or_404(id)
    try:
        ## once the record has been found, delete it and commit changes following by redirecting to the home page to reload the page
        database.db.session.delete(task_to_delete)
        database.db.session.commit()
        return redirect('/')
    except:
            ## handle the error gracefully if something goes wrong when trying to delete
            return "Delete didn't work"

## This route handles uploading of files to Google Cloud Storage
@home.route('/upload/<int:id>', methods=['POST'])
def upload(id):
    ## look in the submitted request for any files. request.files is a dictionary of files that have been streamed to the server
    files = request.files.getlist('filestoupload')
    ## as the current form is multipart (i/e multiple file upload) we need to save each file that has been uploaded
    for upload in files:
        ## give the new file a unique name by concatenating the ID of the task the file is for, appending the file name, the current date time and 4 random digits
        newFilename = str(id)+upload.filename+str(datetime.now())+str(randint(1000, 9999))
        ## use the gcpstorage package to help upload so this file can stay clean and have loosely coupled relationships
        gcpstorage.upload_to_bucket(newFilename, upload)
    return redirect('/')
    

## This route handles the updating of items in the database
## it also has a custom decorator on it "@mods.login_is_required" which controls access to the route to make sure only authenticated users can get to it
@home.route('/update/<int:id>', methods=['POST','GET'])
@mods.login_is_required
def update(id):
    ## the update route has it's own html page to render and we would like to pre-load the form with the data from the database
    ## so first we try to find the record in the database based on the ID passed in the request and throw a 404 if it's not found
    task = database.todo.query.get_or_404(id)
    ## this route handles both loading the page for the first time (i/e GET) and submitting an updated (i/e POST)
    ## if we have posted an update, then...
    if request.method == 'POST':
        ## get the updated content from the form and update the local record accordingly
        task.content = request.form['content']
        try:
            ## then try to save the changes of the record and redirect back to the home route
            database.db.session.commit()
            return redirect('/')
        except:
            ## handle exceptions gracefully
            return 'Could not update your task'
    else:
        ## if it's the first time loading the page, then load update.html and pass task for JINJA to use. (we could also be less prescriptive here and pass **locals())
        return render_template('update.html', task=task)
        
