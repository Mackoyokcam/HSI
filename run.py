#!flask/bin/python
from app import app
<<<<<<< HEAD
app.run(host='0.0.0.0', port=80, debug=True)
=======
app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
>>>>>>> 2824d6767dd459f1397fe0cb1aa4923a76f42103
# app.run(debug=True, threaded=True)
