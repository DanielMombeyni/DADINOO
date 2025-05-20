# ---------------------------------------------------------------------------- #
#                                  OTP Service                                 #
# ---------------------------------------------------------------------------- #

import httpx
import json
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class OTPService:
    def __init__(self):

        self.api_url = "https://api2.ippanel.com/api/v1/sms/send/webservice/single"
        self.pattern_url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

        self.token = settings.IPPANEL_API_KEY
        self.sender = settings.IPPANEL_SENDER_NUMBER
        # self.templates = self.load_templates()

    def load_templates(self):
        """
        پیام‌ها را از فایل JSON بخوان
        """
        try:
            templates_path = os.path.join(
                settings.BASE_DIR, "core", "templates", "SMSTemplates.json"
            )
            with open(templates_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.exception("خطا در خواندن فایل SMSTemplates.json")
            return {}

    def render_template(self, template_name, context: dict):
        """
        متن قالب را با جایگزینی مقادیر از context برگردان
        """
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        return template.format(**context)

    async def send_otp(self, phone_number: str, otp: str):
        """
        ارسال OTP به صورت پیام متنی معمولی (بدون الگو)
        """
        try:
            message = self.render_template("otp", {"otp": otp})

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
                response = await client.post(
                    self.api_url, json=payload, headers=headers
                )

            if response.status_code == 200:
                return {"status": "sent", "otp": otp}
            else:
                error_data = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                logger.warning(f"OTP send failed: {error_data}")
                return {
                    "status": "failed",
                    "http_status": response.status_code,
                    "error": error_data,
                }
        except Exception as e:
            logger.exception("Exception while sending OTP")
            return {"status": "error", "message": str(e)}

    async def send_pattern_otp(
        self, phone_number: str, otp: str, pattern_code: str = "i81jso4bv5z7ewm"
    ):
        """
        ارسال OTP با استفاده از الگو (Pattern)
        """
        try:
            payload = {
                "code": pattern_code,
                "sender": self.sender,
                "recipient": phone_number,
                "variable": {"verification-code": otp},
            }

            headers = {
                "apikey": self.token,
                "Content-Type": "application/json",
                "accept": "*/*",
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.pattern_url, json=payload, headers=headers
                )

            if response.status_code == 200:
                return {"status": "sent", "otp": otp}
            else:
                error_data = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                logger.warning(f"Pattern OTP send failed: {error_data}")
                return {
                    "status": "failed",
                    "http_status": response.status_code,
                    "error": error_data,
                }
        except Exception as e:
            logger.exception("Exception while sending pattern OTP")
            return {"status": "error", "message": str(e)}
