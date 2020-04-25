import os
import glob
from os.path import join, dirname, realpath
from flask import Flask, current_app, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 8mb limit
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index_page():
    return current_app.send_static_file('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        old_files = glob.glob(app.config['UPLOAD_FOLDER'] + '/*')
        for f in old_files:
            os.remove(f)
        if 'file' not in request.files:
            flash('No file part')
            return request.url
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return request.url
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(app.config['UPLOAD_FOLDER'], filename))
            return url_for('uploaded_file', filename=filename)
        return current_app.send_static_file('index.html')
    else:
        return '<h3>Not Allowed</h3>'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
