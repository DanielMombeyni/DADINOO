import httpx


class OTPService:
    def __init__(self):
        self.api_url = "https://api2.ippanel.com/api/v1/sms/send/webservice/single"
        self.token = "OWVlODg5ZTItZTlhZi00ODlhLTg2M2UtYTUwMDBhNWFhZjZmODVhZTdjYzI2YmJiOWUyOGFhZDM4YzljMTZjNzdkZGI="
        self.sender = "+983000505"

    def render_message(self, otp):
        return f"""\
دادینو
👋 خوش آمدید!
دستیار حقوقی دادینو آماده خدمت‌رسانی به شماست.

کد تأیید شما: {otp}
این کد به مدت ۲ دقیقه معتبر است.

اگر شما درخواست ورود نکرده‌اید، این پیام را نادیده بگیرید.
"""

    async def send_otp(self, phone_number: str, otp: str):
        message = self.render_message(otp)

        payload = {
            "recipient": [phone_number],
            "sender": self.sender,
            "message": message,
        }

        headers = {
            "apikey": self.token,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, json=payload, headers=headers)

        if response.status_code == 200:
            return {"status": "sent", "otp": otp}
        else:
            try:
                error_data = response.json()
            except Exception:
                error_data = response.text  # نمایش متن خام اگه JSON نبود

            return {
                "status": "failed",
                "http_status": response.status_code,
                "error": error_data,
            }
