from flask import render_template, request
from app import app

@app.route('/')
@app.route('/index')
@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/account')
def account():
	return  render_template("account.html")

@app.route('/properties', methods=['GET'])
def properties():
	search_string = request.args.get('search_string')
	return render_template("properties.html", search_string=search_string)