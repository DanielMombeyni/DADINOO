# from core.models import SecurePayment
# from django.db import transaction


# class PaymentStatus:
#     PENDING = 1
#     COMPLETED = 2
#     CANCELLED = 3
#     DISPUTED = 4


# class Payment:
#     @staticmethod
#     def Create(advertisement, buyer):
#         """
#         ایجاد پرداخت جدید برای آگهی.

#         :param advertisement: آگهی مرتبط با پرداخت
#         :param buyer: خریدار
#         :return: نمونه SecurePayment ایجاد شده
#         """
#         return SecurePayment.objects.create(
#             advertisement=advertisement,
#             buyer=buyer,
#             seller=advertisement.user,
#             amount=advertisement.price,
#             status=PaymentStatus.PENDING,
#         )

#     @staticmethod
#     def Cancel(secure_payment):
#         """
#         لغو پرداخت و تغییر وضعیت به 'Cancelled'.

#         :param secure_payment: نمونه پرداخت
#         :return: نمونه به‌روزرسانی شده SecurePayment
#         """
#         with transaction.atomic():
#             secure_payment.status = PaymentStatus.CANCELLED
#             secure_payment.save()
#             # بازگشت وجه به خریدار
#             secure_payment.buyer.wallet.balance += secure_payment.amount
#             secure_payment.buyer.wallet.save()
#             return secure_payment

#     @staticmethod
#     def Complete(secure_payment):
#         """
#         تأیید پرداخت و تغییر وضعیت به 'Completed'.

#         :param secure_payment: نمونه پرداخت
#         :return: نمونه به‌روزرسانی شده SecurePayment
#         """
#         with transaction.atomic():
#             secure_payment.status = PaymentStatus.COMPLETED
#             secure_payment.save()
#             # انتقال وجه به فروشنده
#             secure_payment.seller.wallet.balance += secure_payment.amount
#             secure_payment.seller.wallet.save()
#             return secure_payment

#     @staticmethod
#     def Dispute(secure_payment):
#         """
#         قرار دادن پرداخت در وضعیت 'Disputed'.

#         :param secure_payment: نمونه پرداخت
#         :return: نمونه به‌روزرسانی شده SecurePayment
#         """
#         secure_payment.status = PaymentStatus.DISPUTED
#         secure_payment.save()
#         return secure_payment
