# from enum import Enum
# from core.models import WalletTransaction


# class TransactionType(Enum):
#     DEPOSIT = 1  # واریز به کیف پول
#     WITHDRAWAL = 2  # برداشت از کیف پول
#     REFUND = 3  # بازگشت وجه
#     PAYMENT = 4  # پرداخت به فروشنده


# class Transaction:
#     @staticmethod
#     def create(
#         wallet, transaction_type, amount, description=None, advertisement_id=None
#     ):
#         """
#         ثبت تراکنش در دیتابیس.

#         :param wallet: کیف پول مرتبط با تراکنش
#         :param transaction_type: مقدار Enum از TransactionType
#         :param amount: مقدار تراکنش
#         :param description: توضیحات تراکنش (در صورت ارسال نشدن مقدار پیش‌فرض تعیین می‌شود)
#         :param advertisement_id: شناسه آگهی (اختیاری)
#         """
#         if description is None:
#             default_descriptions = {
#                 TransactionType.DEPOSIT: f"Initial deposit #{advertisement_id}",
#                 TransactionType.WITHDRAWAL: f"User withdrew funds #{advertisement_id}",
#                 TransactionType.REFUND: (
#                     f"Refund for order #{advertisement_id}"
#                     if advertisement_id
#                     else "Refund processed"
#                 ),
#                 TransactionType.PAYMENT: (
#                     f"Payment for seller order #{advertisement_id}"
#                     if advertisement_id
#                     else "Payment processed"
#                 ),
#             }
#             description = default_descriptions.get(
#                 transaction_type, "Transaction processed"
#             )

#         return WalletTransaction.objects.create(
#             wallet=wallet,
#             transaction_type=transaction_type.value,
#             amount=amount,
#             description=description,
#         )

#     @staticmethod
#     def Deposit(wallet, amount, advertisement_id=None, description=None):
#         """ثبت تراکنش واریز"""
#         return Transaction.create(
#             wallet, TransactionType.DEPOSIT, amount, description, advertisement_id
#         )

#     @staticmethod
#     def Withdrawal(wallet, amount, advertisement_id=None, description=None):
#         """ثبت تراکنش برداشت"""
#         return Transaction.create(
#             wallet, TransactionType.WITHDRAWAL, amount, description, advertisement_id
#         )

#     @staticmethod
#     def Refund(wallet, amount, advertisement_id=None, description=None):
#         """ثبت تراکنش بازگشت وجه"""
#         return Transaction.create(
#             wallet, TransactionType.REFUND, amount, description, advertisement_id
#         )

#     @staticmethod
#     def Payment(wallet, amount, advertisement_id, description=None):
#         """ثبت تراکنش پرداخت به فروشنده (شناسه آگهی الزامی است)"""
#         return Transaction.create(
#             wallet, TransactionType.PAYMENT, amount, description, advertisement_id
#         )
