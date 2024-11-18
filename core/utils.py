from flask import request
from werkzeug.utils import secure_filename
import os
import config
from core import app


app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER


upload_folder = app.config["UPLOAD_FOLDER"]


def upload_file():
    file = request.files["img"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))
    return filename
