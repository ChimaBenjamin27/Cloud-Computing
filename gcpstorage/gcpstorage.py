
import os
import settings

from flask.blueprints import Blueprint
from google.cloud import storage

gcpstorage = Blueprint("gcpstorage", __name__, static_folder="../static/", template_folder="../templates/")

#Set the cloud computing storage credentials to authenticate against GCP
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cloud-computing-web-app-332414-76fe2e1f81c3.json'
## instantiate a new GCP Storage Client object (i/e the object that has the functions to interact with GCP Storage)
storage_client = storage.Client()

# helper method which uses GCP API to Upload files to a specific Bucket
def upload_to_bucket(blob_name, file):
    try:
        # instantiate an instance of the bucket that holds our files
        bucket = storage_client.get_bucket(settings.GCPBucketName)
        # create a blob instance in the bucket -- the blob will be empty at this point 
        blob = bucket.blob(blob_name)
        ## Upload the content of the file submitted to the server to the newly created blob in GCP
        ## file.read will read a stream of data, file.content_type will provide the metadata on the type of file, i/e .docx, .pdf, .mp4 etc
        ## store the newly created URL in a temporary variable that can be used in the future
        newObjURL = blob.upload_from_string(file.read(), file.content_type)
        print(newObjURL)
        return True
    except Exception as e:
        print(e)
        return


## Create extra methods to interact with GCP Storage here