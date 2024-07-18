from rest_framework import serializers
from .models import CityQuery


class CityQuerySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = CityQuery
        fields = ['city', 'count']
        