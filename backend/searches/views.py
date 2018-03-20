import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from searches.services import GoogleMapsService
from searches.services import OpenWeatherService

from searches.models import Search
from searches.serializers import SearchSerializer


@api_view(['POST'])
def search_zip(request):
    body_request = json.loads(request.body.decode('utf-8'))
    address = body_request.get('address')
    unit_of_measurement = body_request.get('unit_of_measurement', 'celsius')
    gmaps_service = GoogleMapsService()
    data_address = gmaps_service.get_query_parameter(address)
    ows = OpenWeatherService(unit_of_measurement=unit_of_measurement)
    temperature = ows.get_current_weather(data_address)

    if temperature:
        data_address['temperature'] = temperature['temp']
        data_address['unit_of_measurement'] = unit_of_measurement
        # Save the log on our db
        Search.objects.create(**data_address)
        if 'city' in data_address.keys():
            temperature['city'] = data_address['city']

    else:
        return Response(
            {'Address or temperature not found for the address': address}, status=status.HTTP_404_NOT_FOUND)

    return Response(temperature)


@api_view(['get'])
def list_logs(request):
    logs = Search.objects.all()
    serialized_logs = SearchSerializer(logs, many=True)
    return Response(serialized_logs.data)
