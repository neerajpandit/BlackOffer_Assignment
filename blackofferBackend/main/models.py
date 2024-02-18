# models.py
from django.db import models

class EnergyInsight(models.Model):
    end_year = models.CharField(max_length=10, blank=True)
    intensity = models.IntegerField(null=True,)
    sector = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    insight = models.CharField(max_length=100)
    url = models.URLField()
    region = models.CharField(max_length=100)
    start_year = models.CharField(max_length=10, blank=True)
    impact = models.CharField(max_length=100, blank=True)
    added = models.DateTimeField(null=True,)
    published = models.DateTimeField(null=True,)
    country = models.CharField(max_length=100)
    relevance = models.IntegerField(null=True,)
    pestle = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    likelihood = models.IntegerField(null=True,)
