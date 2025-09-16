# upload file
import os
from werkzeug.utils import secure_filename



def upload_thumbnail(file):
    # set the upload folder
    UPLOAD_FOLDER = '../static/thumb/'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename

def upload_profile_photo(file):
    # set the upload folder
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../static/userImg/')
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename