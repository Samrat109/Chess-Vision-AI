from django.contrib import admin
from django.urls import path, include
from games.views import dashboard

urlpatterns = [
    path("", dashboard, name="home"),
    path("admin/", admin.site.urls),
    path("api/positions/", include("games.urls")),
]