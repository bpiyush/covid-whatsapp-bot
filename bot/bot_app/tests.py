from django.test import TestCase

# Create your tests here.

from .views import get_location_from_zip


class ViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_location_from_zip_invalid_inputs(self):
        """Tests get location function from zipcode
        """
        zipcode = '4220089'
        response, location = get_location_from_zip(f'ZIP X {zipcode}')
        import ipdb; ipdb.set_trace()

        self.assertTrue('Incorrect ZIP information entered.' in response)
        self.assertEqual(location, None)

        zipcode = '4220089'
        response, location = get_location_from_zip(f'ZIP {zipcode}')
        self.assertTrue('Incorrect ZIP code entered' in response)
        self.assertEqual(location, None)

    def test_get_location_from_zip_valid_input(self):
        """Tests get location function from zipcode
        """
        zipcode = '422008'
        response, location = get_location_from_zip(f'ZIP {zipcode}')

        latitude = location.latitude
        longitude = location.longitude
        self.assertEqual(latitude, 20.02405519230769)
        self.assertEqual(longitude, 73.76155313076923)
