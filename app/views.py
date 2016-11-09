from flask import render_template
from app import app

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/search', methods=['GET'])
def search():
	return render_template("search.html")