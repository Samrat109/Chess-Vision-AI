import chess

board = chess.Board()

print("CHESSVISION AI")
print("-------------------")

print(board)

print("\nCurrent FEN:")
print(board.fen())

print("\nLegal moves:")
print(board.legal_moves.count())

print("\nFirst 5 legal moves:")

for move in list(board.legal_moves)[:5]:
    print(board.san(move))
