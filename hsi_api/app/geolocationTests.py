import unittest
import hsi_api
import json


class geolocationTests(unittest.TestCase):
    api=None
    def setUp(self):

        self.api = hsi_api.Hsi_Api("config.json")

    def test_happyPath(self):
        results = self.api.get_location_data('416 High St Bellingham WA 98225')
        results = json.loads(results)
        self.assertEqual(results['count'],1)
        self.assertEqual(results['results'][0]['lat'],48.7374448 )
        self.assertEqual(results['results'][0]['lng'],-122.4872668)
    def test_apartment(self):
        address = "465 31st St Bellingham, WA 98225"
        results = self.api.get_location_data(address)
        results = json.loads(results)
        self.assertEqual(results['count'],1)

    def test_non_existant_address(self):
        results = json.loads(self.api.get_location_data("123 main st bellingham wa 98225"))
        self.assertEqual(results['count'],4)


if __name__ == '__main__':
    unittest.main()
