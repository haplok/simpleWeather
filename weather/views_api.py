from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import CityQuery
from .serializers import CityQuerySerializer


class CityQueryCountView(APIView):

    def get(self, request, *args, **kwargs):
        city_query_counts = CityQuery.objects.values('city').annotate(count=Count('city')).order_by('-count')
        serializer = CityQuerySerializer(city_query_counts, many=True)
        return Response(serializer.data)