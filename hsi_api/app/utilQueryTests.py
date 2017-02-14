import unittest
import hsi_api
import json
import Util

class utilQueryTests(unittest.TestCase):
    api = None
    def setUp(self):
        self.api = hsi_api.Hsi_Api("config.json")

    def test_queryHappy(self):
        result = self.api.utilQuery([{'long':-122.4968977, 'lat':48.7606482, 'address':"1020 24th st apt c302, Bellingha Wa 98225"}])
        result = json.loads(result)
        r = ('long' in result['addr0']['c302']) \
        assertEqual(True, r)

if __name__ == '__main__':
    unittest.main()
        
