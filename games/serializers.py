import chess

from django.db import transaction
from rest_framework import serializers

from .models import ChessGame, ChessMove


class PositionSerializer(serializers.Serializer):
    fen = serializers.CharField(
        required=False,
        default=chess.STARTING_FEN
    )

    def validate_fen(self, value):
        try:
            board = chess.Board(value)
        except ValueError as exc:
            raise serializers.ValidationError(
                "Invalid FEN notation."
            ) from exc

        if not board.is_valid():
            raise serializers.ValidationError(
                "Invalid chess position."
            )

        return value


class ChessMoveInputSerializer(serializers.Serializer):
    san = serializers.CharField(max_length=20)


class ChessGameCreateSerializer(serializers.Serializer):
    white_player = serializers.CharField(max_length=100)
    black_player = serializers.CharField(max_length=100)

    moves = ChessMoveInputSerializer(many=True, allow_empty=False)

    result = serializers.ChoiceField(
        choices=["1-0", "0-1", "1/2-1/2", "*"],
        default="*"
    )

    def create(self, validated_data):
        moves_data = validated_data.pop("moves")

        # Validate all moves before saving anything.
        board = chess.Board()
        parsed_moves = []

        for move_number, move_data in enumerate(moves_data, start=1):
            san = move_data["san"]

            try:
                move = board.parse_san(san)
            except (ValueError, AssertionError) as exc:
                raise serializers.ValidationError({
                    "moves": [
                        f"Invalid move {move_number}: {san}"
                    ]
                }) from exc

            board.push(move)

            parsed_moves.append({
                "move_number": move_number,
                "san": san,
                "uci": move.uci(),
                "fen": board.fen(),
            })

        # Save the game and all moves in one transaction.
        with transaction.atomic():
            game = ChessGame.objects.create(**validated_data)

            ChessMove.objects.bulk_create([
                ChessMove(game=game, **move_data)
                for move_data in parsed_moves
            ])

        return game


class ChessMoveOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessMove
        fields = ["move_number", "san", "uci", "fen"]


class ChessGameOutputSerializer(serializers.ModelSerializer):
    moves = ChessMoveOutputSerializer(many=True, read_only=True)

    class Meta:
        model = ChessGame
        fields = [
            "id",
            "white_player",
            "black_player",
            "result",
            "created_at",
            "moves",
        ]