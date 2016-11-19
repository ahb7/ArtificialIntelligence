import gamePlay
import math
#import datetime
#import time
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

'''
This plays the game using MiniMax Algorithm with Alpha-Beta Prunning.
Several evaluation functions used to find the best move.
'''
# This function checks if this is the first move
def isFirstMove(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value1 = 0
    value2 = 0
    # Loop through the middle two rows
    for piece in range(13, 21):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            value1 = value1 + 1
        elif board[x][y].upper() == opponentColor.upper():
            value1 = value1 + 1
    
    # Loop through all the rows
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            value2 = value2 + 1
        elif board[x][y].upper() == opponentColor.upper():
            value2 = value2 + 1
    # If it is first move middle two rows have one or less piece
    if value2 == 24 and value1 <= 1:
        return True
    else:
        return False 


# This function returns which phase the game is in
# 19-24 pieces -> Phase 1, 10-18 -> Phase 2, 10 or less -> Phase 3
def gamePhase(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value2 = 0
    
    # Loop through all the rows
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            value2 = value2 + 1
        elif board[x][y].upper() == opponentColor.upper():
            value2 = value2 + 1
    if value2 > 18 and value2 <= 24:
        return 1
    elif value2 > 10 and value2 <= 18:
        return 2 
    else:
        return 3 


# Evaluation function 1
# Count how many pieces I have  more than opponent
def evaluation1(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value = 0
    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            value = value + 1
        elif board[x][y].upper() == opponentColor.upper():
            value = value - 1
    
    # Let us give weightage 10
    #return value * 10
    return value 


# Evaluation function 2
# Count how many kings I have more than opponent 
# Please note kings already counted once in evaluation 1
def evaluation2(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value = 0
    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y] == color.upper():
            value = value + 1
        elif board[x][y] == opponentColor.upper():
            value = value - 1
    
    # Let us give extra weightage 10 
    #return value * 10 
    return value  


# Evaluation function 3
# Count how many double-capture opportunity I have vs opponent
def evaluation3(board, color):
    
    opColor = gamePlay.getOpponentColor(color)
    
    value = 0
    
    # Loop through all board positions
    for piece in range(1, 33):
        # Check if I can capture two
        # Check whether a jump possible to all four directions
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if gamePlay.canMoveToPosition(board, x, y, x-2, y-2) == True:
            if gamePlay.isCapturePossibleFromPosition(board, x-2, y-2):
                if board[x][y].upper() == color.upper():
                    value = value + 1
                elif board[x][y].upper() == opColor.upper():
                    value = value - 1
        if gamePlay.canMoveToPosition(board, x, y, x-2, y+2) == True:
            if gamePlay.isCapturePossibleFromPosition(board, x-2, y+2):
                if board[x][y].upper() == color.upper():
                    value = value + 1
                elif board[x][y].upper() == opColor.upper():
                    value = value - 1
        if gamePlay.canMoveToPosition(board, x, y, x+2, y-2) == True:
            if gamePlay.isCapturePossibleFromPosition(board, x+2, y-2):
                if board[x][y].upper() == color.upper():
                    value = value + 1
                elif board[x][y].upper() == opColor.upper():
                    value = value - 1
        if gamePlay.canMoveToPosition(board, x, y, x+2, y+2) == True:
            if gamePlay.isCapturePossibleFromPosition(board, x+2, y+2):
                if board[x][y].upper() == color.upper():
                    value = value + 1
                elif board[x][y].upper() == opColor.upper():
                    value = value - 1

    # Lets give weightage 10
    # Let us give extra weightage 10 
    return value 
    

# Evaluation function 4
# This evaluation returns value for net central positioning
# If my pieces are more at the centre, thats a positive thing 
def evaluation4(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    
    value = 0
    # Loop through all board positions in the list with weightage 4, 3, 2, 1
    # The follwoing positions are at edge across the square board
    #list1 = [1, 2, 3, 4, 5, 12, 13, 20, 21, 28, 29, 30, 31, 32]
    # This is 2 level deep from the edge across the square board
    #list2 = [6, 7, 8, 9, 16, 17, 24, 25, 26, 27]
    # This is 3 level deep from the edge across the square board
    list3 = [10, 11, 14, 19, 22, 23]
    # This is 4 level deep from the edge across the square board
    list4 = [15, 18]

    for piece in list3:
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == color.upper():
            value = value + 1
        elif board[x][y].upper() == opponentColor.upper():
            value = value - 1

    for piece in list4:
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
        if board[x][y].upper() == color.upper():
            value = value + 2
        elif board[x][y].upper() == opponentColor.upper():
            value = value - 2
    
    # Lets give weightage 3
    #return value * 3 
    return value  


# Evaluation function 5
# This returns value for how far the pieces are from promotional line
# Promotional line is opponents base line; if pawns reach there become kings
# If my pieces reached prmotional line score +7, for opponenet score -7
def evaluation5(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    # 0th element is for top row from top; 7th element is the bottom row in the board
    list = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]
    
    value = 0
    # Loop through all board positions
    for i in range(0, 8):
        for j in range(0, 4):
            piece = list[i][j]
            xy = gamePlay.serialToGrid(piece)
            x = xy[0]
            y = xy[1]
                
            if board[x][y].upper() == color.upper():
                if color.upper() == 'R':
                    # When R pieces reach bottom base line get score 7
                    value = value + i
                elif color.upper() == 'W':
                    # When W pieces reach top base line get score 7
                    value = value + (7-i)
       
            elif board[x][y].upper() == opponentColor.upper():
                if opponentColor.upper() == 'R':
                    # When opponent's R pieces reach bottom base line get score -7
                    value = value - i
                elif opponentColor.upper() == 'W':
                    # When opponent's W pieces reach top base line get score -7
                    value = value - (7-i)

    # Lets give weightage 2
    #return value * 2
    return value 


# Evaluation function 6
# My Base line is important. These pieces obstructs opponents king making 
# This returns value corresponding to my baseline pieces in absolute term
def evaluation6(board, color):
    
    # If my color is R, baseline is 1,2,3,4, otherwise 29,30,31,32
    list1 = [1, 2, 3, 4]
    list2 = [29, 30, 31, 32]
    
    value = 0
    # When my color is R, base line is list1
    if color.upper() == 'R':
        for piece in list1:
            xy = gamePlay.serialToGrid(piece)
            x = xy[0]
            y = xy[1]
                
            if board[x][y].upper() == color.upper():
                value = value + 1
    # When my color is W, base line is list2
    else:
        for piece in list2:
            xy = gamePlay.serialToGrid(piece)
            x = xy[0]
            y = xy[1]
                
            if board[x][y].upper() == color.upper():
                value = value + 1

    # Lets give weightage 5
    #return value * 5
    return value 


# Evaluation function 7
# Isolated piece means weakness, pieces should move together
# It returns valuation in terms of how many pieces protected by neighbors
def evaluation7(board, color):
    
    opponentColor = gamePlay.getOpponentColor(color)
    list1 = [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27]  
    
    value = 0
    # Loop through all board positions
    for piece in list1:
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y].upper() == color.upper():
            if board[x-1][y-1].upper() == color.upper():
                value = value + 1
            elif board[x-1][y+1].upper() == color.upper():
                value = value + 1
            elif board[x+1][y-1].upper() == color.upper():
                value = value + 1
            elif board[x+1][y+1].upper() == color.upper():
                value = value + 1
            
        elif board[x][y].upper() == opponentColor.upper():
            if board[x-1][y-1].upper() == opponentColor.upper():
                value = value - 1
            elif board[x-1][y+1].upper() == opponentColor.upper():
                value = value - 1
            elif board[x+1][y-1].upper() == opponentColor.upper():
                value = value - 1
            elif board[x+1][y+1].upper() == opponentColor.upper():
                value = value - 1
    
    # Let us give weightage 10
    #return value * 10
    return value 


# Main MiniMax with Alpha-Beta Prunnning Algorithm Implementation
def alphaBeta(board, move, depth, alpha, beta, maximizingPlayer, color, opColor):
    if depth == 0:
        # Different evaluation values multiplied by weightage
        moveVal = evaluation1(board, color) * 10
        if gamePhase(board, color) == 3:
            kingVal = evaluation2(board, color) * 5
        else:
            kingVal = 0
        capVal = evaluation3(board, color) * 10
        posVal = evaluation4(board, color) * 1 
        promoVal = evaluation5(board, color) * 1 
        if gamePhase(board, color) != 0:
            baseVal = evaluation6(board, color) * 1 
        else:
            baseVal = 0
        flockVal = evaluation7(board, color) * 2 
        # print moveVal, kingVal, capVal, posVal, promoVal, baseVal, flockVal
        bestVal = moveVal + kingVal + capVal + posVal + promoVal + baseVal + flockVal
        return bestVal
    
    if (maximizingPlayer):
        bestVal = -float('inf')
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        moves = getAllPossibleMoves(newBoard, color)
        for move in moves:
            bestVal = max(bestVal, alphaBeta(newBoard, move, depth-1, alpha, beta, False, color, opColor))
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = float('inf')
        newBoard = deepcopy(board)
        gamePlay.doMove(newBoard,move)
        moves = getAllPossibleMoves(newBoard, opColor)
        for move in moves:
            bestVal = min(bestVal, alphaBeta(newBoard, move, depth-1, alpha, beta, True, color, opColor))
            beta = min(beta, bestVal)
            if  beta <= alpha:
                break
        return bestVal

    
# Trying to find the move where I have best possible score
def nextMove(board, color, time, movesRemaining):
    # I will have different depth level as per time remaining
    if time > 120: 
        depth = 8
    elif time > 60: 
        depth = 6
    elif time > 5: 
        depth = 4
    else:
        depth = 2
    #print "DBG", phase, depth, time
    #t1 = datetime.datetime.now()
    moves = getAllPossibleMoves(board, color)
    best = None
    opColor = gamePlay.getOpponentColor(color)
    # If only one move available no need for any computations
    if len(moves) == 1:
        bestMove = moves[0]
        return bestMove
    # Strategy1: If it is first move hardcoding the best move
    if isFirstMove(board, color):
        if color.upper() == 'R':
            bestMove = [11, 15]
        else:
            bestMove = [22, 18]
        return bestMove

    # Strategy2: Remove moves that lead to opponent captures my piece
    for move in moves:
        myBoard = deepcopy(board)
        gamePlay.doMove(myBoard,move)
        # Check if opponents capturing position gone
        if gamePlay.isCapturePossible(myBoard, opColor) == True:
            moves.remove(move)

    # Strategy3: Opponent captures one, but I capture double
    # Check if newBoard is giving Opponent a capture
    opMoves = getAllPossibleMoves(board, opColor)
    # At most of the capture, opMoves will have one element
    if gamePlay.isCapturePossible(board, opColor) == True:
        opMove = opMoves[0]
        opBoard = deepcopy(board)
        gamePlay.doMove(opBoard, opMove)
        myMoves = getAllPossibleMoves(opBoard, color)
        # Check if I can capture two pieces
        if len(myMoves) > 0:
            myMove = myMoves[0]
            # At double-capture, lenghth of the move will be >2
            if len(myMove) > 2:
                # Do nothing, let opponent capture
                pass
            else: 
                # Try to block the capture
                for move in moves:
                    myBoard = deepcopy(board)
                    gamePlay.doMove(myBoard,move)
                    opMoves = getAllPossibleMoves(myBoard, opColor)
                    #Check if opponents capturing position gone
                    if  not gamePlay.isCapturePossible(board, opColor):
                        bestMove = move
                        return bestMove

    # Now start the main MiniMax and alpha-beta here
    for move in moves:
        # Strategy4: If I can double-capture, thats best move, kind of greedy
        if len(move) > 2:
            bestMove = move
            return bestMove
        newBoard = deepcopy(board)
        alpha = -float('inf')
        beta = float('inf')
        # Calling with different depth depending on time remaining in the game
        alphaVal = alphaBeta(newBoard, move, depth, alpha, beta, True, color, opColor)
        if best == None or alphaVal > best:
            bestMove = move
            best = alphaVal

    #t2 = datetime.datetime.now()
    return bestMove

