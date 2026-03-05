from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from transactions.models import Trade
from transactions.serializers import TradeSerializer

# Create your views here.
@api_view(['GET'])
def getTrades(request):
    trades = Trade.objects.all()

    serializer = TradeSerializer(trades, many=True)

    return Response(serializer.data)


