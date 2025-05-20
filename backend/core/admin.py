from django.contrib import admin
from django.contrib.auth import get_user_model

from core.models import Plan, Wallet, Chat

# Register your models here.
User = get_user_model()
admin.site.register(User)

admin.site.register(Plan)
admin.site.register(Wallet)
admin.site.register(Chat)
