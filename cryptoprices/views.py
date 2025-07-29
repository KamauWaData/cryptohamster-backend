from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
import requests
from .models import CryptoPrice
from django.shortcuts import get_object_or_404
from .serializers import CryptoPriceSerializer, CryptoPriceDetailSerializer

class PriceIndexView(APIView):
    def get(self, request):
        symbols = request.query_params.getlist('symbols')
        queryset = CryptoPrice.objects.all()

        if symbols:
            queryset = queryset.filter(symbol__in=symbols)

        serializer = CryptoPriceSerializer(queryset, many=True)
        return Response(serializer.data)
    

class CryptoTokenDetailView(RetrieveAPIView):
    serializer_class = CryptoPriceDetailSerializer
    lookup_field = 'symbol'

    def get_queryset(self):
        return CryptoPrice.objects.all()

    def get_object(self):
        symbol = self.kwargs.get('symbol').upper() + "USDT"
        return get_object_or_404(CryptoPrice, symbol=symbol)



