import json
from json import JSONDecodeError


def get_JSON_Obj(file):
    try:
        json_str = ""
        with open(file) as fp:
            json_str = json.load(fp)
        return json_str
    except IOError:
        return None
    except OSError:
        return None
    except FileExistsError:
        return None

def valid_json(json_string):
    try:
        json.JSONDecoder(json_string)
        return True
    except JSONDecodeError:
        return False
