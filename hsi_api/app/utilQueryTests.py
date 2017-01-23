import unittest
import hsi_api
import json
import Util

class utilQueryTests(origins):
    api = None
    def setUp(self):
        self.api = hsi_api.Hsi_Api("config.json")

    def test_queryHappy(self):
        result = self.api.utilQuery([{'long':-122.502782, 'lat':48.729826}])
        result = json.loads(result)
        r = ('long' in result['addr0']['""']) \
            and ('long' in result['addr0']['"M2"') \
            and (Util.valid_json(str(result)))
        assertEqual(True, r)

if __name__ == '__main__':
    unittest.main()
        
