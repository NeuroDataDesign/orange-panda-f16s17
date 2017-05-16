from flask import Flask, send_file
import os
import sys
import json

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
  data = json.loads(request.data.decode())
  if request.method == 'POST':
    print 'executing thing'
    cmd = 'python batch/create_job.py --bucket %s --dataset %s --credentials %s'
    cmd = cmd % (data['bucket'], data['fpath'], '${HOME}/.aws/credentials.csv')
    ut().execute_cmd(cmd)
    return 'Data submitted'
  else:
    abort(400)


@app.route("/")
def main():
    return send_file('./static/index.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True, port=80)
