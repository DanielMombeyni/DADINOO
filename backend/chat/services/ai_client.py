# # ---------------------------------------------------------------------------- #
# #                                  AI Service                                  #
# # ---------------------------------------------------------------------------- #

# import os
# import httpx
# from httpx import HTTPStatusError, RequestError
# from dotenv import load_dotenv

# load_dotenv()

# AIML_API_URL = os.getenv("AIML_API_URL")
# DEFAULT_MODEL = os.getenv("AIML_MODEL")
# DEFAULT_API_KEY = os.getenv("AIML_API_KEY")


# async def get_ai_response(
#     message: str, api_key: str = DEFAULT_API_KEY, model: str = DEFAULT_MODEL
# ) -> str:
#     if not api_key:
#         return "کلید API مشخص نشده است."

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }

#     payload = {
#         "model": model,
#         "messages": [{"role": "user", "content": message}],
#     }

#     async with httpx.AsyncClient(timeout=10.0) as client:
#         try:
#             response = await client.post(AIML_API_URL, headers=headers, json=payload)
#             response.raise_for_status()
#             data = response.json()
#             return data["choices"][0]["message"]["content"]
#         except HTTPStatusError as http_err:
#             return f"خطای سرور AI: {http_err.response.status_code} - {http_err.response.text}"
#         except RequestError as req_err:
#             return f"عدم دسترسی به سرور AI: {str(req_err)}"
#         except (KeyError, IndexError) as parse_err:
#             return f"خطا در پردازش پاسخ AI: {str(parse_err)}"
#         except Exception as e:
#             return f"خطای نامشخص: {str(e)}"


import os
import httpx
from httpx import HTTPStatusError, RequestError
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


async def get_ai_response(
    message: str,
    chat_history: str = None,
    api_key: str = settings.DEFAULT_API_KEY,
    model: str = settings.DEFAULT_MODEL,
) -> str:
    """
    دریافت پاسخ از سرویس هوش مصنوعی با پشتیبانی از کاراکترهای فارسی

    پارامترها:
        message: پیام کاربر (حتماً باید یونیکد باشد)
        chat_history: تاریخچه چت به صورت متن
        api_key: کلید API
        model: مدل مورد استفاده

    بازگشت:
        پاسخ هوش مصنوعی به صورت رشته یونیکد
    """
    if not api_key:
        return "کلید API مشخص نشده است."

    # اطمینان از یونیکد بودن ورودی
    if isinstance(message, bytes):
        try:
            message = message.decode("utf-8")
        except UnicodeDecodeError:
            return "خطا در کدگذاری پیام ورودی"

    # ساخت payload با پشتیبانی از فارسی
    messages = [{"role": "user", "content": message}]

    # اضافه کردن تاریخچه چت اگر وجود دارد
    if chat_history:
        messages.insert(
            0,
            {
                "role": "system",
                "content": f"تاریخچه چت:\n{chat_history}\n\nلطفا به آخرین پیام کاربر پاسخ دهید.",
            },
        )

    payload = {
        "model": model,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # ارسال درخواست با پشتیبانی از یونیکد
            response = await client.post(
                settings.AIML_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                json=payload,
            )
            response.raise_for_status()

            # پردازش پاسخ با مدیریت خطاهای کدگذاری
            try:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as parse_err:
                logger.error(f"Error parsing AI response: {str(parse_err)}")
                return "خطا در پردازش پاسخ هوش مصنوعی"
            except json.JSONDecodeError:
                logger.error("Invalid JSON response from AI service")
                return "پاسخ نامعتبر از سرویس هوش مصنوعی"

        except HTTPStatusError as http_err:
            logger.error(
                f"AI API error: {http_err.response.status_code} - {http_err.response.text}"
            )
            return f"خطای سرور هوش مصنوعی: {http_err.response.status_code}"
        except RequestError as req_err:
            logger.error(f"AI connection error: {str(req_err)}")
            return "عدم دسترسی به سرویس هوش مصنوعی"
        except Exception as e:
            logger.error(f"Unexpected AI error: {str(e)}", exc_info=True)
            return "خطای نامشخص در سرویس هوش مصنوعی"
