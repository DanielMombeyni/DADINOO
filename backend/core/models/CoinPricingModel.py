"""
Coin Pricing.
"""

from django.db import models


class CoinPricing(models.Model):
    title = models.CharField(max_length=255)  # مثلاً "پکیج طلایی"
    coin_amount = models.PositiveIntegerField()  # تعداد سکه‌ها
    original_price = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت اصلی
    discount_percent = models.PositiveIntegerField(default=0)  # درصد تخفیف (0 تا 100)

    @property
    def final_price(self):
        return self.original_price * (1 - self.discount_percent / 100)

    def __str__(self):
        return f"{self.title} - {self.coin_amount} سکه"
