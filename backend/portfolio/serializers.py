from rest_framework import serializers
from .models import Position, Portfolio 

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position 
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
