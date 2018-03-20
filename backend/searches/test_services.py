import mock

from django.test import TestCase

from searches.services import GoogleMapsService
from searches.services import OpenWeatherService


class TestGoogleMapsService(TestCase):

    @mock.patch('searches.services.googlemaps.geocoding.geocode')
    def test_get_query_parameter_with_city(self, mock_googlemaps_geocode):
        """
        On this test we send only the city and
        the return must be a dict with the country code
        and the city only.
        """
        mock_googlemaps_geocode.geocode.return_value = [{
            'address_components': [{
                'types': ['administrative_area_level_2', 'political'],
                'short_name': 'Florianópolis',
                'long_name': 'Florianópolis'
            }, {
                'types': ['administrative_area_level_1', 'political'],
                'short_name': 'SC',
                'long_name': 'State of Santa Catarina'
            }, {
                'types': ['country', 'political'],
                'short_name': 'BR',
                'long_name': 'Brazil'
            }],
            'geometry': {
                'location': {
                    'lat': -27.5948698,
                    'lng': -48.54821949999999
                },
                'bounds': {
                    'southwest': {
                        'lat': -27.8493578,
                        'lng': -48.6065648
                    },
                    'northeast': {
                        'lat': -27.382992,
                        'lng': -48.3587861
                    }
                },
                'viewport': {
                    'southwest': {
                        'lat': -27.8493578,
                        'lng': -48.6065648
                    },
                    'northeast': {
                        'lat': -27.382992,
                        'lng': -48.3587861
                    }
                },
                'location_type': 'APPROXIMATE'
            },
            'place_id': 'ChIJn7h-4b9JJ5URGCq6n0zj1tM',
            'formatted_address': 'Florianópolis - State of Santa Catarina, Brazil',
            'types': ['administrative_area_level_2', 'political']
        }]
        test_service = GoogleMapsService()
        response = test_service.get_query_parameter('florianópolis')
        right_response = {'country_code': 'BR', 'city': 'Florianópolis'}
        self.assertDictEqual(right_response, response)

    @mock.patch('searches.services.googlemaps.geocoding.geocode')
    def test_get_query_parameter_with_a_neighborhood(self, mock_googlemaps_geocode):
        """
        On this test we send only the neighborhood, on this case
        google don't return the city so we need to get the geo cordenates.
        They should be on a dict with the lat and lng keys
        """
        mock_googlemaps_geocode.geocode.return_value = [{
            'place_id': 'ChIJA9ZasVk7J5URM59o-uEPlqY',
            'geometry': {
                'bounds': {
                    'southwest': {
                        'lng': -48.4819752,
                        'lat': -27.6903978
                    },
                    'northeast': {
                        'lng': -48.4502878,
                        'lat': -27.6302606
                    }
                },
                'location_type': 'APPROXIMATE',
                'location': {
                    'lng': -48.4734326,
                    'lat': -27.662215
                },
                'viewport': {
                    'southwest': {
                        'lng': -48.4819752,
                        'lat': -27.6903978
                    },
                    'northeast': {
                        'lng': -48.4502878,
                        'lat': -27.6302606
                    }
                }
            },
            'address_components': [{
                'types': ['establishment', 'natural_feature'],
                'long_name': 'Campeche',
                'short_name': 'Campeche'
            }, {
                'types': ['administrative_area_level_1', 'political'],
                'long_name': 'State of Santa Catarina',
                'short_name': 'SC'
            }, {
                'types': ['country', 'political'],
                'long_name': 'Brazil',
                'short_name': 'BR'
            }],
            'types': ['establishment', 'natural_feature'],
            'formatted_address': 'Campeche, State of Santa Catarina, Brazil'
        }]
        test_service = GoogleMapsService()
        response = test_service.get_query_parameter('campeche, florianópolis')
        right_response = {
            'zip_code': '',
            'cordenates': {'lat': -27.662215, 'lng': -48.4734326},
            'country_code': 'BR'
        }
        self.assertDictEqual(right_response, response)

        @mock.patch('searches.services.googlemaps.geocoding.geocode')
        def test_get_query_parameter_with_a_full_address(self, mock_googlemaps_geocode):
            """
            On this test we send the full address, on this case
            we are able to get the zipcode.
            """
            mock_googlemaps_geocode.geocode.return_value = [{
                'types': ['route'],
                'formatted_address': 'Servidão Canto das Pérolas - Campeche, Florianópolis - SC, 88063-076, Brazil',
                'geometry': {
                    'viewport': {
                        'northeast': {
                            'lat': -27.6926408197085,
                            'lng': -48.499885
                        },
                        'southwest': {
                            'lat': -27.6953387802915,
                            'lng': -48.5037779
                        }
                    },
                    'location': {
                        'lat': -27.6940506,
                        'lng': -48.5016898
                    },
                    'bounds': {
                        'northeast': {
                            'lat': -27.693596,
                            'lng': -48.499885
                        },
                        'southwest': {
                            'lat': -27.6943836,
                            'lng': -48.5037779
                        }
                    },
                    'location_type': 'GEOMETRIC_CENTER'
                },
                'place_id': 'ChIJW6jmLTk7J5URFzPzdSxrV_Q',
                'address_components': [{
                    'short_name': 'Servidão Canto das Pérolas',
                    'types': ['route'],
                    'long_name': 'Servidão Canto das Pérolas'
                }, {
                    'short_name': 'Campeche',
                    'types': ['political', 'sublocality', 'sublocality_level_1'],
                    'long_name': 'Campeche'
                }, {
                    'short_name': 'Florianópolis',
                    'types': ['administrative_area_level_2', 'political'],
                    'long_name': 'Florianópolis'
                }, {
                    'short_name': 'SC',
                    'types': ['administrative_area_level_1', 'political'],
                    'long_name': 'Santa Catarina'
                }, {
                    'short_name': 'BR',
                    'types': ['country', 'political'],
                    'long_name': 'Brazil'
                }, {
                    'short_name': '88063-076',
                    'types': ['postal_code'],
                    'long_name': '88063-076'
                }]
            }]
            test_service = GoogleMapsService()
            response = test_service.get_query_parameter(
                'servidão canto das pérolas campeche florianópolis')
            right_response = {'country_code': 'BR',
                              'city': 'Florianópolis', 'zip_code': '88063-076'}

            self.assertDictEqual(right_response, response)

    def test_get_country_code_true(self):
        address_component = [{
            'long_name': 'Servidão Canto das Pérolas',
            'short_name': 'Servidão Canto das Pérolas',
            'types': ['route']
        }, {
            'long_name': 'Campeche',
            'short_name': 'Campeche',
            'types': ['political', 'sublocality', 'sublocality_level_1']
        }, {
            'long_name': 'Florianópolis',
            'short_name': 'Florianópolis',
            'types': ['administrative_area_level_2', 'political']
        }, {
            'long_name': 'Santa Catarina',
            'short_name': 'SC',
            'types': ['administrative_area_level_1', 'political']
        }, {
            'long_name': 'Brazil',
            'short_name': 'BR',
            'types': ['country', 'political']
        }, {
            'long_name': '88063-076',
            'short_name': '88063-076',
            'types': ['postal_code']
        }]
        country_code = GoogleMapsService().get_country_code(address_component)
        self.assertEqual('BR', country_code)

    def test_get_country_code_false(self):
        address_component = [{
            'long_name': 'Servidão Canto das Pérolas',
            'short_name': 'Servidão Canto das Pérolas',
            'types': ['route']
        }, {
            'long_name': 'Campeche',
            'short_name': 'Campeche',
            'types': ['political', 'sublocality', 'sublocality_level_1']
        }, {
            'long_name': 'Florianópolis',
            'short_name': 'Florianópolis',
            'types': ['administrative_area_level_2', 'political']
        }, {
            'long_name': 'Santa Catarina',
            'short_name': 'SC',
            'types': ['administrative_area_level_1', 'political']
        }, {
            'long_name': '88063-076',
            'short_name': '88063-076',
            'types': ['postal_code']
        }]
        country_code = GoogleMapsService().get_country_code(address_component)
        self.assertFalse(country_code)

    def test_get_city_name_true(self):
        address_component = [{
            'long_name': 'Servidão Canto das Pérolas',
            'short_name': 'Servidão Canto das Pérolas',
            'types': ['route']
        }, {
            'long_name': 'Campeche',
            'short_name': 'Campeche',
            'types': ['political', 'sublocality', 'sublocality_level_1']
        }, {
            'long_name': 'Florianópolis',
            'short_name': 'Florianópolis',
            'types': ['administrative_area_level_2', 'political']
        }, {
            'long_name': 'Santa Catarina',
            'short_name': 'SC',
            'types': ['administrative_area_level_1', 'political']
        }, {
            'long_name': 'Brazil',
            'short_name': 'BR',
            'types': ['country', 'political']
        }, {
            'long_name': '88063-076',
            'short_name': '88063-076',
            'types': ['postal_code']
        }]
        city_name = GoogleMapsService().get_city_name(address_component)
        self.assertEqual('Florianópolis', city_name)

        address_component = [{
            'long_name': 'Servidão Canto das Pérolas',
            'short_name': 'Servidão Canto das Pérolas',
            'types': ['route']
        }, {
            'long_name': 'Campeche',
            'short_name': 'Campeche',
            'types': ['political', 'sublocality', 'sublocality_level_1']
        }, {
            'long_name': 'Florianópolis',
            'short_name': 'Florianópolis',
            'types': ['locality']
        }, {
            'long_name': 'Santa Catarina',
            'short_name': 'SC',
            'types': ['administrative_area_level_1', 'political']
        }, {
            'long_name': 'Brazil',
            'short_name': 'BR',
            'types': ['country', 'political']
        }, {
            'long_name': '88063-076',
            'short_name': '88063-076',
            'types': ['postal_code']
        }]
        city_name = GoogleMapsService().get_city_name(address_component)
        self.assertEqual('Florianópolis', city_name)

    def test_get_city_name_false(self):
        address_component = [{
            'long_name': 'Servidão Canto das Pérolas',
            'short_name': 'Servidão Canto das Pérolas',
            'types': ['route']
        }, {
            'long_name': 'Campeche',
            'short_name': 'Campeche',
            'types': ['political', 'sublocality', 'sublocality_level_1']
        }, {
            'long_name': 'Santa Catarina',
            'short_name': 'SC',
            'types': ['administrative_area_level_1', 'political']
        }, {
            'long_name': '88063-076',
            'short_name': '88063-076',
            'types': ['postal_code']
        }]
        city_name = GoogleMapsService().get_country_code(address_component)
        self.assertFalse(city_name)


