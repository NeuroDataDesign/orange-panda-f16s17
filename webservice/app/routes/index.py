import os
import sys
lib_path = os.path.abspath(os.path.join('..', 'pipeline', 'src'))
sys.path.append(lib_path)
from app import app
from flask import (Flask,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   send_from_directory,
                   jsonify)
import utils.web as web

ALLOWED_EXTENSIONS = set(['mat', 'csv', 'txt'])
@app.route('/')
def root():
    return app.send_static_file('views/index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/analyze_data', methods=['GET', 'POST'])
def analyze_data():
    if request.method == 'POST':
        patient = request.json['name']
        out = web.make_meda_html(patient)
        res = web.save_analysis(out, patient)
        return jsonify(res)
    else:
	   abort(404)

@app.route('/gets3', methods=['GET', 'POST'])
def get_s3():
    if request.method == 'POST':
        return web.get_s3(request.json)
    else:
	abort(400)

@app.route('/getTable', methods=['GET'])
def get_table_data():
    return jsonify(web.populate_table())

