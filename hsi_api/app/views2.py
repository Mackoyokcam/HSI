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

@app.route('userDB/addUser', methods = ['POST'])
def addUser():
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
