from flask import render_template, request, flash, url_for, redirect
from app import app
from .forms import AccountCreationForm, AddressForm
from flask_wtf.csrf import CsrfProtect
import requests


CsrfProtect(app)


''''
@csrf.error_handler
def csrf_error(reason):
	return render_template('csrf_error.html', reason=reason), 400
'''


@app.route('/')
@app.route('/index')
@app.route('/search')
def search():
	return render_template("search.html")


@app.route('/about')
def about():
	return render_template("about.html")


@app.route('/account', methods=['GET', 'POST'])
def account():
	userform = AccountCreationForm()
	addressform = AddressForm()
	if userform.validate_on_submit() & addressform.validate_on_submit():
		post_data = addressform.data
		post_data['key'] = ""

		# Add User to DB.

		# Add Info to UtilDB
		res = requests.post('http://140.160.142.77:5000/utilDB/add', data=post_data)
		return render_template('response.html', res=addressform)

	return render_template("account_creation.html", form=userform, addressform=addressform)


@app.route('/properties', methods=['GET'])
def properties():
	search_string = request.args.get('search_string')
	return render_template("properties.html", search_string=search_string)


@app.route('/test', methods=['POST'])
def test():
	account_data = request.args.get('account_data')
	return render_template("test.html", account_data=account_data)
