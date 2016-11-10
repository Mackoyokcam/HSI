from flask import render_template
from app import app

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/search', methods=['GET'])
def search():
	return render_template("search.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/account')
def account():
	return  render_template("account.html")

@app.route('/properties/<property_string>')
def properties(property_string=""):
	return render_template("properties.html", property_string=property_string)