class TestOpenWeatherService(TestCase):

    @mock.patch('searches.services.pyowm')
    @mock.patch.object(OpenWeatherService, '_weather_at_place')
    def test_get_current_weather_with_city(self, mock_method, mock_pyowm):
        data = {'country_code': 'BR', 'city': 'Florianópolis'}
        ows = OpenWeatherService('celsius')
        ows.get_current_weather(data)
        mock_method.assert_called_with('Florianópolis,BR')

    @mock.patch('searches.services.pyowm')
    @mock.patch.object(OpenWeatherService, '_weather_at_coords')
    def test_get_current_weather_with_cordenates(self, mock_method, mock_pyowm):
        data = {
            'country_code': 'BR',
            'cordenates': {'lat': -27.662215, 'lng': -48.4734326},
            'zip_code': ''
        }
        ows = OpenWeatherService('celsius')
        ows.get_current_weather(data)
        mock_method.assert_called_with(data)

    @mock.patch('searches.services.pyowm')
    @mock.patch.object(OpenWeatherService, '_weather_at_zip_code')
    def test_get_current_weather_with_zip_code(self, mock_method, mock_pyowm):
        data = {
            'country_code': 'BR',
            'zip_code': '88034-132'
        }
        ows = OpenWeatherService('celsius')
        ows.get_current_weather(data)
        mock_method.assert_called_with(data)
