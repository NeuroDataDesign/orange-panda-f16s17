import sys
from app import app
if len(sys.argv) > 1:
    app.run(host='0.0.0.0', port=80)
else:
    app.run(debug=True)
