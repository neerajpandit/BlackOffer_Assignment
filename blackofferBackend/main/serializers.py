# dashboard_app/serializers.py
from rest_framework import serializers
from .models import EnergyInsight

class EnergyInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyInsight
        fields = '__all__'

    