from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from weather.models import CityQuery


class WeatherViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('weather.views.get_weather')
    def test_weather_view_valid_city(self, mock_get_weather):
        mock_get_weather.return_value = {
            'city': 'TestCity',
            'forecast': [
                {
                    'date': '2024-07-18',
                    'temperature_max': 30,
                    'temperature_min': 20,
                    'precipitation': 5,
                    'wind_speed': 10
                }
            ]
        }

        response = self.client.post(reverse('weather'), {'city': 'TestCity'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(CityQuery.objects.filter(city='TestCity').exists())
        self.assertContains(response, 'TestCity')
        self.assertContains(response, '2024-07-18')

    @patch('weather.views.get_weather')
    def test_weather_view_invalid_city(self, mock_get_weather):
        mock_get_weather.return_value = None

        response = self.client.post(reverse('weather'), {'city': 'InvalidCity'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results found for city: InvalidCity')
        self.assertFalse(CityQuery.objects.filter(city='InvalidCity').exists())

    def test_weather_view_get_request(self):
        response = self.client.get(reverse('weather'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('last_city', response.context)
        self.assertIn('cities', response.context)

    @patch('weather.views.get_weather')
    def test_weather_view_session(self, mock_get_weather):
        mock_get_weather.return_value = {
            'city': 'TestCity',
            'forecast': [
                {
                    'date': '2024-07-18',
                    'temperature_max': 30,
                    'temperature_min': 20,
                    'precipitation': 5,
                    'wind_speed': 10
                }
            ]
        }

        self.client.post(reverse('weather'), {'city': 'TestCity'})
        response = self.client.get(reverse('weather'))

        self.assertEqual(self.client.session['last_city'], 'TestCity')
        self.assertEqual(response.context['last_city'], 'TestCity')

