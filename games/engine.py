import chess
import chess.engine

STOCKFISH_PATH = "/usr/games/stockfish"


def analyze_chess_position(fen=None, time_limit=1.0, multipv=3):
    """Analyze a chess position and return the best candidate moves."""

    board = chess.Board(fen) if fen else chess.Board()

    if not board.is_valid():
        raise ValueError("Invalid chess position.")

    multipv = max(1, min(int(multipv), 5))
    time_limit = max(0.1, min(float(time_limit), 5.0))

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        engine.configure({"Threads": 1, "Hash": 64})

        analyses = engine.analyse(
            board,
            chess.engine.Limit(time=time_limit),
            multipv=multipv,
        )

    if isinstance(analyses, dict):
        analyses = [analyses]

    candidates = []

    for analysis in analyses:
        pv = analysis.get("pv", [])
        if not pv:
            continue

        best_move = pv[0]
        score = analysis["score"].pov(board.turn)

        candidates.append({
            "uci": best_move.uci(),
            "san": board.san(best_move),
            "evaluation": {
                "centipawns": score.score(),
                "mate_in": score.mate(),
            },
            "principal_variation": [
                board.variation_san(pv)
            ][0],
            "depth": analysis.get("depth"),
        })

    return {
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "candidates": candidates,
    }
