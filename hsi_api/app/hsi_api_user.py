from pymongo import MongoClient
import datetime
import pprint
import json
client = MongoClient()
userDB = client.test_database
users = userDB.test_collection
# to do
 # (done) add Aparement functions
 # add 3 month inactivity function
def addUser(email, password, street, city, state, zipCode, apt):
    checkEmail = users.find_one({"Email" : email})
    checkAddy = users.find_one({"Street" : street, "City" : city, "State" : state, "Zip" : zipCode, "Apt" : apt})
    if (checkEmail != None):
        #print("email is already in database")
        return -1
    elif (checkAddy != None):
        #print("only 1 address per email please")
        return -2
    else:
        new_user = {"Email" : email,
            "Password" : password,
            "Street" : street,
            "City" : city,
            "State" : state,
            "Zip" : zipCode,
            "Apt" : apt,
            "Last_Login" : datetime.datetime.utcnow()}
    result = users.insert_one(new_user)
    #print("success adding user to database")
    return 1
def changePassword(email, oldPass, newPass):
    result = users.find_one({"Email" : email, "Password" : oldPass})
    if (result == None):
        #print("email verification unsuccessful")
        return -1
    else:
        users.update(
            { "Email" : email },
            {
                 '$set': 
                  { 'Password' : newPass}
            }
         )
        return 1
def changeStreet(email, newStreet):
    result = users.find_one({"Email" : email})
    if (result == None):
        # print("email verification unsuccessful")
        return -1
    else:
        users.update(
            { "Email" : email},
            {
                '$set': {'Street': newStreet}
            }   
        )
        return 1
def changeZip(email, newZip):
    result = users.find_one({"Email" : email})
    if (result == None):
        #print ("email verification unsuccessful")
        return -1
    else:
        users.update(
            { "Email" : email},
            {
                '$set': {'Zip': newZip}
            }
        )
        return 1
def changeApt(email, newApt):
    result = users.find_one({"Email" : email})
    if (result == None):
        #print ("email verification unsuccessful")
        return -1
    else:
        users.update(
            { "Email" : email},
            {
                '$set': {"Apt": newApt}
            }
        )
def removeAccount(email):
    result = users.find_one({"Email" : email})
    if (result == None):
        #print ("email verification unsuccessful")
        return -1
    else:                    
        users.remove({ 'Email' : email})
        return 1
def login(email, password):
    result = users.find_one({"Email" : email, "Password" : password})
    if (result == None):
        #print("unsuccessful login attempt")
        return -1
    else:
        users.update(
            { "Email" : email},
            {
                '$set' : { 'Last_Login' : datetime.datetime.utcnow()}
            }
        )
        return 1
def getUserEmail(email):
    checker = list(users.find({"Email" : email},{"Email": email, "_id":0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONemail = json.loads(conversion2)
        return JSONemail
def getUserStreet(email):
    checker = list(users.find({"Email": email},{"Email":0,  "_id":0, "Password":0, "City":0, "State":0, "Zip":0,"Last_Login":0, "Apt":0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONstreet = json.loads(conversion2)
        return JSONstreet
def getUserCity(email):
    checker = list(users.find({"Email": email},{"Email":0,  "_id":0, "Password":0, "Street":0, "State":0, "Zip":0,"Last_Login":0, "Apt":0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONcity = json.loads(conversion2)
        return JSONcity
def getUserState(email):
    checker = list(users.find({"Email": email},{"Email":0,  "_id":0, "Password":0, "City":0, "Street":0, "Zip":0,"Last_Login":0, "Apt": 0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONstate = json.loads(conversion2)
        return JSONstate
def getUserZip(email):
    checker = list(users.find({"Email": email},{"Email":0,  "_id":0, "Password":0, "City":0, "State":0, "Street":0,"Last_Login":0, "Apt":0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONzip = json.loads(conversion2)
        return JSONzip

def getUserApt(email):
    checker = list(users.find({"Email": email},{"Email":0,  "_id":0, "Password":0, "City":0, "State":0, "Street":0,"Last_Login":0, "Zip":0}))
    if (checker == list()):
        #print("unsuccessful login attempt")
        return -1
    else:
        conversion = json.dumps(checker[0])
        conversion1 = conversion[:-1]
        conversion1 = conversion1.split(":",1)
        conversion2 = json.dumps(conversion1[1])
        JSONapt = json.loads(conversion2)
        return JSONapt

              
