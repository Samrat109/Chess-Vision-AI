from django.urls import path
from django.http import JsonResponse


def positions_home(request):
    return JsonResponse({
        "status": "success",
        "message": "ChessVision Positions API is working"
    })


urlpatterns = [
    path("", positions_home, name="positions-home"),
]
