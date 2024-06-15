import pygame
import math
import random
import os

os.makedirs("screenshots", exist_ok=True)

#####################################################################################


def drawHexagon(screen, fillColor, strokeColor, r, center, grid, x, y):
    # calculating the coordinate of each vertex from the center of the hexagon using sin and cos functions
    coord = [r * math.cos(toRad(30)), r * math.sin(toRad(30))]
    multipliers = [
        [1, 1],
        [1, -1],
        [0, -1 / math.sin(toRad(30))],
        [-1, -1],
        [-1, 1],
        [0, 1 / math.sin(toRad(30))],
    ]

    # create a list of all vertex coordinates
    vertices = []
    centers[x].append(center)

    for multiplier in multipliers:
        vertices.append(
            (center[0] + coord[0] * multiplier[0], center[1] + coord[1] * multiplier[1])
        )

    if grid[x][y] >= 6:
        pygame.draw.polygon(screen, fillColor, vertices)
        pygame.draw.polygon(screen, strokeColor, vertices, strokeWidth)


def drawGrid(screen, grid):
    for i in range(gridY):
        for j in range(gridX):
            if i % 2:
                drawHexagon(
                    screen,
                    white,
                    stroke,
                    radius,
                    [offsetX * j, offsetY * i],
                    grid,
                    i,
                    j,
                )
            else:
                drawHexagon(
                    screen,
                    white,
                    stroke,
                    radius,
                    [(offsetX * j) + offsetX / 2, offsetY * i],
                    grid,
                    i,
                    j,
                )


def pointInCircle(x, y, a, b, r):
    distance = math.sqrt((x - a) ** 2 + (y - b) ** 2)
    return distance < r


def getNeighbours(i, j):
    # Making a list of the indices of all neighbours of the hexagon
    # i is the row, j is column

    if i % 2:
        indices = [
            [i - 1, j - 1],
            [i - 1, j],
            [i, j - 1],
            [i, j + 1],
            [i + 1, j - 1],
            [i + 1, j],
        ]
    else:
        indices = [
            [i - 1, j + 1],
            [i - 1, j],
            [i, j - 1],
            [i, j + 1],
            [i + 1, j + 1],
            [i + 1, j],
        ]

    # Counting alive neighbours
    count = 0
    try:
        for index in indices:
            if grid[index[0]][index[1]] == 6:
                count += 1
    except:
        pass
    return count


def checkCells():
    for i in range(gridY):
        for j in range(gridX):
            neighbours = getNeighbours(i, j)
            # Death Conditions:
            #   If the cell has been resurrected, then it cannot die by the previous method
            #   Else, it can die by any method
            if grid[i][j] == 6:
                if neighbours < 2:
                    if ressurections[i][j] == 1:
                        if deaths[i][j] == 2:
                            grid[i][j] = 0
                            deaths[i][j] = 1
                            ressurections[i][j] = 0
                    else:
                        grid[i][j] = 0
                        deaths[i][j] = 1
                elif neighbours > 3:
                    if ressurections[i][j] == 1:
                        if deaths[i][j] == 1:
                            grid[i][j] = 0
                            deaths[i][j] = 2
                            ressurections[i][j] = 0
                    else:
                        grid[i][j] = 0
                        deaths[i][j] = 2
                else:
                    grid[i][j] = 6
            else:
                if neighbours == 3:
                    grid[i][j] = 6
                    deaths[i][j] = 0
                    ressurections[i][j] = 0


def toRad(deg):
    return math.pi / 180 * deg


#####################################################################################

pygame.init()

stroke = (64, 67, 133)
blue = (28, 21, 73)
white = (36, 36, 104)

width, height = 720, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Of Life - Quant Club IIT KGP")

# Making hexagon with center as origin for each, hence calculating using radius
radius = 8
strokeWidth = 1

offsetX = 2 * radius * math.cos(toRad(30))
offsetY = radius + radius * math.sin(toRad(30))

# Number of hexagons to draw basically, plus some value so screen is filled
gridX = int(height / offsetX) + 5
gridY = int(width / offsetY) + 5

grid = []

# Initialize entire matrix for storing deaths
deaths = [[0 for _ in range(gridX)] for _ in range(gridY)]
ressurections = [[0 for _ in range(gridX)] for _ in range(gridY)]

centers = []

ticks = 0
flag = 0

grid = [[0 for _ in range(gridX)] for _ in range(gridY)]

running = True
generate = False

while running:
    screen.fill(blue)

    centers = [[] for _ in range(gridY)]

    # Draw hexagon grid
    drawGrid(screen, grid)

    # Keep checking for any game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Starting simulation..")
                generate = not generate
        if pygame.mouse.get_pressed()[0]:
            clickPos = pygame.mouse.get_pos()
            for i in range(gridY):
                for j in range(gridX):
                    if pointInCircle(
                        clickPos[0],
                        clickPos[1],
                        centers[i][j][0],
                        centers[i][j][1],
                        radius,
                    ):
                        grid[i][j] = 6

    ticks += 1

    if generate:
        checkCells()

        for i in range(gridY):
            for j in range(gridX):
                if grid[i][j] < 6 and (deaths[i][j] == 1 or deaths[i][j] == 2):
                    grid[i][j] += 1

                    # Resurrection
                    # "Every DEAD cell resurrects after 6 generations irrespective of the number of live neighbors":
                    #    1) Store which cells are being resurrected
                    #    2) Store their last cause of death (1 = Underpopulation, 2 = Overpopulation)
                    #    3) Check their last death before killing them again

                    if grid[i][j] == 6:
                        ressurections[i][j] = 1

        if ticks % 4 == 0:
            i, j = random.randint(0, gridY - 1), random.randint(0, gridX - 1)
            while grid[i][j] == 6:
                i, j = random.randint(0, gridY - 1), random.randint(0, gridX - 1)
            grid[i][j] = 6
            ressurections[i][j] = 0

        pygame.image.save(screen, f"screenshots/ss-{ticks}.png")
    pygame.display.flip()
pygame.quit()
