from flask import render_template, request, flash, url_for, redirect
from app import app
from .forms import AccountCreationForm, AddressForm
from flask_wtf.csrf import CSRFProtect
import requests


CSRFProtect(app)


''''
@csrf.error_handler
def csrf_error(reason):
	return render_template('csrf_error.html', reason=reason), 400
'''


@app.route('/')
@app.route('/index')
@app.route('/search')
@app.route('/main')
def search():
	return render_template("search.html")


@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/privacy')
def privacy():
	return render_template("privacy.html")

@app.route('/terms')
def terms():
	return render_template("terms.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")


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


@app.route('/properties', methods=['GET', 'POST'])
def properties():
	search_string = request.args.get('search_string')
	if (search_string == ""):
		return render_template("properties.html", search_string=search_string)
	data = {
		"key" : "",
		"origins" : search_string
	}
	res = requests.post('http://140.160.142.77:5000/utilDB/query', data=data)
	addressData = res.json()
	return render_template("properties.html", search_string=search_string, addressData=addressData)

@app.route('/compare', methods=['GET'])
def compare():
	properties = request.args.get('properties').split(':')
	return render_template("compare.html", properties=properties)

@app.route('/test', methods=['POST'])
def test():
	account_data = request.args.get('account_data')
	return render_template("test.html", account_data=account_data)
