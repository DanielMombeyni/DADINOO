"""
Wallet Serializers.
"""

from rest_framework import serializers
from core.models import Wallet, Transaction
from core.models.TransactionsModel import TransactionType


# class WalletBalanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ["balance"]


# class TransactionListSerializer(serializers.ModelSerializer):
#     type_display = serializers.CharField(source="get_transaction_type_display")
#     status_display = serializers.CharField(source="get_status_display")

#     class Meta:
#         model = Transaction
#         fields = [
#             "id",
#             "amount",
#             "type",
#             "type_display",
#             "status_display",
#             "transaction_date",
#             "description",
#         ]

class TransactionItemSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_transaction_type_display')
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'type_display', 'status_display', 'transaction_date', 'description']


class WalletWithTransactionsSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=15, decimal_places=3)
    transactions = TransactionItemSerializer(many=True)