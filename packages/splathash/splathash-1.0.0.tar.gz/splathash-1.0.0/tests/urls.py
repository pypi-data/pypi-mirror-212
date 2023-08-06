from django.contrib import admin
from django.urls import include, path

from .test_app.views import USSDView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("splathash/", include("splathash.urls")),
    path("ussd/", USSDView.as_view()),
]
