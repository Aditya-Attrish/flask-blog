# upload file
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file, folder_name, current_img):
    # set the upload folder
    UPLOAD_FOLDER = f'./app/static/{folder_name}/'
    if file and file.filename and allowed_file(file.filename):
        # remove the current image if it exists and default image is not empty
        if current_img and 'default-user.jpg' not in current_img:
            file_path = os.path.join(UPLOAD_FOLDER, current_img.split('/')[-1])
            if os.path.isfile(file_path):
                os.remove(file_path)
        elif not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        return f'{folder_name}/{unique_filename}'
    return current_img

def remove_image(file_path):
    if file_path:
        full_path = os.path.join('./app/static/', file_path)
        if os.path.exists(full_path):
            os.remove(full_path)