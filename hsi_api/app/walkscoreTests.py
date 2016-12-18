import unittest
import hsi_api


class walkscoreTests(unittest.TestCase):
    api = None
    def setUp(self):
        self.api = hsi_api.Hsi_Api("config.json")

    def test_happyPath(self):
        result = self.api.get_walkscore('416 High St Bellingham, WA 98225')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
