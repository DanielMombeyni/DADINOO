"""
Wallet Views.
"""

from rest_framework import generics, permissions, response
from rest_framework.views import APIView
from core.models import Wallet, Transaction
from core.serializers import WalletWithTransactionsSerializer


class WalletSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user,defaults={"balance": 0})

        # آخرین ۱۰ تراکنش
        transactions = Transaction.objects.filter(user=request.user).order_by(
            "-transaction_date"
        )[:10]

        data = {"balance": wallet.balance, "transactions": transactions}
        serializer = WalletWithTransactionsSerializer(data)
        return response.Response(serializer.data)



# class WalletBalanceView(generics.RetrieveAPIView):
#     serializer_class = WalletBalanceSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return Wallet.objects.get(user=self.request.user)


# class TransactionListView(generics.ListAPIView):
#     serializer_class = TransactionListSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user).order_by(
#             "-transaction_date"
#         )
