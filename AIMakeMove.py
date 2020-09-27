import numpy as np
import time

# Global Variables
TIME_PER_MOVE = -1
TIME_REMAINING = -1
TMAX = 600
gBoard = [[]]


def MakeMove(board: [[]], PlayerIsRed: bool) -> int:
    global TIME_PER_MOVE, TMAX, TIME_REMAINING, gBoard

    gBoard = board

    if TIME_PER_MOVE == -1:
        boardSize = len(board) * len(board[0])
        totalMoves = boardSize/2 + 1
        TIME_PER_MOVE = (TMAX/totalMoves)*.95
        TIME_REMAINING = TMAX

    if TIME_PER_MOVE <= TMAX * 0.05 or TIME_REMAINING <= 3:
        return chooseFirstMove(board)
    startTime = time.time()
    cutoffTime = startTime + TIME_PER_MOVE  # calculate when to stop

    depth = 0
    bestScore = float("-inf")
    bestCol = chooseFirstMove(board)
    result = bestCol

    while time.time() < cutoffTime:
        for column in range(len(board[0])):
            # column = [board[x][col] for x in range(len(board))]
            if canMakeMove(column):
                simMove(column, PlayerIsRed)
                score = abSearch(float("-inf"), float("inf"), depth, PlayerIsRed, cutoffTime, PlayerIsRed)
                undoMove(column)
                if score > bestScore:
                    bestScore = score
                    bestCol = column
        depth += 1
        if time.time() < cutoffTime:
            result = bestCol        # only save result if depth was completely searched
    TIME_REMAINING -= time.time() - startTime
    return result


def chooseFirstMove(board: [[]]) -> int:
    for col in range(len(board[0])):
        if board[5][col] == 0:
            return col


def boardEval(forRedPlayer: bool) -> int:
    xInARowWeights = {2: 50, 3: 250, 4: 1000}
    return scoreXInARowOccurrences(xInARowWeights, forRedPlayer) - \
        scoreXInARowOccurrences(xInARowWeights, not forRedPlayer)


def abSearch(alpha, beta, depth: int, isRedPlayer: bool, timeCutoff, isRedTurn: bool) -> int:
    global gBoard
    if time.time() >= timeCutoff:
        return 0
    elif depth == 0:
        return boardEval(isRedPlayer)

    if isRedPlayer == isRedTurn:
        currMax = float("-inf")
        for column in range(len(gBoard[0])):
            if not canMakeMove(column):
                continue
            simMove(column, isRedPlayer)
            currMax = max(currMax, abSearch(alpha, beta, depth-1, isRedPlayer, timeCutoff, not isRedTurn))
            undoMove(column)
            alpha = max(alpha, currMax)
            if alpha >= beta:
                break
        return currMax
    else:
        currMin = float("inf")
        for column in range(len(gBoard[0])):
            if not canMakeMove(column):
                continue
            simMove(column, isRedPlayer)
            currMin = min(currMin, abSearch(alpha, beta, depth-1, isRedPlayer, timeCutoff, not isRedTurn))
            undoMove(column)
            beta = min(beta, currMin)
            if alpha >= beta:
                break
        return currMin


def simMove(column: int, playerIsRed: bool) -> None:
    global gBoard
    tile = -1 if playerIsRed else 1
    for r, row in enumerate(gBoard):
        if row[column] == 0:
            gBoard[r][column] = tile


def undoMove(column: int) -> None:
    global gBoard
    for r, row in enumerate(gBoard[::-1]):    # iterate from top
        if row[column] != 0:
            gBoard[len(gBoard)-1-r][column] = 0
            return


def canMakeMove(column: int) -> bool:
    return gBoard[5][column] == 0


def scoreXInARowOccurrences(xInARowWeights: dict, isRed: bool) -> int:
    global gBoard
    occurrences = [0, 0, 0]
    target = 1 if isRed else -1

    for row in gBoard:
        occurrences = addOcc(occurrences, consecutiveTiles(row, target))

    for column in range(len(gBoard[0])):
        column = [gBoard[x][column] for x in range(len(gBoard))]
        occurrences = addOcc(occurrences, consecutiveTiles(column, target))

    boardNumpy = np.array(gBoard)
    for diag in range(len(gBoard)+len(gBoard[0])-1):
        diag = (len(gBoard)+len(gBoard[0]))//2 - diag    # get diagonal offset that numpy uses
        occurrences = addOcc(occurrences, consecutiveTiles(list(boardNumpy.diagonal(diag)), target))
        # search anti-diagonal
        occurrences = addOcc(occurrences, consecutiveTiles(list(np.fliplr(boardNumpy).diagonal(diag)), target))

    scoreResult = 0
    for i in range(3):
        scoreResult += xInARowWeights[i+2] * occurrences[i]

    return scoreResult


def addOcc(array1: [], array2: []) -> []:
    return [sum(occ) for occ in zip(array1, array2)]


def consecutiveTiles(array: [], target: int) -> []:
    result = [0, 0, 0]
    currCount = 0
    for i in array:
        if i == target:
            currCount += 1
        else:
            if currCount > 1:
                result[min(currCount, 4) - 1] += 1
            currCount = 0
    return result
