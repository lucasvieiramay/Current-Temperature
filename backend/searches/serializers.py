from searches.models import Search
from rest_framework import serializers


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ('zip_code', 'city', 'cordenates', 'country_code',
                  'temperature', 'searched_at', 'unit_of_measurement')

    def create(self, validated_data):
        return Search.objects.create(**validated_data)
