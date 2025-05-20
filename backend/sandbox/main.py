import asyncio
from otp import (
    OTPService,
)  # فرض بر این است که کلاس را در فایل جدا مثل otp_service.py ذخیره کرده‌ای


async def main():
    otp = "123456"  # OTP باید بیرون از کلاس ساخته شود
    phone = "+989223108571"

    service = OTPService()
    result = await service.send_otp(phone, otp)
    print(result)


asyncio.run(main())
