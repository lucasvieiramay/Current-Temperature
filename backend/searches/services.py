import googlemaps
import pyowm
import re
from django.conf import settings


class GoogleMapsService():
    def __init__(self):
        self.gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    def get_country_code(self, address_components):
        for component in address_components:
            if 'country' in component['types']:
                return component['short_name']
        return False

    def get_city_name(self, address_components):
        for component in address_components:
            if 'locality' in component['types']:
                return component['short_name']
            elif 'administrative_area_level_2' in component['types']:
                # administrative_area_level_2 is the city
                return component['short_name']
        return False

    def get_query_parameter(self, address):
        gmaps_response = self.gmaps.geocode(address)[0]
        data = {}
        data['country_code'] = self.get_country_code(
            gmaps_response['address_components'])

        if self.get_city_name(gmaps_response['address_components']):
            data['city'] = self.get_city_name(gmaps_response['address_components'])
        else:
            # Google didnt return the city name, lets get the cordenates
            data['cordenates'] = gmaps_response['geometry']['location']
        if 'formatted_address' in gmaps_response:
            formatted_address = gmaps_response['formatted_address'].split(',')
            if len(formatted_address) > 2:
                zip_code = formatted_address[2]
                zip_code = zip_code.replace(' ', '')
                data['zip_code'] = re.sub('[^0123456789\.\-]', '', zip_code)
        return data


class OpenWeatherService():
    def __init__(self, unit_of_measurement):
        self.ows = pyowm.OWM(settings.OPENWEATHER_API_KEY)
        self.unit_of_measurement = unit_of_measurement

    def _weather_at_place(self, ows_parameter):
        try:
            ows_response = self.ows.weather_at_place(ows_parameter)
        except pyowm.exceptions.not_found_error.NotFoundError:
            return False
        return ows_response

    def _weather_at_coords(self, data):
        try:
            ows_response = self.ows.weather_at_coords(
                data['cordenates']['lat'], data['cordenates']['lng']
            )
        except pyowm.exceptions.not_found_error.NotFoundError:
            return False
        return ows_response

    def _weather_at_zip_code(self, data):
        try:
            ows_response = self.ows.weather_at_zip_code(
                data['zip_code'], data['country_code']
            )
        except pyowm.exceptions.not_found_error.NotFoundError:
            return False
        return ows_response

    def get_current_weather(self, data):
        if 'city' in data.keys():
            # Get using the city
            ows_parameter = data['city'] + ',%s' % (data['country_code'])
            ows_response = self._weather_at_place(ows_parameter)

        elif 'cordenates' in data.keys():
            # Get using the cordenates
            ows_response = self._weather_at_coords(data)

        elif 'zip_code' in data.keys() and data['zip_code']:
            # Get using the Zipcode
            ows_response = self._weather_at_zip_code(data)

        if ows_response:
            observation = ows_response.get_weather()
            temperature = observation.get_temperature(self.unit_of_measurement)
            temperature['rain'] = observation.get_rain()
        else:
            return False

        return temperature
