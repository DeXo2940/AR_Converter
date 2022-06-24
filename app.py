from flask import Flask, render_template, request, send_file, session
from werkzeug.utils import secure_filename
from os import path, makedirs, walk, remove
from uuid import uuid4

import datetime

from ar_converter_engine import convert

SESSION_FILENAME_VARIABLE = 'session_filename'
UPLOAD_PATH = 'uploads/'
PROCESSED_PATH = 'processed/'
NECESSARY_PATHS = [UPLOAD_PATH, PROCESSED_PATH]

DEFAULT_EXCEL_EXTENSION = 'xlsx'
ALLOWED_EXTENSIONS = [DEFAULT_EXCEL_EXTENSION]


def remove_all_files():
    for dest_path in NECESSARY_PATHS:
        if not path.exists(dest_path):
            continue
        filenames = next(walk(dest_path), (None, None, []))[2]
        for file in filenames:
            remove(dest_path + file)


def check_file_extension(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS


# TODO: Remove files on schedule

# Create necessary destinations if they don't exist
for destination_path in NECESSARY_PATHS:
    if not path.exists(destination_path):
        makedirs(destination_path)
remove_all_files()

app = Flask(__name__)
app.secret_key = str(uuid4())  # 'super secret key'

app.config['UPLOAD_FOLDER'] = UPLOAD_PATH  # define upload path
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024  # 50Kb # * 1024  # define max file size


@app.route('/')
def upload_view():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        if not check_file_extension(f.filename):
            return 'Invalid file type'
        f.filename = str(uuid4())
        print('upload: {}'.format(f.filename))
        f.save(path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))  # this will secure the file
        output_file_name = str(uuid4()) + '.' + DEFAULT_EXCEL_EXTENSION
        convert(UPLOAD_PATH + f.filename, PROCESSED_PATH + output_file_name)

        session[SESSION_FILENAME_VARIABLE] = output_file_name
        return render_template('download.html')


@app.route('/download')
def download_file():
    output_file_name = session.get(SESSION_FILENAME_VARIABLE, None)
    output_file_path = PROCESSED_PATH + output_file_name
    if not output_file_name or not path.exists(output_file_path):
        return 'No file found'
    return send_file(output_file_path, as_attachment=True)


@app.route('/remove')
def remove_file():
    remove_all_files()
    return 'Files deleted'


if __name__ == '__main__':
    app.run()
