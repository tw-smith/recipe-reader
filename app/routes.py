from flask import render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from app import app, parser as parser
from app.forms import UploadForm
import os


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            save_filname = app.config['UPLOAD_FOLDER'] + filename
            f.save(save_filname)
            flash("File uploaded!")
            parse = parser.VisionParser()
            parse.detect_text(file_path=save_filname)
            parse.parse_text()
            parse.find_ingredients()
            ing_text = parse.return_for_flask()
            return render_template("displaylist.html", ing_text=ing_text)
        #return redirect(request.url)

    if request.method == 'GET':
        form = UploadForm()
        return render_template("uploadform.html", form=form)
