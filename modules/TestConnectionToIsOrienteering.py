import utilities.ErrorHandler as e
from GetFromIsOrienteering import Mod_get
import PostToIsOrienteering as post
import unittest
import json

API_ENDPOINT = 'https://is.orienteering.sk/api'
API_KEY = 'NjUxODU1ZDE3YTEyMA=='
WRONG_API_ENDPOINT = 'https://is.orienteering.sk'
WRONG_API_KEY = 'NjUxODU1ZDE3YTEyMA'
RACE_ID = None
CLUB_ID = 81
RUNNER_ID = None


class ModGetTest(unittest.TestCase):
    def test_bad_endpoint_get(self):
        g = Mod_get(WRONG_API_ENDPOINT, API_KEY)
        self.assertRaises(e.IsOrieteeringApiError, g.get_categories_details)
        try:
            g.get_categories_details()
        except e.IsOrieteeringApiError as er:
            self.assertEqual(er.code, 404)
            self.assertEqual(er.message, 'Not Found https://is.orienteering.sk/lists/category')

    def test_bad_key_get(self):
        g = Mod_get(API_ENDPOINT, WRONG_API_KEY)
        self.assertRaises(e.IsOrieteeringApiError, g.get_categories_details)
        try:
            g.get_categories_details()
        except e.IsOrieteeringApiError as er:
            self.assertEqual(er.code, 403)
            self.assertEqual(er.message, 'Forbidden https://is.orienteering.sk/api/lists/category')

    def test_bad_everything(self):
        g = Mod_get(WRONG_API_ENDPOINT, WRONG_API_KEY)
        self.assertRaises(e.IsOrieteeringApiError, g.get_categories_details)
        try:
            g.get_categories_details()
        except e.IsOrieteeringApiError as er:
            self.assertEqual(er.code, 404)
            self.assertEqual(er.message, 'Not Found https://is.orienteering.sk/lists/category')

    def test_get_races_in_month(self):
        g = Mod_get(API_ENDPOINT, API_KEY)
        races = g.get_races_in_month("November")
        self.assertIsNotNone(races)
        RACE_ID = races[1]["id"]
        self.assertIsNotNone(RACE_ID)
        ### doplnit test ci preteky su v datume

    def test_get_club_registrations(self):
        g = Mod_get(API_ENDPOINT, API_KEY)
        club_registrations = g.get_club_registrations(CLUB_ID)
        self.assertIsNotNone(club_registrations)
        self.assertEqual(club_registrations[0]["runner"]["first_name"], "Richard")
        RUNNER_ID = club_registrations[0]["runner_id"]
        self.assertIsNotNone(RUNNER_ID)
        
    def test_get_runner(self):
        g = Mod_get(API_ENDPOINT, API_KEY)
        print(RUNNER_ID)
        runner = g.get_runner(RUNNER_ID)
        print(runner)
        self.assertIsNotNone(runner)
        self.assertEqual(runner[0]["first_name"], "Richard")

if __name__ == '__main__':
    unittest.main()