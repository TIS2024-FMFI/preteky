import utilities.ErrorHandler as e
from GetFromIsOrienteering import Mod_get
import PostToIsOrienteering as post
import unittest

API_ENDPOINT = 'https://is.orienteering.sk/api'
API_KEY = 'NjUxODU1ZDE3YTEyMA=='
WRONG_API_ENDPOINT = 'https://is.orienteering.sk'
WRONG_API_KEY = 'NjUxODU1ZDE3YTEyMA'
RACE_ID = None
CLUB_ID = 81
RUNNER_ID = None
CATEGORY_ONE = None
CATEGORY_TWO = None

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

    def test_get_info(self):
        g = Mod_get(API_ENDPOINT, API_KEY)
        races = g.get_races_in_month("November")
        self.assertIsNotNone(races)
        RACE_ID = races[1]["id"]
        self.assertIsNotNone(RACE_ID)
        ### doplnit test ci preteky su v datume

        club_registrations = g.get_club_registrations(CLUB_ID)
        self.assertIsNotNone(club_registrations)
        self.assertEqual(club_registrations[0]["runner"]["first_name"], "Richard")
        RUNNER_ID = club_registrations[0]["runner_id"]
        self.assertIsNotNone(RUNNER_ID)

        runner = g.get_runner(RUNNER_ID)
        self.assertIsNotNone(runner)
        self.assertEqual(runner[0]["first_name"], "Richard")

        details = g.get_race_details(RACE_ID)
        self.assertIsNotNone(details)
        self.assertEqual(len(details["categories"]), 6)
        CATEGORY_ONE, CATEGORY_TWO = details["categories"][:2] 
        self.assertIsNotNone(CATEGORY_ONE)   
        self.assertIsNotNone(CATEGORY_TWO)
        self.assertEqual(CATEGORY_ONE["category_id"], '160')
        self.assertEqual(CATEGORY_TWO["category_id"], '161')

        

if __name__ == '__main__':
    unittest.main()