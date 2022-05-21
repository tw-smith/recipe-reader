from flask import render_template, request
from app import app, parser as parser


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        parse = parser.VisionParser()
        parse.detect_text(file_path='./images/recipe_screenshot.png')
        parse.parse_text()
        parse.find_ingredients()
        ing_text = parse.return_for_flask()
        return render_template("index.html", ing_text=ing_text)
