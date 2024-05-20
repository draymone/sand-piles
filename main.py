import time
import pygame
import copy
from pygame.font import Font

# <editor-fold desc="CONFIGURATION">
# The size (heigth and width) of the grid
GRID_SIZE = 5

# The size of a cell (in pixels)
CELL_SIZE = 20

# If true, the grid is import from the grid.txt file, else it's and empty grid
IMPORT_FROM_GRID = True

# The number of ticks that elapse per second
TICKRATE = 1
# </editor-fold>

COLORS = [
    (0, 0, 0),        # 0 grain
    (70, 0, 0),       # 1 grain
    (70, 70, 0),      # 2 grains
    (70, 70, 70),     # 3 grains
    (100, 100, 100),  # 4 grains or more
]

grid: list[list[int]] = []
font: Font | None = None


def import_from_grid():
    global GRID_SIZE
    with open("grid.txt", "r") as file:
        while line := file.readline():
            grid_line = []
            for e in line.rstrip().split(" "):
                grid_line.append(int(e))
            grid.append(grid_line)
        GRID_SIZE = len(grid)


def tick():
    new_grid: list[list[int]] = copy.deepcopy(grid)

    # Itterate through cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # If there are more than 4 grains
            if grid[i][j] >= 4:
                # 4 of them fall ...
                new_grid[i][j] -= 4
                # Into the neighbor cells
                for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x = i + offset[0]
                    y = j + offset[1]
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        new_grid[x][y] += 1

    grid[:] = new_grid[:]


def display_grid(screen):
    # For each cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]

            # Draw it
            color = COLORS[value] if value < len(COLORS) else COLORS[-1]
            pygame.draw.rect(screen,
                             color,
                             (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

            # Draw the label
            label_color = (255-color[0], 255-color[1], 255-color[2])
            label = font.render(str(value), 1, label_color)
            screen.blit(label, (i * CELL_SIZE, j * CELL_SIZE))

    pygame.display.update()


def main():
    if IMPORT_FROM_GRID:
        import_from_grid()
    else:
        global grid
        grid = [[0] * GRID_SIZE] * GRID_SIZE

    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE))
    screen.fill((30, 30, 30))
    global font
    font = pygame.font.SysFont("monospace", 15)

    display_grid(screen)
    pygame.display.flip()

    while True:
        time.sleep(1 / TICKRATE)
        tick()
        display_grid(screen)


if __name__ == '__main__':
    main()
