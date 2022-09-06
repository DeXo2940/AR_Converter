import flask
import flask_cors
import werkzeug.utils
import os
import uuid
import ar_converter_engine

SESSION_FILENAME_VARIABLE = 'session_filename'
UPLOAD_PATH = 'uploads/'
PROCESSED_PATH = 'processed/'
NECESSARY_PATHS = [UPLOAD_PATH, PROCESSED_PATH]

DEFAULT_EXCEL_EXTENSION = 'xlsx'
ALLOWED_EXTENSIONS = [DEFAULT_EXCEL_EXTENSION]


def remove_all_files():
    for dest_path in NECESSARY_PATHS:
        if not os.path.exists(dest_path):
            continue
        filenames = next(os.walk(dest_path), (None, None, []))[2]
        for file in filenames:
            os.remove(dest_path + file)


def check_file_extension(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS


# Create necessary destinations if they don't exist
for destination_path in NECESSARY_PATHS:
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
remove_all_files()

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())  # 'super secret key'

if 'CORS_ORIGINS' in os.environ:
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = flask_cors.CORS(
        app, resources={r"/": {"origins": os.environ['CORS_ORIGINS']}})

app.config['UPLOAD_FOLDER'] = UPLOAD_PATH  # define upload path
# 50Kb # * 1024  # define max file size
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024


@app.route('/')
def upload_view():

    return flask.render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':  # check if the method is post
        f = flask.request.files['file']  # get the file from the files object
        if not check_file_extension(f.filename):
            return 'Invalid file type'
        f.filename = str(uuid.uuid4())
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], werkzeug.utils.secure_filename(
            f.filename)))  # this will secure the file
        output_file_name = str(uuid.uuid4()) + '.' + DEFAULT_EXCEL_EXTENSION
        ar_converter_engine.convert(
            UPLOAD_PATH + f.filename, PROCESSED_PATH + output_file_name)

        flask.session[SESSION_FILENAME_VARIABLE] = output_file_name
        return flask.render_template('download.html')


@app.route('/download')
def download_file():
    output_file_name = flask.session.get(SESSION_FILENAME_VARIABLE, None)
    output_file_path = PROCESSED_PATH + output_file_name
    if not output_file_name or not os.path.exists(output_file_path):
        return 'No file found'
    return flask.send_file(os.path.join(os.getcwd(), output_file_path), as_attachment=True)


@app.route('/remove')
def remove_file():
    remove_all_files()
    return 'Files deleted'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
