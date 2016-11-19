import random
import gamePlay
from getAllPossibleMoves import getAllPossibleMoves

'''This plays as a human vs computer interactively'''
def nextMove(board, color, time, movesRemaining): 

	moved = False
	while moved == False:
		print 'Possible moves:', getAllPossibleMoves(board, color)
		moveStr = raw_input("Please enter your move(" + color + "): ")
		exec('move=[' + moveStr + ']')
						
		if gamePlay.isLegalMove(board, move, color):			
			moved = True			
			return move
		else:
			print "Illegal move", str(move)
		
