import requests
from django.shortcuts import render
from .forms import CityForm
from .models import CityQuery


def get_weather(city):
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(geocoding_url)
    coords_data = response.json()

    if 'results' not in coords_data or len(coords_data['results']) == 0:
        return None

    city_coords = (coords_data['results'][0]['latitude'], coords_data['results'][0]['longitude'])
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city_coords[0]}&longitude={city_coords[1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=auto"
    response = requests.get(url)
    daily_data = response.json()['daily']

    weather_data = {
        'city': city,
        'forecast': [],
    }
    for i in range(len(daily_data['time'])):
        day_data = {
            'date': daily_data['time'][i],
            'temperature_max': daily_data['temperature_2m_max'][i],
            'temperature_min': daily_data['temperature_2m_min'][i],
            'precipitation': daily_data['precipitation_sum'][i],
            'wind_speed': daily_data['windspeed_10m_max'][i]
        }
        weather_data['forecast'].append(day_data)

    return weather_data


def weather_view(request):
    form = CityForm()
    weather_data = None
    error_message = None
    cities = list(CityQuery.objects.values_list('city', flat=True).distinct())

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather(city)
            if weather_data:
                CityQuery.objects.create(city=city)
                request.session['last_city'] = city
            else:
                error_message = f"No results found for city: {city}"

    last_city = request.session.get('last_city')
    context = {'form': form, 'weather_data': weather_data, 'last_city': last_city, 'cities': cities, 'error_message': error_message}
    return render(request, 'weather/weather.html', context)

