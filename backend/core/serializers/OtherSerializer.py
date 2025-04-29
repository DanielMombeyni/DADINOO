"""
Base Models Serializers.
"""

from rest_framework import serializers
from core.models import Plan, CoinPricing


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "description", "logo"]


class CoinPricingSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = CoinPricing
        fields = [
            "id",
            "title",
            "coin_amount",
            "original_price",
            "discount_percent",
            "final_price",
        ]

    def get_final_price(self, obj):
        return obj.final_price
