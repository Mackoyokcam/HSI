#!flask/bin/python
from app import app
app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
# app.run(debug=True, threaded=True)

