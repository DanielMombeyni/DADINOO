# # ---------------------------------------------------------------------------- #
# #                             Consumer Chat with AI                            #
# # ---------------------------------------------------------------------------- #

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Chat, Message, SenderType, Plan
from chat.services.ai_client import get_ai_response
from core.middleware.rate_limiter import is_rate_limited
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async
from core.utils.wallet import deduct_cost
import logging
from django.db import DatabaseError
import time

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    DEFAULT_PLAN_ID = 8

    async def connect(self):
        """اتصال WebSocket با احراز هویت کاربر"""
        if isinstance(self.scope["user"], AnonymousUser):
            logger.warning("Anonymous user connection attempt")
            await self.close()
            return

        await self.accept()

        logger.info(f"WS connected - User: {self.scope['user'].id}")

    async def disconnect(self, close_code):
        """قطع ارتباط WebSocket"""
        logger.info(f"WS disconnected - Code: {close_code}")
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def safe_send_json(self, data):
        """ارسال ایمن پیام JSON با مدیریت خطاها"""
        try:
            await self.send(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Send failed - Error: {str(e)}", exc_info=True)
            try:
                await self.send(
                    json.dumps(
                        {"type": "error", "error": "خطا در ارسال پیام"},
                        ensure_ascii=False,
                    )
                )
            except Exception as fallback_error:
                logger.critical(f"Fallback send failed - Error: {str(fallback_error)}")

    async def receive(self, text_data):
        """پردازش پیام دریافتی از کاربر"""
        try:
            # پردازش اولیه پیام
            message_data = await self._parse_message_data(text_data)
            if not message_data:
                return

            user = self.scope["user"]
            message_text, chat_id, plan_id, msg_type = message_data

            # مدیریت چت
            chat = await self._handle_chat_operations(user, chat_id, plan_id, msg_type)
            if not chat:
                return

            if not message_text:
                return

            # اعتبارسنجی پیام
            if not await self._validate_message(message_text):
                return

            # بررسی محدودیت ارسال
            if await self._check_rate_limit(user.id):
                return

            # پردازش پرداخت
            payment_status = await self._process_payment(user, chat)
            if not payment_status:
                return

            # ذخیره پیام کاربر
            await self._save_user_message(chat, user, message_text)

            # پردازش و ارسال پاسخ AI
            await self._process_ai_response(chat, user, message_text)

        except DatabaseError as e:
            logger.error(f"Database error - {str(e)}", exc_info=True)
            await self.safe_send_json(
                {"type": "error", "error": "خطای پایگاه داده رخ داده است"}
            )
        except Exception as e:
            logger.error(f"Unexpected error - {str(e)}", exc_info=True)
            await self.safe_send_json(
                {"type": "error", "error": "خطای سرور رخ داده است"}
            )


    async def _process_payment(self, user, chat):
        """مدیریت کامل فرآیند پرداخت"""
        try:
            plan = await sync_to_async(lambda: chat.plan)()
            success, message = await sync_to_async(deduct_cost)(user, plan)
            if not success:
                logger.warning(f"Payment failed - User: {user.id} - Reason: {message}")
                await self.safe_send_json({"type": "error", "error": message})
                return False
            return True
        except Exception as e:
            logger.error(
                f"Payment processing error - User: {user.id} - Error: {str(e)}",
                exc_info=True,
            )
            await self.safe_send_json(
                {"type": "error", "error": "خطا در پردازش پرداخت"}
            )
            return False

    async def _parse_message_data(self, text_data):
        """پارس و اعتبارسنجی داده‌های ورودی"""
        try:
            data = json.loads(text_data)
            return (
                data.get("message", "").strip(),
                data.get("chat_id"),
                data.get("plan_id", self.DEFAULT_PLAN_ID),
                data.get("type"),
            )
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received")
            await self.safe_send_json({"type": "error", "error": "فرمت داده نامعتبر"})
            return None

    async def _validate_message(self, message_text):
        """اعتبارسنجی محتوای پیام"""
        if not message_text or not isinstance(message_text, str):
            await self.safe_send_json(
                {"type": "error", "error": "پیام معتبر ارسال نشده است"}
            )
            return False
        return True

    async def _handle_chat_operations(self, user, chat_id, plan_id, msg_type):
        """مدیریت چت (ایجاد/بازیابی)"""
        try:
            chat = await sync_to_async(self._get_or_create_chat)(user, chat_id, plan_id)
            if not chat:
                await self.safe_send_json(
                    {"type": "error", "error": "خطا در مدیریت چت"}
                )
                return None

            if msg_type == "init":
                await self._send_chat_history(chat)

            return chat
        except Exception as e:
            logger.error(f"Chat operation failed - Error: {str(e)}", exc_info=True)
            return None

    async def _check_rate_limit(self, user_id):
        """بررسی محدودیت ارسال پیام"""
        try:
            if await sync_to_async(is_rate_limited)(user_id):
                await self.safe_send_json(
                    {"type": "error", "error": "پیام‌دهی بیش از حد مجاز"}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Rate limit check failed - Error: {str(e)}", exc_info=True)
            return True

    async def _save_user_message(self, chat, user, message_text):
        """ذخیره پیام کاربر با مدیریت خطاها"""
        try:
            await sync_to_async(self._save_message)(
                chat, user, SenderType.USER, message_text
            )
        except Exception as e:
            logger.error(f"Message save failed - Error: {str(e)}", exc_info=True)
            raise

    async def _process_ai_response(self, chat, user, message_text):
        """پردازش و ارسال پاسخ هوش مصنوعی"""
        try:
            chat_history = await sync_to_async(self._get_chat_history)(chat)

            # اطمینان از کدگذاری صحیح متن
            if isinstance(message_text, bytes):
                message_text = message_text.decode("utf-8")

            ai_response = await get_ai_response(message_text, chat_history)

            # اطمینان از کدگذاری صحیح پاسخ
            if isinstance(ai_response, bytes):
                ai_response = ai_response.decode("utf-8")

            ai_message = await sync_to_async(self._save_message)(
                chat, user, SenderType.POSTMAN, ai_response
            )

            await self.safe_send_json(
                {
                    "id": ai_message.id,
                    "response": ai_response,
                    "type": "ai",
                    "chat_id": chat.id,
                    "timestamp": int(time.time()),
                }
            )

        except Exception as e:
            logger.error(f"AI processing error: {str(e)}", exc_info=True)
            await self.safe_send_json(
                {
                    "type": "error",
                    "error": "خطا در پردازش درخواست",
                    "timestamp": int(time.time()),
                }
            )

    def _get_or_create_chat(self, user, chat_id, plan_id):
        """مدیریت چت به صورت همگام"""
        try:
            if chat_id:
                chat = (
                    Chat.objects.select_related("plan")
                    .filter(id=chat_id, user=user)
                    .first()
                )
                if chat:
                    return chat

            plan = Plan.objects.get(id=plan_id)

            # بررسی وجود چت قبلی با همین پلن
            existing_chat = Chat.objects.filter(user=user, plan=plan).first()
            if existing_chat:
                return existing_chat

            # اگر چت موجود نبود، ایجاد جدید
            return Chat.objects.create(user=user, plan=plan)

        except Plan.DoesNotExist:
            logger.error(f"Plan not found - ID: {plan_id}")
            return None
        except Exception as e:
            logger.error(f"Chat creation failed - Error: {str(e)}", exc_info=True)
            return None

    def _get_chat_history(self, chat):
        """دریافت تاریخچه چت"""
        messages = Message.objects.filter(chat=chat).order_by("created_at")
        print(f"history Message: {messages}")
        return "\n".join(
            f"{'کاربر' if m.sender_type == SenderType.USER else 'دستیار'}: {m.message_text}"
            for m in messages
        )

    def _save_message(self, chat, user, sender_type, text):
        """ذخیره پیام در دیتابیس"""
        return Message.objects.create(
            chat=chat, sender=user, sender_type=sender_type, message_text=text
        )

    async def _send_chat_history(self, chat):
        """ارسال تاریخچه چت به کاربر"""
        messages = await sync_to_async(list)(
            Message.objects.filter(chat=chat).order_by("created_at")
        )

        for msg in messages:
            await self.safe_send_json(
                {
                    "id": msg.id,
                    "message": msg.message_text,
                    "type": "user" if msg.sender_type == SenderType.USER else "ai",
                    "is_history": True,
                    "timestamp": int(msg.created_at.timestamp()),
                }
            )
