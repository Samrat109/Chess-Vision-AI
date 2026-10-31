from django.db import models


class ChessGame(models.Model):
    white_player = models.CharField(max_length=100)
    black_player = models.CharField(max_length=100)

    result = models.CharField(
        max_length=10,
        default="*",
        help_text="1-0, 0-1, 1/2-1/2, or * for unfinished"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.white_player} vs {self.black_player}"


class ChessMove(models.Model):
    game = models.ForeignKey(
        ChessGame,
        on_delete=models.CASCADE,
        related_name="moves"
    )

    move_number = models.PositiveIntegerField()
    san = models.CharField(max_length=20)
    uci = models.CharField(max_length=10)
    fen = models.TextField()

    class Meta:
        ordering = ["move_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["game", "move_number"],
                name="unique_move_number_per_game"
            )
        ]

    def __str__(self):
        return f"Game {self.game_id}, move {self.move_number}: {self.san}"