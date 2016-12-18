import unittest
import hsi_api

class distanceMatrixTests(unittest.TestCase):
    api = None

    def setUp(self):
        self.api = hsi_api.Hsi_Api("config.json")

    def test_happyPath(self):
        result = self.api.google_matrix(['465 31st st bellingham wa 98225'],['416 high st bellingham wa 98225','210 36th St bellingham wa 98225'])
        self.assertEqual("1.2 mi",result['rows'][0]['elements'][0]['distance']['text'])
        self.assertEqual("0.5 mi", result['rows'][0]['elements'][1]['distance']['text'])


if __name__ == '__main__':
    unittest.main()
