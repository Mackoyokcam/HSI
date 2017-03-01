from flask import render_template, request, flash, url_for, redirect, jsonify
from app import app
from .forms import AccountCreationForm, AddressForm, Login, OriginCompareForm, DestinationCompareForm
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
# from .redirects import get_redirect_target, redirect_back
import requests
import json
import time


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
	searchString = request.args.get('search_string')
	if (searchString == ""):
		return render_template("properties.html", search_string=search_string)
	data = {
		"key" : "",
		"origins" : searchString
	}
	# res = requests.post('http://140.160.142.77:5000/utilDB/query', data=data)
	testingDataSingleUnit = {"addr0": {"walkscore": {"status": "Key is invalid"},
									   "status": "True",
									   "units": {"N/A": {"rent": "500.0",
									   					 "gas": "10.0",
									   					 "lat": 48.7228498,
									   					 "compost": "False",
									   					 "long": -122.4862003,
									   					 "electrical": "10.0",
									   					 "updateDate": "2017.02.14",
									   					 "recycle": "False",
									   					 "water": "10.0"}}}}
	testingDataMultiUnit = {"addr0": {"walkscore": {"status": "Key is invalid"},
									   "status": "True",
									   "units": {"N/A": {"rent": "500.0",
									   					 "gas": "10.0",
									   					 "lat": 48.7228498,
									   					 "compost": "False",
									   					 "long": -122.4862003,
									   					 "electrical": "10.0",
									   					 "updateDate": "2017.02.14",
									   					 "recycle": "False",
									   					 "water": "10.0"},
									   			 "B201" : {"rent": "350.0",
									   					 "gas": "45.0",
									   					 "lat": 48.7228498,
									   					 "compost": "True",
									   					 "long": -122.4862003,
									   					 "electrical": "34.0",
									   					 "updateDate": "2017.02.14",
									   					 "recycle": "True",
									   					 "water": "15.0"}}}}
	
	# addressData = testingDataSingleUnit
	addressData = testingDataMultiUnit
	jsonUnitData = json.dumps(addressData["addr0"]["units"])
	print(jsonUnitData)
	# addressData = res.json()
	# NOTE: this is kind of hacky but it's only temporary until we figure out
	# some data formatting issues with the back end
	if addressData['addr0']['status'] == 'True':
		addressData = addressData['addr0']
		if len(addressData["units"]) > 1:
			# extract just the values of the first (and only) unit
			# singleUnit = list(addressData["units"])[0]
			# addressData = list(addressData["units"].values())[0]
			# print(addressData)
			multiUnit = "yep"
			return render_template("properties.html", searchString=searchString,
								   addressData=addressData, multiUnit=multiUnit, jsonUnitData=jsonUnitData)
		else:
			return render_template("properties.html", searchString=searchString,
								   addressData=addressData, jsonUnitData=jsonUnitData)
	else:
		return render_template("properties.html", searchString=searchString)


# for just viewing the json results of querying the database
@app.route('/simplesearch', methods=['GET'])
def simplesearch():
	search_string = request.args.get('search_string')
	if (search_string == "" or search_string == None):
		return render_template("simplesearch.html")
	data = {
		"key" : "",
		"origins" : search_string
	}
	res = requests.post('http://140.160.142.77:5000/utilDB/query', data=data)
	addressData = res.json()
	return render_template("simplesearch.html", addressData=addressData)

# for adding to the db without having to wget
@app.route('/simpleadd', methods=['GET'])
def simpleadd():
	if 'address' in request.args:
		data = {
			"key" : "",
			"updateDate" : time.strftime("%Y.%m.%d"),
			"address" : request.args.get('address'),
			"city" : request.args.get('city'),
			"state" : request.args.get('state'),
			"zip" : request.args.get('zip'),
			"apt" : request.args.get('apt'),
			"rent" : request.args.get('rent'),
			"gas" : request.args.get('gas'),
			"electrical" : request.args.get('electrical'),
			"water" : request.args.get('water'),
			"recycle" : request.args.get('recycle'),
			"compost" : request.args.get('compost')
		}
		res = requests.post('http://140.160.142.77:5000/utilDB/add', data=data)
		responseText = res.text
		return render_template("simpleadd.html", responseText=responseText)
	else:
		return render_template("simpleadd.html")


@app.route('/compare', methods=['GET', 'POST'])
def compare():
	# properties = request.args.get('properties').split(':')
	compareForm1 = OriginCompareForm(csrf_enabled=False)
	compareForm2 = DestinationCompareForm(csrf_enabled=False)
	if compareForm1.validate_on_submit() & compareForm2.validate_on_submit():
		compare_post_data = {}
		compare_post_data['origins'] = compareForm1.address1.data + ' ' + compareForm1.city1.data + ' ' \
										   + compareForm1.state1.data + ' ' + compareForm1.zip1.data

		compare_post_data['destinations'] = compareForm2.address2.data + ' ' + compareForm2.city2.data + ' ' \
												+ compareForm2.state2.data + ' ' + compareForm2.zip2.data

		compare_post_data['key'] = ''

		# Send compare request
		compare_result = requests.post('http://140.160.142.77:5000/compare', data=compare_post_data)

		# test bin
		# compare_result = requests.post('http://requestb.in/13h5mjd1', data=compare_post_data)

		# test data
		#compare_result = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
		#json.dumps(compare_result)

		return render_template('response.html', result=compare_result)

	return render_template("compare.html", formOrigin=compareForm1, formDestination=compareForm2) #properties=properties


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

