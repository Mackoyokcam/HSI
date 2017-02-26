from flask import render_template, request, flash, url_for, redirect
from app import app
from .forms import AccountCreationForm, AddressForm, Login, AddressCompareForm
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
# from .redirects import get_redirect_target, redirect_back
import requests


# CSRFProtect(app)


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
	userform = AccountCreationForm(csrf_enabled=False)
	addressform = AddressForm(csrf_enabled=False)
	loginform = Login(csrf_enabled=False)
	if userform.validate_on_submit() & addressform.validate_on_submit():
		user_post_data = {}
		util_post_data = addressform.data
		util_post_data['key'] = ''

		# Add User to DB.
		# user_add = requests.post('http://140.160.142.77:5000/<insert user add call>', data=post_data)

		# Add Info to UtilDB
		util_add = requests.post('http://140.160.142.77:5000/utilDB/add', data=util_post_data)

		# test bin
		# util_add = requests.post('http://requestb.in/16s31qr1', data=util_post_data)

		return render_template('response.html', util_add=util_add) #add user_add=useradd

	return render_template("account_creation.html", form=userform, addressform=addressform, loginform=loginform)


@app.route('/account_view', methods=['GET', 'POST'])
@login_required
def account_view():
	# code for viewing account
	# If user is not authenticated, send to account creation page.
	# If authenticated, show account info.
	return render_template("account.html")


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
	# NOTE: this is kind of hacky but it's only temporary until we figure out
	# some data formatting issues with the back end
	if 'status' in addressData['addr0']:
		return render_template("properties.html", search_string=search_string)
	addressData = addressData['addr0']
	return render_template("properties.html", search_string=search_string, addressData=addressData)


# for just viewing the json results of querying the database
@app.route('/simple', methods=['GET'])
def simple():
	search_string = request.args.get('search_string')
	if (search_string == "" or search_string == None):
		return render_template("simple.html")
	data = {
		"key" : "",
		"origins" : search_string
	}
	res = requests.post('http://140.160.142.77:5000/utilDB/query', data=data)
	addressData = res.json()
	return render_template("simple.html", addressData=addressData)


@app.route('/compare', methods=['GET', 'POST'])
def compare():
	# properties = request.args.get('properties').split(':')
	compareForm = AddressCompareForm(csrf_enabled=False)
	if compareForm.validate_on_submit():
		compare_post_data = {}
		compare_post_data['origins'] = compareForm.address1.data + ' ' + compareForm.city1.data + ' ' \
									   + compareForm.state1.data + ' ' + compareForm.zip1.data

		compare_post_data['destinations'] = compareForm.address2.data + ' ' + compareForm.city2.data + ' ' \
											+ compareForm.state2.data + ' ' + compareForm.zip2.data

		compare_post_data['key'] = ''

		# Send compare request
		compare_result = requests.post('http://140.160.142.77:5000/compare', data=compare_post_data)

		# test bin
		# compare_result = requests.post('http://requestb.in/13h5mjd1', data=compare_post_data)

		return render_template('response.html', util_add=compare_result)

	return render_template("compare.html", form=compareForm) #properties=properties


@app.route('/test', methods=['POST'])
def test():
	account_data = request.args.get('account_data')
	return render_template("test.html", account_data=account_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
	userform = AccountCreationForm(csrf_enabled=False)
	addressform = AddressForm(csrf_enabled=False)
	loginform = Login(csrf_enabled=False)

	if loginform.validate_on_submit():

		# requires user class import and API call function.
		'''
		user = requests.get('http://140.160.142.77:5000/<userdb function>', data=user_data)
		if get request for user successful...
			login_user(user)
			flash('Logged in successfully.')
		'''

		# Change to go to account page instead.
		return render_template('search.html')

	return render_template("account_creation.html", form=userform, addressform=addressform, loginform=loginform,
						   login_error = True)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
	# logout(user)
	return render_template("search.html")

