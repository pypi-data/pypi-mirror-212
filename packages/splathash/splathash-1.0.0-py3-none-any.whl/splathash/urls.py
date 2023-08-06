from django.urls import path

from . import views

urlpatterns = [
    path("playground/", views.ussd_web_tester),
]
