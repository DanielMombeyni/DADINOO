from django.db import transaction
from core.services.TransactionService import (
    TransactionService,
    WalletTransactionType,
    TransactionStatus,
)
import logging

logger = logging.getLogger(__name__)


def deduct_cost(user, plan):
    """
    کسر هزینه از کیف پول کاربر با مدیریت تراکنش و خطاها

    پارامترها:
        user: شیء کاربر
        plan: شیء پلن انتخابی

    بازگشت:
        tuple: (status: bool, message: str)
    """
    try:
        # محاسبه هزینه (1% قیمت پلن)
        cost = plan.price / 100

        # اعتبارسنجی ورودی‌ها
        if not hasattr(user, "wallet"):
            logger.error(f"User {user.id} has no wallet attached")
            return False, "سیستم کیف پول برای کاربر فعال نیست"

        if not plan or not plan.price:
            logger.error(f"Invalid plan provided for user {user.id}")
            return False, "پلن انتخاب شده معتبر نیست"

        with transaction.atomic():
            # تازه‌سازی موجودی از دیتابیس برای جلوگیری از شرایط رقابتی
            user.wallet.refresh_from_db()

            # بررسی موجودی کافی
            if user.wallet.balance < cost:
                logger.warning(
                    f"Insufficient balance for user {user.id}. Current: {user.wallet.balance}, Required: {cost}"
                )
                return False, "موجودی کیف پول کافی نیست"

            # کسر هزینه
            user.wallet.balance -= cost
            user.wallet.save()

            # ثبت تراکنش
            TransactionService.create(
                user=user,
                transaction_type=WalletTransactionType.WITHDRAWAL,
                amount=cost,
                related_id=plan.id,
                description=f"پرداخت بابت پلن {plan.name}",
                status=TransactionStatus.Success,
            )

            logger.info(
                f"Successfully deducted {cost} from user {user.id}. New balance: {user.wallet.balance}"
            )
            return True, "پرداخت با موفقیت انجام شد"

    except Exception as e:
        logger.error(
            f"Error in deducting cost for user {user.id}: {str(e)}", exc_info=True
        )
        return False, "خطا در پردازش پرداخت"
