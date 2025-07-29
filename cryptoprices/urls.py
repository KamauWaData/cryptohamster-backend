from django.urls import path
from .views import PriceIndexView, CryptoTokenDetailView

urlpatterns = [
    path('prices/', PriceIndexView.as_view(), name='price-index'),
   
    path("price/<str:symbol>/", CryptoTokenDetailView.as_view(), name="token-detail"),
]