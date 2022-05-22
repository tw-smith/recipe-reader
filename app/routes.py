from flask import render_template, request, redirect, flash, abort
from werkzeug.utils import secure_filename
from app import app, parser as parser
from app.forms import UploadForm
import os
import imghdr


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    stream_format = imghdr.what(None, header)
    if not stream_format:
        return None
    return '.' + (stream_format if stream_format != 'jpeg' else 'jpg')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # TODO: more robust validation and error messages
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(f.stream) or \
                    f.content_length > app.config['MAX_CONTENT_LENGTH']:
                abort(400)
            save_filename = app.config['UPLOAD_FOLDER'] + filename
            f.save(save_filename)
            flash("File uploaded!")
            parse = parser.VisionParser()
            parse.detect_text(file_path=save_filename)
            parse.parse_text()
            parse.find_ingredients()
            ing_text = parse.return_for_flask()
            return render_template("displaylist.html", ing_text=ing_text)

    if request.method == 'GET':
        form = UploadForm()
        return render_template("uploadform.html", form=form)
