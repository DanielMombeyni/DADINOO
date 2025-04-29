import random

otp_storage = {}  # بهتره Redis یا DB استفاده بشه در تولید


def send_otp(phone):
    otp = str(random.randint(100000, 999999))
    otp_storage[phone] = otp
    print(f"OTP for {phone}: {otp}")  # به جای SMS واقعی
    return otp


def verify_otp(phone, otp):
    return otp_storage.get(phone) == otp
