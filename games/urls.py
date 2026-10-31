from django.urls import path

from .views import (
       analyze_position,
    create_game,
    list_games,
    get_game,
    analyze_game,
    analyze_game_position,
    predict_move,
    dashboard,
)

urlpatterns = [
    path("analyze/", analyze_position, name="analyze-position"),
    path("games/", create_game, name="create-game"),
    path("games/list/", list_games, name="list-games"),
    path("games/<int:game_id>/", get_game, name="get-game"),
    path("games/<int:game_id>/analyze/", analyze_game, name="analyze-game"),
    path("predict/", predict_move, name="predict-move"),
    path("", dashboard, name="dashboard"),
    path(
    "games/<int:game_id>/position/<int:ply>/",
    analyze_game_position,
    name="analyze-game-position",
    ),
]