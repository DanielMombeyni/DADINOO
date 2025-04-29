"""
Home Urls.
"""

from django.urls import path
from api.views import HomeViews


app_name = "Home"

urlpatterns = [
    path("plans/", HomeViews.PlanListView.as_view(), name="plan-list"),
]
