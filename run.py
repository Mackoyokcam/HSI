#!flask/bin/python
from app import app
app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
# app.run(debug=True, threaded=True)
