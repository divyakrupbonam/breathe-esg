from django.urls import path

from .views import (
    EmissionListView,
    ApproveEmissionView
)

urlpatterns = [
    path('', EmissionListView.as_view()),

    path(
        '<int:pk>/approve/',
        ApproveEmissionView.as_view()
    ),
]