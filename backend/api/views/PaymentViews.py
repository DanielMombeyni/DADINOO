from rest_framework import generics
from core.models import CoinPricing
from core.serializers import CoinPricingSerializer


class CoinPricingListView(generics.ListAPIView):
    queryset = CoinPricing.objects.all()
    serializer_class = CoinPricingSerializer
