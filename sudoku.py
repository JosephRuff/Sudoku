import pygame
import random
import time

interval = 0
animate = False

print("Do you wish to animate the progress? (y/n)")
while (True):
    animateInput = input()
    if (animateInput == "y"):
        animate = True
        break
    elif (animateInput == "n"):
        animate = False
        break
if (animate):
    print("What interval do you want to set? Recommended 0 < n < 1")
    while (True):
        intervalInput = input()
        try:
            interval = float(intervalInput)
            if (interval >= 0):
                break
        except ValueError:
            pass

gameDisplay = pygame.display.set_mode((462,462))

pygame.display.set_caption('Sudoku Solver')

black = (0,0,0)
blue = (46, 92, 184)
white = (255,255,255)
red = (255,120,120)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 35)


def setBackground():
    pygame.draw.rect(gameDisplay, white, (0,0,462,462))

    #vertical bars
    pygame.draw.rect(gameDisplay, black, (0,0,1,462))
    pygame.draw.rect(gameDisplay, black, (51,0,1,462))
    pygame.draw.rect(gameDisplay, black, (102,0,1,462))
    pygame.draw.rect(gameDisplay, black, (153,0,2,462))
    pygame.draw.rect(gameDisplay, black, (205,0,1,462))
    pygame.draw.rect(gameDisplay, black, (256,0,1,462))
    pygame.draw.rect(gameDisplay, black, (307,0,2,462))
    pygame.draw.rect(gameDisplay, black, (359,0,1,462))
    pygame.draw.rect(gameDisplay, black, (410,0,1,462))
    pygame.draw.rect(gameDisplay, black, (461,0,1,462))

    #horizontal bars
    pygame.draw.rect(gameDisplay, black, (0,0,462,1))
    pygame.draw.rect(gameDisplay, black, (0,51,462,1))
    pygame.draw.rect(gameDisplay, black, (0,102,462,1))
    pygame.draw.rect(gameDisplay, black, (0,153,462,2))
    pygame.draw.rect(gameDisplay, black, (0,205,462,1))
    pygame.draw.rect(gameDisplay, black, (0,256,462,1))
    pygame.draw.rect(gameDisplay, black, (0,307,462,2))
    pygame.draw.rect(gameDisplay, black, (0,359,462,1))
    pygame.draw.rect(gameDisplay, black, (0,410,462,1))
    pygame.draw.rect(gameDisplay, black, (0,461,462,1))


def printLetter(x, y, value, colour):
    xOffset = 1
    yOffset = 1
    xOffset = xOffset + (50 * x) + x
    yOffset = yOffset + (50 * y) + y

    #adjust for thicker lines
    if (x > 2):
        xOffset = xOffset + 1 
    if (x > 5):
        xOffset = xOffset + 1 
    if (y > 2):
        yOffset = yOffset + 1 
    if (y > 5):
        yOffset = yOffset + 1
        
    #center printed numbers
    if (value == 1):
        xOffset = xOffset + 16 
    elif (value == 2):
        xOffset = xOffset + 14 
    elif (value == 3):
        xOffset = xOffset + 14 
    elif (value == 4):
        xOffset = xOffset + 15 
    elif (value == 5):
        xOffset = xOffset + 15
    elif (value == 6):
        xOffset = xOffset + 15
    elif (value == 7):
        xOffset = xOffset + 15 
    elif (value == 8):
        xOffset = xOffset + 15 
    else:
        xOffset = xOffset + 15

    if ((value > 0) and (value < 10)):
        textsurface = myfont.render(str(value), False, colour)
        gameDisplay.blit(textsurface,(xOffset,yOffset))


def checkValid(x, y, board):
    valid = True
    #check X
    xList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    xList.remove(x)
    for i in xList:
        if (board[x][y] == board[i][y]):
            valid = False
            #print("x false")
    #check Y
    yList = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    yList.remove(y)
    for i in yList:
        if (board[x][y] == board[x][i]):
            valid = False
            #print("y false")
    #check section
    xSection = x // 3
    xList = [(xSection * 3), (xSection * 3) + 1, (xSection * 3) + 2]
    xList.remove(x)
    ySection = y // 3
    yList = [(ySection * 3), (ySection * 3) + 1, (ySection * 3) + 2]
    yList.remove(y)
    for i in range (0, len(xList)):
        for j in range (0, len(yList)):
            xCheck = xList[i]
            yCheck = yList[j]
            if (board[x][y] == board[xCheck][yCheck]):
                if (xCheck != x):
                    if (yCheck != y):
                        valid = False
                        #print("section false")
    return (valid)


def displayBoard(board, x, y):
    setBackground()
    if (x >= 0):
        if (y >= 0):
            xOffset = 1
            yOffset = 1
            xOffset = xOffset + (50 * x) + x
            yOffset = yOffset + (50 * y) + y

            #adjust for thicker lines
            if (x > 2):
                xOffset = xOffset + 1 
            if (x > 5):
                xOffset = xOffset + 1 
            if (y > 2):
                yOffset = yOffset + 1 
            if (y > 5):
                yOffset = yOffset + 1
            
            pygame.draw.rect(gameDisplay, red, (xOffset,yOffset,50,50))
    
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (lockBoard[i][j]):
                colour = black
            else:
                colour = blue
            printLetter(i, j, board[i][j], colour)
    
    if (x >= 0):
        if (y >= 0):
            time.sleep(interval)
    pygame.display.update()
    pygame.event.pump()


def solveBoard(board):
    x = 0
    y = 0
    incrementCount = 0
    print("Working...")
    while(True):
        #if at end it is complete
        if (y > 8):
            print("Done.")
            print(incrementCount)
            return(board)
        #if at start it is failed
        elif (y < 0):
            print("Failed!")
            print(incrementCount)
            return(board)
        #otherwise solve
        else:
            #if locked move on. 
            if (lockBoard[x][y]):
                x = x + 1
                if (x > 8):
                    x = 0
                    y = y + 1
            #if not locked
            else:
                #increment until valid
                while(True):
                    board[x][y] = board[x][y] + 1
                    incrementCount = incrementCount + 1
                    if (animate):
                        displayBoard(board, x, y)
                    #if number exceeds 9 reset and backtrack
                    if (board[x][y] > 9):
                        board[x][y] = 0
                        #backtrack until at last unlocked cell
                        while(True):
                            x = x - 1
                            if (x < 0):
                                x = 8
                                y = y - 1
                            if (y < 0):
                                print("Failed")
                                print(incrementCount)
                                return(board)
                            elif(lockBoard[x][y]):
                                pass
                            else:
                                break
                    #if valid move on and stop incrementing
                    elif (checkValid(x, y, board)):
                        x = x + 1
                        if (x > 8):
                            x = 0
                            y = y + 1
                        break
                        

lockBoard = []
for i in range(0, 9):
    lockBoard.append([False]*9)

gameBoard = []
for i in range(0, 9):
    gameBoard.append([0]*9)

file = open("board.txt", "r")
Lines = file.readlines()
for y in range(0, 9):
    row = Lines[y]
    for x in range (0, 9):
        value = int(row[x])
        gameBoard[x][y] = value
        if (value > 0):
            lockBoard[x][y] = True

displayBoard(gameBoard, -1, -1)
gameBoard = solveBoard(gameBoard)
displayBoard(gameBoard, -1, -1)

print("Enter anything to continue: ")
input()
