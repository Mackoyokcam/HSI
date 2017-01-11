from app import Util
import json,requests
from app.googlemaps import client,distance_matrix,geocoding
from pymongo import errors as mongoerrors
from pymongo import MongoClient



class Hsi_Api:
    GOOGLE_API_KEY = ""
    WALKSCORE_API_KEY = ""
    WALKSCORE_URL ="http://api.walkscore.com/score"
    GOOGLE_CLIENT = None
    MAX_COMPARES = 0
    
    def __init__(self, config_file_url):
        json_obj = Util.get_JSON_Obj(config_file_url)
        self.GOOGLE_API_KEY = json_obj["GOOGLE_API_KEY"]
        self.WALKSCORE_API_KEY = json_obj["WALKSCORE_KEY"]
        self.GOOGLE_CLIENT = client.Client(key=self.GOOGLE_API_KEY)
        self.MAX_COMPARES = json_obj['max_compares']

        
        
    def compare(self, home_addresses, list_destinations):
        if type(home_addresses) is not list or type(list_destinations) is not list:
            return '{"error":"origins and destinations must be in list form"}'
        elif len(home_addresses) > self.MAX_COMPARES or len(list_destinations) > self.MAX_COMPARES:
            return '{"error":"Max compares exceeded. Only '+str(self.MAX_COMPARES)+' allowed per request"}'
        return json.JSONEncoder().encode({"google":self.google_matrix(home_addresses,list_destinations), \
                                          "walkscore": self.get_walkscore(home_addresses)})
    '''
    format = json
    address= ""
    lat=""
    lon=""
    apikey=""
    
    200 	1 	Walk Score successfully returned.
    200 	2 	Score is being calculated and is not currently available.
    404 	30 	Invalid latitude/longitude.
    500 series 	31 	Walk Score API internal error.
    200 	40 	Your WSAPIKEY is invalid.
    200 	41 	Your daily API quota has been exceeded.
    403 	42 	Your IP address has been blocked.
    '''
    def get_single_walkscore(self, address,lat = None, lng = None):
        if address == None:
            return '{"status":"An address must be supplied"}'
        if lat == None or lng == None:
            lat_lng = json.loads(self.get_location_data(address))
            if lat_lng['count'] < 1:
                return '{"results":"no results found"}'
            lat = lat_lng['results'][0]['lat']
            lng = lat_lng['results'][0]['lng']
        params = {'address':address,'lat':lat,'lon':lng,'format':'json','apikey':self.WALKSCORE_API_KEY}
        results = json.loads(requests.get(self.WALKSCORE_URL,params=params).text)
        status = results['status']
        if status  == 40:
            return '{"status": "Key is invalid"}'
        elif status == 30:
            return '{"status": "Latitude and Longitude are invalid"}'
        elif status == 41:
            return '{"status": "Quota is exceeded"}'
        elif status == 42:
            return '{"status": "IP address is blocked"}'
        elif status == 31:
            return '{"status": "Walkscore had an error"}'
        elif status == 1:
            print(results)
            return results


    def get_walkscore(self,address,lat=None,lng=None):
        if type(address) is list and lat is None and lng is None:
            results = dict()
            for addr in address:
                results[addr] = self.get_single_walkscore(addr,None,None)
            return str(results)
        elif type(address) is list and lat is not None and lng is not None\
                and len(lat) == len(lng):
                    results = dict()
                    for combo in self.params_to_tuples:
                        results[combo[0]] = self.get_single_walkscore(combo[0],combo[1],combo[2])
                    return str(results)
        return {"error":"invalid request for walkscore interface: addresses is a "+\
                str(type(address)) +" and lat is: "+str(type(lat)) + "and lng is: "+str(type(lng))}

    def params_to_tuples(self,addresses,lat,lng):
        list_tuples=list()
        for x in range(0,len(addresses)):
            current = list()
            current.append(addresses[x])
            if lat is not None and x < len(lat):
                current.append(lat[x])
            else:
                current.append(None)
            if lng is not None and x < len(lng):
                current.append(lng[x])
            else:
                current.append(None)
            list_tuples.append(tuple(current))
        return list_tuples


    '''
    
    :param origins
    :type list
    
    :param destinations
    :type list
    '''
    def google_matrix(self, origins, destinations, mode="walking", language=None, avoid=None, units="imperial",
                      departure_time=None,
                      arrival_time=None, transit_mode=None, transit_routing_preference=None, traffic_model=None):
        return distance_matrix.distance_matrix(self.GOOGLE_CLIENT, origins, destinations, mode, language, avoid,
                                               units, departure_time, arrival_time, transit_mode,
                                               transit_routing_preference, traffic_model)
    
    
    '''
    
    
    :param address a required parameter that specifies an address to search for
    :type string
    
    :returns returns a json string containing results. the schema of the response will be
    {"count": int, "results":[{"lat":"","lng":"","formatted_address":""}...n]}. If there
    :type string or None
    '''
    def get_location_data(self, address):
        result = geocoding.geocode(self.GOOGLE_CLIENT,address=address)
        status_code = result['status']
        if status_code == 'OK':
            relevant_info = result["results"]
            return_value = dict()
            return_value['count'] = len(relevant_info)
            return_value['results'] = list()
            for x in relevant_info:
                temp = dict()
                temp['formatted_address'] = x['formatted_address']
                temp['lat'] = x['geometry']['location']['lat']
                temp['lng'] = x['geometry']['location']['lng']
                return_value['results'].append(temp)
            return_value = json.JSONEncoder().encode(return_value)
        else:
            return_value = '{"status":"'+status_code+'"}'
        return return_value
 

    '''''
    Format for origins is a list, the contents of each index being a dict containing a latitude and a longitude of the original addres, calculated by Google's geocoding in views.py

    Returns a dict that, for every index in origins, returns a dict entry of format "addr#": #Mongo return json#, the # in addr corresponding to the index in which each address was originally referenced in the POST parameters. addresses that return in error in Google's geocoding will contain a dict with entry "status", with the value being the error message in that address' corresponding dict entry.
    
    Can be extended to gather more than just the last updated information, if average cost numbers were implemented later
    '''''
    def utilQuery(self, origins):        
        MDBclient = MongoClient()
        db = MDBclient.test
        data = {}
        j = 0
        for i in origins:
            apt = db.util.distinct("apt", i)
            if len(apt) is 0:
                data.update({"addr"+str(j):{"status":"ZERO DB RESULTS"}})
            else:
                apt_data={}                    
                for k in apt:
                    new_i = i
                    new_i.update({"apt":k})                        
                    cursor = db.util.find(new_i, { "_id":0, "lat":0, "long":0, "apt":0 }).sort("updateDate", -1).limit(1)
                    cursor = next(cursor, None)
                    apt_data.update({k: cursor})                        
                data.update({"addr"+str(j):apt_data})    
            j = j+1
        return data
                
    '''''
    Format for util_info is a string formatted like a json document.
    Returns true/false depending on success of data entry (will implement more extensive error reporting later).
    '''''
    def utilAdd(self, util_info):
        MDBclient = MongoClient()
        db = MDBclient.test
        try:
            result = db.util.insert_one(util_info)
        except mongoerrors.PyMongoError:
            return False        
        return True
