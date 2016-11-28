from flask import Flask, send_file
import os
import sys
lib_path = os.path.abspath(os.path.join('pipeline', 'src'))
sys.path.append(lib_path)
from flask import (Flask,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   send_from_directory,
                   jsonify)
import utils.web as web
app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['mat', 'csv', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/analyze_data', methods=['GET', 'POST'])
def analyze_data():
    if request.method == 'POST':
        file_name = request.json['name']
        out = web.make_meda_html(file_name)
        res = web.save_analysis(out, file_name)
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

@app.route("/")
def main():
    return send_file('./static/index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
