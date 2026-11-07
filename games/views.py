import chess
import chess.engine

from django.db import transaction
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChessGame, ChessMove
from .serializers import (
    PositionSerializer,
    ChessGameCreateSerializer,
    ChessGameOutputSerializer,
)

from .engine import analyze_chess_position
from django.shortcuts import render

from .chatbot import generate_chess_explanation

from openai import (
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

@api_view(["POST"])
def analyze_position(request):
    serializer = PositionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    board = chess.Board(serializer.validated_data["fen"])

    legal_moves = [
        {
            "uci": move.uci(),
            "san": board.san(move)
        }
        for move in board.legal_moves
    ]

    if board.is_checkmate():
        game_status = "checkmate"
    elif board.is_stalemate():
        game_status = "stalemate"
    elif board.is_check():
        game_status = "check"
    elif board.is_game_over():
        game_status = "game_over"
    else:
        game_status = "active"

    return Response({
        "success": True,
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "game_status": game_status,
        "legal_move_count": len(legal_moves),
        "legal_moves": legal_moves
    })


@api_view(["POST"])
def create_game(request):
    serializer = ChessGameCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        game = serializer.save()

    return Response(
        {
            "success": True,
            "message": "Chess game saved successfully",
            "game_id": game.id,
            "white_player": game.white_player,
            "black_player": game.black_player,
            "result": game.result,
            "move_count": game.moves.count()
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def list_games(request):
    games = ChessGame.objects.prefetch_related("moves").order_by("-created_at")
    serializer = ChessGameOutputSerializer(games, many=True)

    return Response({
        "success": True,
        "count": len(serializer.data),
        "games": serializer.data,
    })


@api_view(["GET"])
def get_game(request, game_id):
    try:
        game = ChessGame.objects.prefetch_related("moves").get(id=game_id)
    except ChessGame.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Chess game not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ChessGameOutputSerializer(game)

    return Response({
        "success": True,
        "game": serializer.data
    })


@api_view(["GET"])
def analyze_game(request, game_id):
    try:
        game = ChessGame.objects.prefetch_related("moves").get(id=game_id)
    except ChessGame.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Chess game not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # Reconstruct the current board from saved moves.
    moves = list(game.moves.all())
    board = chess.Board()

    for move in moves:
        board.push_uci(move.uci)

    # Determine the current game status.
    if board.is_checkmate():
        game_status = "checkmate"
    elif board.is_stalemate():
        game_status = "stalemate"
    elif board.is_check():
        game_status = "check"
    elif board.is_game_over():
        game_status = "game_over"
    else:
        game_status = "active"

    # Find all legal moves.
    legal_moves = [
        {
            "uci": move.uci(),
            "san": board.san(move)
        }
        for move in board.legal_moves
    ]

    # Analyze the current position using Stockfish.
    best_moves = []
    engine_message = "Position analyzed successfully."

    if board.is_game_over():
        engine_message = "Game is over. No further moves are available."
    else:
        try:
            analysis = analyze_chess_position(
                fen=board.fen(),
                time_limit=1.0,
                multipv=3,
            )
            best_moves = analysis["candidates"]

        except (ValueError, TypeError):
            engine_message = "Could not analyze the chess position."

        except chess.engine.EngineError:
            engine_message = "Chess engine analysis failed."

        except OSError:
            engine_message = "Stockfish engine could not be started."

    return Response({
        "success": True,
        "message": engine_message,
        "game_id": game.id,
        "white_player": game.white_player,
        "black_player": game.black_player,
        "result": game.result,
        "total_moves": len(moves),
        "current_fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "in_check": board.is_check(),
        "game_status": game_status,
        "legal_move_count": len(legal_moves),
        "legal_moves": legal_moves,
        "best_moves": best_moves,
    })


@api_view(["POST"])
def predict_move(request):
    fen = request.data.get("fen")

    try:
        result = analyze_chess_position(
            fen=fen,
            time_limit=1.0,
            multipv=3,
        )
    except (ValueError, TypeError):
        return Response(
            {
                "success": False,
                "message": "Invalid chess position or FEN."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except chess.engine.EngineError:
        return Response(
            {
                "success": False,
                "message": "Chess engine analysis failed."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except OSError:
        return Response(
            {
                "success": False,
                "message": "Stockfish engine could not be started."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response({
        "success": True,
        "message": "Chess position analyzed successfully.",
        **result,
    })

from django.shortcuts import render


def dashboard(request):
    return render(request, "games/dashboard.html")

@api_view(["GET"])
def analyze_game_position(request, game_id, ply):
    """
    Analyze a position from a saved game.

    ply=0 means the starting position.
    ply=1 means after White's first move.
    ply=2 means after Black's first move.
    """
    try:
        game = ChessGame.objects.prefetch_related("moves").get(id=game_id)
    except ChessGame.DoesNotExist:
        return Response(
            {"success": False, "message": "Chess game not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    moves = list(game.moves.all())

    if ply < 0 or ply > len(moves):
        return Response(
            {
                "success": False,
                "message": "Requested position is outside the recorded game.",
                "available_plies": len(moves),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    board = chess.Board()

    for move in moves[:ply]:
        board.push_uci(move.uci)

    try:
        analysis = analyze_chess_position(
            fen=board.fen(),
            time_limit=1.0,
            multipv=3,
        )
    except (ValueError, TypeError):
        return Response(
            {"success": False, "message": "Invalid chess position."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except chess.engine.EngineError:
        return Response(
            {"success": False, "message": "Chess engine analysis failed."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except OSError:
        return Response(
            {"success": False, "message": "Stockfish could not be started."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response({
        "success": True,
        "game_id": game.id,
        "ply": ply,
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "in_check": board.is_check(),
        "game_status": (
            "checkmate" if board.is_checkmate()
            else "stalemate" if board.is_stalemate()
            else "check" if board.is_check()
            else "game_over" if board.is_game_over()
            else "active"
        ),
        "candidates": analysis["candidates"],
    })


@api_view(["POST"])
def chess_chat(request):
    """
    ChessVision AI chatbot.
    Uses Stockfish for chess analysis and OpenAI for explanations.
    """

    fen = request.data.get("fen")
    question = request.data.get("question", "").strip()
    history = request.data.get("history", [])

    if not fen or not question:
        return Response(
            {
                "success": False,
                "message": "Both FEN and question are required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(question) > 1000:
        return Response(
            {
                "success": False,
                "message": "Question must be 1000 characters or fewer."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not isinstance(history, list):
        return Response(
            {
                "success": False,
                "message": "History must be a list."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        board = chess.Board(fen)

        if not board.is_valid():
            raise ValueError("Invalid chess position.")

    except (ValueError, TypeError):
        return Response(
            {
                "success": False,
                "message": "Invalid chess position or FEN."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if board.is_game_over():
            engine_analysis = {
                "message": "The game is over.",
                "candidates": [],
            }
        else:
            engine_analysis = analyze_chess_position(
                fen=board.fen(),
                time_limit=1.0,
                multipv=3,
            )

        # Keep only a small amount of recent conversation context.
        safe_history = []

        for item in history[-6:]:
            if (
                isinstance(item, dict)
                and item.get("role") in ("user", "assistant")
                and isinstance(item.get("content"), str)
            ):
                safe_history.append({
                    "role": item["role"],
                    "content": item["content"][:1000],
                })

        answer = generate_chess_explanation(
            fen=board.fen(),
            question=question,
            engine_analysis=engine_analysis,
            history=safe_history,
        )

        return Response({
            "success": True,
            "fen": board.fen(),
            "turn": "white" if board.turn == chess.WHITE else "black",
            "best_moves": engine_analysis.get("candidates", []),
            "answer": answer,
        })

    except ValueError as error:
        return Response(
            {"success": False, "message": str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except RateLimitError:
        return Response(
            {
                "success": False,
                "message": "OpenAI API rate limit or quota reached."
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    except APIConnectionError:
        return Response(
            {
                "success": False,
                "message": "Could not connect to OpenAI."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    except (APIStatusError, chess.engine.EngineError, OSError):
        return Response(
            {
                "success": False,
                "message": "AI or Stockfish service is temporarily unavailable."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )