from flask import render_template, request, flash, url_for, redirect, jsonify
from app import app
from .forms import AccountCreationForm, AddressForm, Login, OriginCompareForm, DestinationCompareForm
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
# from .redirects import get_redirect_target, redirect_back
import requests
import json
import time
from collections import OrderedDict

# CSRFProtect(app)


''''
@csrf.error_handler
def csrf_error(reason):
	return render_template('csrf_error.html', reason=reason), 400
'''

# custom jinja2 filters:

# reverse of the built in |tojson filter
@app.template_filter()
def fromjson(jsonString):
	print(jsonString)
	return json.loads(jsonString)

# routes
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
	loginform = Login()
	if userform.validate_on_submit() & addressform.validate_on_submit():
		user_post_data = userform.data
		user_post_data['Street'] = addressform.address.data
		user_post_data['City'] = addressform.city.data
		user_post_data['State'] = addressform.state.data
		user_post_data['Zip'] = addressform.zip.data
		user_post_data['Apt'] = addressform.apt.data
		util_post_data = addressform.data
		user_post_data['key'] = ''
		util_post_data['key'] = ''

		# Add User to DB.
		user_result = requests.post('http://140.160.142.77:5000/userDB/addUser', data=user_post_data)
		# user_result = requests.post('http://requestb.in/1d62yzd1', data=user_post_data)
		print(user_result)
		# Add Info to UtilDB
		# string_result = requests.post('http://140.160.142.77:5000/utilDB/add', data=util_post_data)
	 
				
		# util_add = string_result.json()
		# temp_result = string_result.json()
		#user_temp_result = string_result.json()
		# util_add = json.dumps(temp_result)
		# util_add = json.dumps(temp_result)

		# test bin
		# util_add = requests.post('http://requestb.in/16s31qr1', data=util_post_data)
		return render_template('search.html') #add user_add=useradd

		#return render_template('add_response.html', utilData=util_add) #add user_add=useradd

	return render_template("account_creation.html", form=userform, addressform=addressform, loginform=loginform)


@app.route('/account_view', methods=['GET', 'POST'])
@login_required
def account_view():
	# code for viewing account
	# If user is not authenticated, send to account creation page.
	# If authenticated, show account info.
	return render_template("account.html")

# This is the main page for displaying map and utility data for a given
# property
@app.route('/properties', methods=['GET', 'POST'])
def properties():
	DEBUG = True
	searchString = request.args.get('searchString')
	if (searchString == ""):
		return render_template("properties.html", searchString=searchString)
	data = {
		"key" : "",
		"origins" : searchString
	}
	res = requests.post("http://140.160.142.77:5000/utilDB/query", data=data)

	# dummy data for offline testing
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
	
	testingNearbyData = '{"lat":"48.722849", "long":"-122.502782"}'
	# addressData = testingDataSingleUnit
	# addressData = testingDataMultiUnit
	if DEBUG:
		print (res.text)
	addressData = fromjson(res.text.replace("'", '"'))
	if "error" in addressData:
		errorMessage = addressData["error"]
		return render_template("errors.html", errorMessage=errorMessage)
	else:
		if addressData["status"] == "True": # i.e. the db contained a valid entry
			# testingNearbyData = fromjson(testingNearbyData)
			data = {
				"lat" : addressData["lat"],
				"long" : addressData["long"],
				"key" : ""
			}
			# data = {
			# 	"lat" : "48.722849",
			# 	"long" : "-122.502782",
			# 	"key" : ""
			# }
			res = requests.post("http://140.160.142.77:5000/utilDB/area", data=data)
			if DEBUG:
				print (res.text)
			nearbyData = fromjson(res.text.replace("'", '"'))
			nearbyData = json.dumps(nearbyData)
			multiUnit = "False"
			if len(addressData["units"]) > 1:
				multiUnit = "True"
			addressData = json.dumps(addressData["units"])
			return render_template("properties.html", searchString=searchString,
									   addressData=addressData, nearbyData=nearbyData, multiUnit=multiUnit)
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


