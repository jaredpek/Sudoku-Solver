import pygame
import sys
from dokusan import generators
import numpy as np

RED = (200, 120, 120)
GREEN = (120, 200, 152)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

pygame.init()

WIDTH = 800
ROWS = 9
GAP = WIDTH / ROWS
gap = GAP + 0.12
WIN = pygame.display.set_mode((WIDTH, WIDTH + 120))
WIN.fill(WHITE)
pygame.display.set_caption("SUDOKU")

FPS = 1000
fpsclock = pygame.time.Clock()

numberfont = pygame.font.SysFont("Arial", 45)
instrfont = pygame.font.SysFont("Arial", 25)


def drawgrid(rows, width, gapp):
    for i in range(rows + 1):
        if i % 3 == 0 and i != 0:
            pygame.draw.line(WIN, BLACK, (0, i * gapp), (width, i * gapp), 3)
            pygame.draw.line(WIN, BLACK, (i * gapp, 0), (i * gapp, width), 3)
        else:
            pygame.draw.line(WIN, BLACK, (0, i * gapp), (width, i * gapp), 1)
            pygame.draw.line(WIN, BLACK, (i * gapp, 0), (i * gapp, width), 1)

    instrtext1 = "1. Left-click on a box and key in a number."
    INSTRUCTIONS1 = instrfont.render(instrtext1, True, BLACK)
    WIN.blit(INSTRUCTIONS1, (10, width + 5))

    instrtext2 = "2. Right-click on a box to clear it."
    INSTRUCTIONS2 = instrfont.render(instrtext2, True, BLACK)
    WIN.blit(INSTRUCTIONS2, (10, width + 32))

    instrtext3 = "3. Press 'SPACE' to solve the problem!"
    INSTRUCTIONS3 = instrfont.render(instrtext3, True, BLACK)
    WIN.blit(INSTRUCTIONS3, (10, width + 59))

    instrtext4 = "4. Press 'ENTER' to load the next problem."
    INSTRUCTIONS4 = instrfont.render(instrtext4, True, BLACK)
    WIN.blit(INSTRUCTIONS4, (10, width + 86))


def drawproblem(boa, rows, gapp):
    for i in range(rows):
        for j in range(rows):
            if boa[i][j] != 0:
                value = numberfont.render(str(boa[i][j]), True, BLACK)
                WIN.blit(value, (j * gapp + 33, i * gapp + 17))


def insertnumber(bo, roww, coll, gapp, number):
    if bo[roww][coll] == 0:
        if number == 0:
            pygame.draw.rect(WIN, WHITE, (coll * gapp, roww * gapp, gapp, gapp))
        else:
            pygame.draw.rect(WIN, WHITE, (coll * gapp, roww * gapp, gapp, gapp))
            value = numberfont.render(str(number), True, GREY)
            WIN.blit(value, (coll * gap + 33, roww * gap + 17))


def insertfinalnumber(bo, roww, coll, gapp, number):
    if bo[roww][coll] == 0:
        if number == 0:
            pygame.draw.rect(WIN, WHITE, (coll * gapp, roww * gapp, gapp, gapp))
            drawgrid(ROWS, WIDTH, gap)
        else:
            pygame.draw.rect(WIN, GREEN, (coll * gapp, roww * gapp, gapp, gapp))
            drawgrid(ROWS, WIDTH, gap)
            value = numberfont.render(str(number), True, BLACK)
            WIN.blit(value, (coll * gap + 33, roww * gap + 17))


def checkempty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j
    # NO EMPTY BOXES
    return None


def checkvalid(bo, num, pos):
    roww, coll = pos

    # CHECK HORIZONTAL
    for i in range(len(bo[0])):
        if bo[roww][i] == num and coll != i:

            return False
    # CHECK VERTICAL
    for j in range(len(bo)):
        if bo[j][coll] == num and roww != i:
            return False
    # CHECK BOX
    box_x = coll // 3
    box_y = roww // 3
    for k in range(box_y * 3, box_y * 3 + 3):
        for m in range(box_x * 3, box_x * 3 + 3):
            if bo[k][m] == num and (k, m) != pos:
                return False
    # NUMBER IS VALID
    return True


def solve(bo):
    find = checkempty(bo)
    if not find:
        return True
    else:
        roww, coll = find

    for num in range(1, 10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if checkvalid(bo, num, (roww, coll)):
            fpsclock.tick(FPS)
            insertfinalnumber(bo, roww, coll, gap, num)
            pygame.display.flip()
            bo[roww][coll] = num
            if solve(bo):
                return True

        bo[roww][coll] = 0
        pygame.draw.rect(WIN, RED, (coll * gap, roww * gap, gap, gap))
        drawgrid(ROWS, WIDTH, gap)
        pygame.display.flip()


def generate(gapp):
    arr = np.array(list(str(generators.random_sudoku(avg_rank=700))))
    strbo = arr.reshape(9, 9)
    intbo = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 8, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for roww in range(len(strbo)):
        for coll in range(len(strbo[roww])):
            pygame.draw.rect(WIN, WHITE, (coll * gapp, roww * gapp, gapp, gapp))
            intbo[roww][coll] = int(strbo[roww][coll])

    return intbo


run = True

board = generate(gap)

row, col = checkempty(board)

while run:
    fpsclock.tick(FPS)
    drawproblem(board, ROWS, gap)
    drawgrid(ROWS, WIDTH, gap)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # SELECT BOX
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                col = int(x // GAP)
                row = int(y // GAP)

            # CLEAR BOX CONTENTS
            if event.button == 3:
                x, y = pygame.mouse.get_pos()
                col = int(x // GAP)
                row = int(y // GAP)
                insertnumber(board, row, col, gap, 0)

        if event.type == pygame.KEYDOWN:
            # INSERT NUMBER INTO BOX
            if event.key == pygame.K_1:
                insertnumber(board, row, col, gap, 1)
            if event.key == pygame.K_2:
                insertnumber(board, row, col, gap, 2)
            if event.key == pygame.K_3:
                insertnumber(board, row, col, gap, 3)
            if event.key == pygame.K_4:
                insertnumber(board, row, col, gap, 4)
            if event.key == pygame.K_5:
                insertnumber(board, row, col, gap, 5)
            if event.key == pygame.K_6:
                insertnumber(board, row, col, gap, 6)
            if event.key == pygame.K_7:
                insertnumber(board, row, col, gap, 7)
            if event.key == pygame.K_8:
                insertnumber(board, row, col, gap, 8)
            if event.key == pygame.K_9:
                insertnumber(board, row, col, gap, 9)

            # SOLVE PROBLEM
            if event.key == pygame.K_SPACE:
                solve(board)

            # GENERATE NEW PROBLEM
            if event.key == pygame.K_RETURN:
                board = generate(gap)
                drawproblem(board, ROWS, gap)
                drawgrid(ROWS, WIDTH, gap)

    pygame.display.update()
