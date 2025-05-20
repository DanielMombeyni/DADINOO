# ---------------------------------------------------------------------------- #
#                         JWT Authentication Middleware                        #
# ---------------------------------------------------------------------------- #

from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())

        token = query_string.get("token", [None])[0]

        if token:
            try:
                from rest_framework.authtoken.models import Token

                token_obj = await sync_to_async(Token.objects.get)(key=token)
                user = await sync_to_async(lambda: token_obj.user)()
                scope["user"] = user
            except Token.DoesNotExist:
                scope["user"] = AnonymousUser()
                logger.warning(f"توکن نامعتبر یا کاربر یافت نشد.")
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