@app.route('/distance', methods=['GET', 'POST'])
def distance():
	return render_template('distance.html')

def queryAddress(address):
	data = {
		"key" : "",
		"origins" : address
	}
	res = requests.post("http://140.160.142.77:5000/utilDB/query", data=data)
	addressData = fromjson(res.text.replace("'", '"'))
	if addressData["status"] == True:
		return addressData
	else:
		return None

@app.route('/comparisons', methods=['GET'])
def comparisons():
	addresses = [];
	for i in range(1, 5):
		field = "field-" + str(i)
		if field != "" in request.args:
			param = request.args.get(field)
			if param != "":
				query = queryAddress(param)
				if query is None:
					addresses.append("No Data Available")
				else:
					firstApt = next(iter(query["units"]))
					unit = query["units"][firstApt]
					addresses.append({"address": query["address"], "apartment": firstApt, "data": unit})
	if len(addresses) == 0:
		return render_template("comparisons.html")
	else:
		return render_template("comparisons.html", addresses=addresses)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
	# properties = request.args.get('properties').split(':')
	compareForm1 = OriginCompareForm()
	compareForm2 = DestinationCompareForm()
	if compareForm1.validate_on_submit() & compareForm2.validate_on_submit():
		compare_post_data = {}
		compare_post_data['origins'] = compareForm1.address1.data + ' ' + compareForm1.city1.data + ' ' \
										   + compareForm1.state1.data + ' ' + compareForm1.zip1.data

		compare_post_data['destinations'] = compareForm2.address2.data + ' ' + compareForm2.city2.data + ' ' \
												+ compareForm2.state2.data + ' ' + compareForm2.zip2.data

		compare_post_data['key'] = ''

		# Send compare request
		string_result = requests.post('http://140.160.142.77:5000/compare', data=compare_post_data)
		temp_result = string_result.json()

		# test bin
		# compare_result = requests.post('http://requestb.in/13h5mjd1', data=compare_post_data)

		# dummy data
		temp_result = '''{'google': \
							{'destination_addresses': ['18113 31st Ave NE, Arlington, WA 98223, USA'], \
							'status': 'OK', \
							'rows': [{'elements': \
									[{'status': 'OK', \
									'distance': {'value': 88050, \
										'text': '54.7 mi'}, \
 									'duration': {'value': 65273, \
										'text': '18 hours 8 mins'} \
									}] \
								}], \
							'origin_addresses': ['355 Meadowbrook Ct, Bellingham, WA 98226, USA'] \
							}, \
						'hsi_db': \
							{'addr': \
								{'results': \
									{'water': '30.0', \
									'lat': 48.8088895, \
									'updateDate': '2017.03.01', \
									'address': '355 Meadowbrook Ct', \
									'city': 'Bellingham', \
									'state': 'WA', \
									'compost': 'True', \
									'long': -122.5002452, \
									'electrical': '90.0', \
									'gas': '50.0', \
									'rent': '900.0', \
									'apt': 'N/A', \
									'zip': '98226', \
									'recycle': 'True' \
								}, \
							'status': 'True'}}}'''

		compare_result = json.dumps(temp_result)

		return render_template('response.html', compareData=compare_result)

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
		#user_data = loginform.data
		# requires user class import and API call function.
		'''
		user = requests.get('http://140.160.142.77:5000/login', data=user_data)
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


@app.route('/test2', methods=['GET', 'POST'])
def test2():
	send_this = request.get_json()
	print(send_this)
	#temp_result = requests.post('http://requestb.in/1cf0mp11', data=temp_data)
	temp_result = requests.post('http://140.160.142.77:5000/compare', data=send_this)
	string_result = temp_result.text
	print(string_result)	
	#compare_result = json.loads(string_result)
	return string_result
