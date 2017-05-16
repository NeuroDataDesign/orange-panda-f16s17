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
app = Flask(__name__)

from utils.utils import utils as ut # this is gross

ALLOWED_EXTENSIONS = set(['mat', 'csv', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/gets3', methods=['GET', 'POST'])
def get_s3():
  if request.method == 'POST':
    print 'executing thing'
    cmd = 'python batch/test_front.py --bucket %s --dataset %s --credentials %s --subject %s --session %s'
    cmd = cmd % ('neurodatadesign-test', 'small_test_set', '${HOME}/.aws/credentials.csv', '0001', '02')
    ut().execute_cmd(cmd)
    return 'did the thing'
  else:
    abort(400)


@app.route("/")
def main():
    return send_file('./static/index.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=80)
