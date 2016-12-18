from app import app
from app import hsi_api
import json
from flask import request
from werkzeug.datastructures import MultiDict

CONFIG_FILE_URL = "app/config.json"
VALIDATION_ERROR = '{"error": "validation failed, make sure you are not above your api request limit and that your key is valid"}'
FORMAT_ERROR = '{"error": "Formatting is incorrect"}'

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
