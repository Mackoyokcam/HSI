from app import app
from app import hsi_api
import json
import usaddress as usad
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

'''''
Format for Query can be multiple origin addresses, such that:
 origins="address1:address2:address3"

OR format can be json String that is a Google geocode result (See Google's Geocode API for details).

If both or neither origins and geocode contains data, utilQuery will return a FORMAT_ERROR

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
                geo = api.get_location_data(i)
                geo = json.loads(geo)
                if "status" in geo:
                    coordinates.update({"status": geo["status"]})
                else:
                    addr = geo['results'][0]['address_components']
                    coordinates.update({"address":geo['results'][0]['address']})
                    for j in addr:
                        if 'subpremise' in j['types']:
                            coordinates.update({'apt':j['short_name']})
                            break
                    coordinates.update({"lat":geo['results'][0]["lat"]})
                    coordinates.update({"long":geo['results'][0]["lng"]})
                locations.append(coordinates)
            result = str(api.utilQuery(locations, None)).replace('\'', '\"')
            return result.replace('""', '"')
    return FORMAT_ERROR



'''''
Converts param_keys into a dict with all the needed values.
A Sanity check is performed before utilCombine is called, so none is necessary here (except in the case of the geocode errors)
'''''
def utilCombine(param_keys):
    data = {}
    add = request.form['address'] + " "
    
    apt = request.form['apt']
    if apt != 'N/A':
        add += "apt " + apt + " "
    add += request.form['city'] + " "
    add += request.form['state'] + " "
    add += request.form['zip']

    api = hsi_api.Hsi_Api(CONFIG_FILE_URL)    
    geo = json.loads(api.get_location_data(add))

    if "status" not in geo:       
        data.update({"lat":geo['results'][0]["lat"]})
        data.update({"long":geo['results'][0]["lng"]})
        result = geo['results'][0]['address_components']
        
        for i in result:
            if "subpremise" in i['types']:
                data.update({"apt":i["short_name"]})
            elif "street_number" in i['types'] :
                if "address" in data:
                    data["address"] = i["short_name"]+" "+data["address"]
                else:
                    data.update({"address":i["short_name"]})
            elif "route" in i["types"] :
                if "address" in data:
                    data["address"] = data["address"] + " " + i["short_name"]
                else:
                    data.update({"address": i["short_name"]})
            elif "locality" in i['types']:
                data.update({"city":i['short_name']})
            elif "administrative_area_level_1" in i['types']:
                data.update({"state": i['short_name']})
            elif "postal_code" in i['types']:
                data.update({"zip": i['short_name']})
        
        
        if "apt" not in data:
            data.update({"apt": "N/A"})
    else:
        return geo #Google geocode error
    
    data.update({"updateDate":request.form['updateDate']})
    data.update({"rent":request.form['rent']})
    data.update({"gas":request.form['gas']})
    data.update({"water":request.form['water']})
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
    result = {}
    if 'key' not in param_keys or ('key' in param_keys and valid(request.form['key']) == False):
        return VALIDATION_ERROR    
    if utilAddSanity(param_keys):
        util_info = utilCombine(param_keys)
        if "status" in util_info:
            return '{"error": "' + util_info["status"] + '"}'
        res = api.utilAdd(util_info)
        if "error" in res:
            return str(res) 
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


@app.route('/userDB/addUser', methods = ['POST'])
def addUser():
    return "test"
    #param_keys = MultiDict.to_dict(request.form)                                                                                                                                             
    #api = hsi_api.                                                                                                                                                                           
    Email = request.form['Email']
    Password = request.form['Password']
    Street = request.form['Street']
    City = request.form['City']
    State = request.form['State']
    Zip = request.form['Zip']
    Apt = request.form['Apt']
    res = hsi_api_user.addUser(Email,Password, Street, City, State, Zip, Apt)
    if (res == -1):
        return "user already in database"
    elif (res == -2):
        return "address already in database"
    else
        return "user added to database"
