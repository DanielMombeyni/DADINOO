"""
Payment Views.
"""

from django.urls import path
from api.views import PaymentViews

app_name = "payment"

urlpatterns = [
    path(
        "pricing/", PaymentViews.CoinPricingListView.as_view(), name="coin-pricing-list"
    ),
]
