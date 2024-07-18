from django.urls import path
from .views import weather_view
from .views_api import CityQueryCountView

urlpatterns = [
    path('', weather_view, name='weather'),
    path('api/city-query-count/', CityQueryCountView.as_view(), name='city-query-count'),
]