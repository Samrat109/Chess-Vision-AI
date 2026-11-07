import os
import json
from openai import OpenAI


def generate_chess_explanation(
    fen,
    question,
    engine_analysis,
    history=None,
):
    """Explain Stockfish analysis in simple language using OpenAI."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API key is not configured.")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    context = {
        "fen": fen,
        "stockfish_analysis": engine_analysis,
        "conversation_history": history or [],
    }

    instructions = """
    You are ChessVision AI, a friendly chess coach.

    Explain chess positions in simple language for beginner
    and intermediate players.

    Rules:
    1. Use Stockfish analysis as the source of chess calculations.
    2. Never invent engine evaluations or moves.
    3. Explain the candidate moves supplied by Stockfish.
    4. Explain tactical ideas, threats, and positional weaknesses.
    5. If information is insufficient, say so.
    6. Focus on completed games and practice positions.
    """

    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=[
            {
                "role": "user",
                "content": (
                    "Chess information:\n"
                    + json.dumps(context)
                    + "\n\nQuestion:\n"
                    + question
                ),
            }
        ],
        max_output_tokens=700,
        store=False,
    )

    return response.output_text