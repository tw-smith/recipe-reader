from flask import render_template, request, redirect, flash, abort
from werkzeug.utils import secure_filename
from app import app, parser as parser
from app.forms import UploadForm
import os
from os.path import exists
import imghdr
import json


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    stream_format = imghdr.what(None, header)
    if not stream_format:
        return None
    else:
        if stream_format == 'jpeg':
            stream_format = 'jpg'
    return '.' + (stream_format)


def next_filename(path):
    counter_file_path = path + "counter.txt"
    if exists(counter_file_path):
        with open(counter_file_path, "r") as counter:
            count = int(counter.read())
            count += 1
        with open(counter_file_path, "w") as counter:
            counter.write(str(count))
    else:
        count = 1
        with open(counter_file_path, "w") as counter:
            counter.write(str(count))
    return str(count)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # TODO: more robust validation and error messages
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext == '.jpeg':
                file_ext = '.jpg'
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(f.stream) or \
                    f.content_length > app.config['MAX_CONTENT_LENGTH']:
                abort(400)
            save_filename = next_filename(app.config['OUTPUT_FOLDER'])
            img_filename = app.config['OUTPUT_FOLDER'] + save_filename + file_ext
            txt_filename = app.config['OUTPUT_FOLDER'] + save_filename + '.txt'
            f.save(img_filename)
            flash("File uploaded!")
            parse = parser.VisionParser()
            parse.detect_text(file_path=img_filename)
            parse.parse_text()
            parse.find_ingredients()
            ing_text = parse.return_for_flask()
            with open(txt_filename, "w") as output:
                output.write(json.dumps(ing_text, indent=6))
            return render_template("displaylist.html", ing_text=ing_text, file_number=save_filename)

    if request.method == 'GET':
        form = UploadForm()
        return render_template("uploadform.html", form=form)
