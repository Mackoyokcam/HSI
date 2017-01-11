from app import app
from app import hsi_api
import json
from flask import request
from werkzeug.datastructures import MultiDict

CONFIG_FILE_URL = "app/config.json"
VALIDATION_ERROR = '{"error": "validation failed, make sure you are not above your api request limit and that your key is valid"}'
FORMAT_ERROR = '{"error": "Formatting is incorrect"}'
ADD_ERROR = '{"error": "Error in adding entry to database"}'
WRITE_ERROR = '{"error": "Error writing to DB"}'
LIMIT_EXCEEDED = '{"error": "Too many queries"}'

'''
compare

Each parameter needs to be sent over in a post request

:param origins
:type string

:param destinations
:type string

:param key
:string

'''


@app.route('/compare',methods=['POST'])
def compare():
    param_keys = MultiDict.to_dict(request.form).keys()
    print(param_keys)
    print(MultiDict.to_dict(request.form))
    if 'key' not in param_keys or ('key' in param_keys and valid(request.form['key']) == False):
        return VALIDATION_ERROR
    else:
        print(param_keys is not None)
        print('key' in param_keys)
        print('origins' in param_keys)
        print('destinations' in param_keys)
        if param_keys is not None and 'origins' in param_keys and 'destinations' in param_keys:
            destinations = request.form['destinations'].split(':')
            origins = request.form['origins'].split(':')
            print(origins,destinations)
            if type(origins) is list and type(destinations) is list:
                api = hsi_api.Hsi_Api(CONFIG_FILE_URL)
                response = api.compare(origins, destinations)
                return response
    return FORMAT_ERROR

######################################################
'''''
Format for Query can be multiple origin addresses, such that:
 origins="address1:address2:address3"

Returns a string consisting of dicts, separated by the : character
'''''
@app.route('/utilDB/query', methods = ['POST'])
def utilQuery():
    param_keys = MultiDict.to_dict(request.form).keys()
    if 'key' not in param_keys or ('key' in param_keys and valid(request.form['key']) == False):
        return VALIDATION_ERROR
    if 'origins' in param_keys:
        origins = request.form['origins']
        origins = origins.split(":")
        if type(origins) is list and not None:
            api = hsi_api.Hsi_Api(CONFIG_FILE_URL)
            locations = list()
            for i in origins:
                coordinates = {}
                geo = json.loads(api.get_location_data(i))
                if "status" in geo:
                    coordinates.update({"status": geo["status"]})
                else:
                    geo = geo["results"]
                    coordinates.update({"lat":geo[0]["lat"]})
                    coordinates.update({"long":geo[0]["lng"]})
                locations.append(coordinates)
            result = api.utilQuery(locations)
            return str(result)
    return FORMAT_ERROR
    
'''''
Converts param_keys into a dict with all the needed values.
A Sanity check is performed before utilCombine is called, no none is necessary here (except in the case of the geocode errors)
'''''
def utilCombine(param_keys):
    data = {}
    data.update({"address":request.form['address']})
    data.update({"city":request.form['city']})
    data.update({"state":request.form['state']})
    data.update({"zip":request.form['zip']})
    add = data["address"] + " " + data["city"] + " " + data["state"] + " " + data["zip"]
    api = hsi_api.Hsi_Api(CONFIG_FILE_URL)    
    geo = json.loads(api.get_location_data(add))

    if "status" not in geo:
        result = geo["results"]
        data.update({"lat":result[0]["lat"]})
        data.update({"long":result[0]["lng"]})
    else:
        return geo #Google geocode error
    
    data.update({"apt":request.form['apt']})
    data.update({"updateDate":request.form['updateDate']})
    data.update({"rent":request.form['rent']})
    data.update({"gas":request.form['gas']})
    data.update({"water":request.form['water']})
    data.update({"heating":request.form['heating']})
    data.update({"electrical":request.form['electrical']})
    data.update({"recycle":request.form['recycle']})
    data.update({"compost":request.form['compost']})
    
    return data


'''''
Format for POST call for add should include all entries matching the attributes used in utilCombine. This is checked in utilAddSanity, and will not continue if any attributes are missing/misspelled/etc.
lat and long are calculated by Google's geocoding, and should not be provided.

Returns "True" upon success
NOTE: Does not deal with duplicate key errors yet
'''''
@app.route('/utilDB/add', methods = ['POST'])
def utilAdd():
    param_keys = MultiDict.to_dict(request.form).keys()
    api = hsi_api.Hsi_Api(CONFIG_FILE_URL)
    if 'key' not in param_keys or ('key' in param_keys and valid(request.form['key']) == False):
        return VALIDATION_ERROR    
    if utilAddSanity(param_keys):
        util_info = utilCombine(param_keys)
        if "status" in util_info:
            return '{"error": "'+ util_info["status"] + '"}'
        res = api.utilAdd(util_info)
        if res is False:
            return WRITE_ERROR 
        return '{"status":"True"}'
    return FORMAT_ERROR

'''
utilAdd sanity check, to make sure all relevent keys are in param_keys
'''
def utilAddSanity(param_keys):
    if param_keys is not None and 'address' in param_keys and \
       'city' in param_keys and \
       'state' in param_keys and \
       'zip' in param_keys and \
       'apt' in param_keys and \
       'updateDate' in param_keys and \
       'rent' in param_keys and \
       'gas' in param_keys and \
       'water' in param_keys and \
       'heating' in param_keys and \
       'electrical' in param_keys and \
       'recycle' in param_keys and \
       'compost' in param_keys:
        return True
    return False

'''
valid

This should check to make sure that the application making the request is an authorized application
and that is has not exceeded its request limit; only then should it return true.

NOTE:
Just a passthrough at this point

:param api_key
:type string

:returns True
:returns False
'''


def valid(api_key):
    return True
