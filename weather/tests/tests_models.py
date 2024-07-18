from django.test import TestCase
from weather.models import CityQuery
from django.utils import timezone


class CityQueryModelTest(TestCase):

    def setUp(self):
        # Create a CityQuery instance for testing
        self.city_query = CityQuery.objects.create(city="TestCity")

    def test_city_query_creation(self):
        # Test if the CityQuery instance is created correctly
        self.assertIsInstance(self.city_query, CityQuery)
        self.assertEqual(self.city_query.city, "TestCity")
        self.assertIsNotNone(self.city_query.timestamp)

    def test_city_query_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.city_query), "TestCity")

    def test_timestamp_auto_now_add(self):
        # Test if timestamp is automatically set
        self.assertAlmostEqual(self.city_query.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_city_max_length(self):
        # Test the max_length of the city field
        max_length = self.city_query._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)
