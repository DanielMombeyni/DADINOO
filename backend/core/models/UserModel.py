"""
Database Models.
"""

from django.conf import settings  # type:ignore
from django.db import models  # type:ignore
from django.contrib.auth.models import (  # type:ignore
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import pre_save  # type:ignore
from django.dispatch import receiver  # type:ignore
from datetime import timedelta
from django.utils.timezone import now  # type:ignore


class UserManager(BaseUserManager):
    """Manager for user"""

    # def create_user(self, email: str, password: str, **extra_fields: dict):
    #     """Create, save and return a new user"""
    #     if not email:
    #         raise ValueError("User must have an email address.")
    #     user = self.model(email=self.normalize_email(email), **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)

    #     return user

    def create_user(self, phone_number, password=None):
        user = self.model(phone_number=phone_number)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        if not password:
            raise ValueError("رمز عبور برای سوپریوزر الزامی است.")

        user = self.create_user(phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)
    # email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=15)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Reset Password
    password_reset_token = models.CharField(max_length=128, null=True, blank=True)
    password_reset_token_expires = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    def generate_password_reset_token(self):
        """Generate a password reset token and expiry."""
        import secrets

        self.password_reset_token = secrets.token_hex(16)
        self.password_reset_token_expires = now() + timedelta(
            hours=1
        )  # Token expires in 1 hour
        self.save(
            update_fields=["password_reset_token", "password_reset_token_expires"]
        )
        return self.password_reset_token

    def clear_password_reset_token(self):
        """Clear the password reset token and expiry."""
        self.password_reset_token = None
        self.password_reset_token_expires = None
        self.save()

    class Meta:
        indexes = [
            models.Index(name="fullname", fields=["first_name", "last_name"]),
        ]
