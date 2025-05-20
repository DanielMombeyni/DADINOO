# ---------------------------------------------------------------------------- #
#                              Transaction Service                             #
# ---------------------------------------------------------------------------- #

from enum import Enum
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from core.models import (
    Transaction,
    TransactionType,
    TransactionStatus,
)

User = get_user_model()


class WalletTransactionType(Enum):
    DEPOSIT = TransactionType.Deposit
    WITHDRAWAL = TransactionType.Withdrawal
    REFUND = TransactionType.REFUND
    CHARGE = TransactionType.Charge
    DISCOUNT = TransactionType.Discount


class TransactionService:
    @staticmethod
    def create(
        user: User,  # type: ignore
        transaction_type: WalletTransactionType,
        amount: float,
        related_id: int = None,
        description: str = None,
        source_account: str = None,
        destination_account: str = None,
        status: int = TransactionStatus.Success,
    ) -> Transaction:
        """
        ایجاد و ذخیره تراکنش در دیتابیس.

        Args:
            user (User): کاربر دریافت‌کننده یا صاحب تراکنش.
            transaction_type (WalletTransactionType): نوع تراکنش (واریز، برداشت و...).
            amount (float): مبلغ تراکنش.
            related_id (int, optional): آی‌دی مرتبط (مثل آگهی یا سفارش).
            description (str, optional): توضیحات تراکنش.
            source_account (str, optional): حساب مبدا.
            destination_account (str, optional): حساب مقصد.
            status (int): وضعیت تراکنش.

        Returns:
            Transaction: شیء ایجاد شده تراکنش.
        """

        default_descriptions = {
            WalletTransactionType.DEPOSIT: f"واریز به کیف پول",
            WalletTransactionType.WITHDRAWAL: f"برداشت از کیف پول",
            WalletTransactionType.REFUND: f"بازگشت مبلغ",
            WalletTransactionType.CHARGE: f"پرداخت هزینه",
            WalletTransactionType.DISCOUNT: f"اعمال تخفیف",
        }

        if description is None:
            description = default_descriptions.get(transaction_type, "تراکنش")

        transaction = Transaction.objects.create(
            user=user,
            transaction_type=transaction_type.value,
            amount=amount,
            related_id=related_id,
            description=description,
            source_account=source_account,
            destination_account=destination_account,
            status=status,
            created_at=now(),
            transaction_date=now(),
        )

        return transaction
