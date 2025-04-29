"""
Home Views.
"""

from rest_framework import generics
from core.models import Plan
from core.serializers import PlanSerializer


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
