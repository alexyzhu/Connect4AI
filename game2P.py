import numpy as np


RED_PLAYER = 1
YELLOW_PLAYER = -1
GAME_BOARD = [[0 for _ in range(7)] for _ in range(6)]


def canMakeMove(column: int) -> bool:
    return GAME_BOARD[5][column] == 0


def moveInColumn(column: int, player: int) -> bool:
    global GAME_BOARD
    if canMakeMove(column):
        for r, row in enumerate(GAME_BOARD):
            if row[column] == 0:
                GAME_BOARD[r][column] = player
                return True
    return False


def isGameOver() -> int:
    global GAME_BOARD

    for row in GAME_BOARD:
        isOver = fourInARow(row)
        if isOver:
            return isOver

    for column in range(len(GAME_BOARD[0])):
        column = [GAME_BOARD[x][column] for x in range(len(GAME_BOARD))]
        isOver = fourInARow(column)
        if isOver:
            return isOver

    boardNumpy = np.array(GAME_BOARD)
    for diag in range(-2, 4):  # all diagonals that can have 4 in a row
        isOver = fourInARow(list(boardNumpy.diagonal(diag)))
        if isOver:
            return isOver
        # search anti-diagonal
        isOver = fourInARow(np.fliplr(boardNumpy).diagonal(diag))
        if isOver:
            return isOver

    return 0


def fourInARow(array):
    currCount = 0
    currPlayer = array[0]
    for i in array:
        if i == currPlayer:
            currCount += 1
        else:
            if currCount >= 4 and currPlayer != 0:
                return currPlayer
            currCount = 1
            currPlayer = i
    if currCount >= 4 and currPlayer != 0:
        return currPlayer
    return 0


def printBoard():
    for row in reversed(GAME_BOARD):
        print('\t', end='')
        for item in row:
            print('\t' + ('R' if item == 1 else str(item) if item == 0 else 'Y'), end='')
        print()

    print('-'*35, end='')
    print('\ncol', end='')

    print("\t", end='')
    for column in range(7):
        print('\t' + str(column + 1), end="")
    print("\n")


def checkGameOver() -> bool:
    isOver = isGameOver()
    if isOver == 1:
        print("Red Win")
        return True
    elif isOver == -1:
        print("Yellow Win")
        return True
    return False


def runGame():
    while(True):
        printBoard()
        if checkGameOver():
           break

        # Red Move
        print("Red Move\n")
        while(True):
            column = int(input("Input the column you want to move in: "))
            if not canMakeMove(column-1):
                print("Unable to move in column, please select another column")
                continue
            moveInColumn(column-1, RED_PLAYER)
            break

        printBoard()
        if checkGameOver():
            break

        # Yellow Move
        print("Yellow Move\n")
        while(True):
            column = int(input("Input the column you want to move in: "))
            if not canMakeMove(column-1):
                print("Unable to move in column, please select another column")
                continue
            moveInColumn(column-1, YELLOW_PLAYER)
            break


def main():
    runGame()


if __name__ == '__main__':
    main()
