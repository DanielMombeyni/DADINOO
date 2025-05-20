# ---------------------------------------------------------------------------- #
#                                  Rate Limit                                  #
# ---------------------------------------------------------------------------- #

import redis
from django.conf import settings
from datetime import timedelta

# اتصال به Redis با استفاده از تنظیمات پروژه
r = redis.Redis(
    host=settings.CHANNEL_LAYERS["default"]["CONFIG"]["hosts"][0][0],
    port=int(settings.CHANNEL_LAYERS["default"]["CONFIG"]["hosts"][0][1]),
    db=0,
    decode_responses=True,  # برای جلوگیری از byte string
)


def is_rate_limited(user_id: int, limit: int = 1, period: int = 2) -> bool:
    """
    بررسی محدودیت ارسال پیام برای کاربر.
    :param user_id: آیدی کاربر
    :param limit: تعداد مجاز پیام‌ها در دوره زمانی
    :param period: بازه زمانی بر حسب ثانیه
    """
    key = f"user:{user_id}:chat_limit"
    current = r.get(key)

    if current and int(current) >= limit:
        return True

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, period)
    pipe.execute()
    return False
