"""
Wallet Urls.
"""

from django.urls import path
from api.views import WalletViews

app_name = "Wallet"

urlpatterns = [
    path(
        "summary/",
        WalletViews.WalletSummaryView.as_view(),
        name="wallet-summary",
    ),
]


# urlpatterns = [
#     path("balance/", WalletViews.WalletBalanceView.as_view(), name="wallet-balance"),
#     path(
#         "transactions/",
#         WalletViews.TransactionListView.as_view(),
#         name="wallet-transactions",
#     ),
# ]
