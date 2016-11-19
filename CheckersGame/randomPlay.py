import random
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves

'''Just play randomly among the possible moves'''
def nextMove(board, color, time, movesRemaining):
    moves = getAllPossibleMoves(board, color)    
    bestMove = moves[random.randint(0,len(moves) - 1)]
    return bestMove
