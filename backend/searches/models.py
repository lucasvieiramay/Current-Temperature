from django.db import models


class Search(models.Model):
    """
    Storage the logs.
    Notes about the zip code:
    Currently, the longest postal code is 10 char. Iran has 10 diguts
    and the US have 4 and 5 seperated by a hyphen. Brazil is 9.
    """
    zip_code = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=255, blank=True)
    cordenates = models.CharField(max_length=64, blank=True)
    country_code = models.CharField(max_length=4, blank=True)
    temperature = models.CharField(max_length=8)
    searched_at = models.DateTimeField(auto_now=True, blank=True)
    unit_of_measurement = models.CharField(max_length=32)
