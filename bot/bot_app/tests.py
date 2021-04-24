from django.test import TestCase

# Create your tests here.

from .views import get_location_from_zip, search_location_in_sheet
import sys
sys.path.append('/Users/piyushbagad/personal/projects/covid-whatsapp-bot/')

from data.gsheets import get_gsheet



class ViewsTestCase(TestCase):
    def setUp(self):
        self.gsheet = get_gsheet()

    def test_get_location_from_zip_invalid_inputs(self):
        """Tests get location function from zipcode
        """
        zipcode = '4220089'
        response, location, _ = get_location_from_zip(f'ZIP X {zipcode}')
        self.assertTrue('Incorrect ZIP information entered.' in response)
        self.assertEqual(location, None)

        zipcode = '4220089'
        response, location, _ = get_location_from_zip(f'ZIP {zipcode}')
        self.assertTrue('Incorrect ZIP code entered' in response)
        self.assertEqual(location, None)

    def test_get_location_from_zip_valid_input(self):
        """Tests get location function from zipcode
        """
        zipcode = '422008'
        response, location, _ = get_location_from_zip(f'ZIP {zipcode}')

        latitude = location.latitude
        longitude = location.longitude
        self.assertEqual(latitude, 20.02405519230769)
        self.assertEqual(longitude, 73.76155313076923)

    def test_search_location_in_sheet(self):
        """Tests search location in sheet
        """
        zipcode = '400012'
        response, location, _ = get_location_from_zip(f'ZIP {zipcode}')

        latitude = location.latitude
        longitude = location.longitude

        response = search_location_in_sheet(zipcode, location)
        self.assertTrue('Mr. Rakesh' in response)
