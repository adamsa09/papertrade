from rest_framework import serializers
<<<<<<< HEAD
=======
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
>>>>>>> 571f8e3ad5d5a6479d6294ded5b4c3ac94a3a70e
