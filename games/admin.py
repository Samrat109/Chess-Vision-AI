from django.contrib import admin
from .models import ChessGame, ChessMove


class ChessMoveInline(admin.TabularInline):
    model = ChessMove
    extra = 0


@admin.register(ChessGame)
class ChessGameAdmin(admin.ModelAdmin):
    list_display = ("id", "white_player", "black_player", "result", "created_at")
    search_fields = ("white_player", "black_player")
    list_filter = ("result",)
    inlines = [ChessMoveInline]


@admin.register(ChessMove)
class ChessMoveAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "move_number", "san", "uci")
    list_filter = ("game",)