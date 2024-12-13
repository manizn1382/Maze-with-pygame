import pygame

# Screen dimensions
WIDTH, HEIGHT = 550, 550  # Screen width and height
CELL_SIZE = 50  # Size of each grid cell

# Calculate the number of rows and columns
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# matchstick_dim
stick_x = 10
stick_y = 80

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# player_pos
player_x = 5
player_y = 1

# player score
player_score = 2000


# cost of each cell in yellow,red and black
black_cost = 10
yellow_cost = 20
red_cost = 30


# Load wall images
down_image = pygame.image.load("asset/down.png")
up_image = pygame.image.load("asset/up.png")
left_image = pygame.image.load("asset/left.png")
right_image = pygame.image.load("asset/right.png")
character_image = pygame.image.load("asset/character.png")
rightArrow_image = pygame.image.load("asset/right-arrow.png")
teleport_image = pygame.image.load("asset/teleport.png")
red_cell_image = pygame.image.load("asset/red_cell.png")
yellow_cell_image = pygame.image.load("asset/yellow_cell.png")
down_puzzle_image = pygame.image.load("asset/down_puzzle.png")
up_puzzle_image = pygame.image.load("asset/up_puzzle.png")
left_puzzle_image = pygame.image.load("asset/left_puzzle.png")
right_puzzle_image = pygame.image.load("asset/right_puzzle.png")
mist_image = pygame.image.load("asset/mist.png")
down_stick_image = pygame.image.load("asset/down_stick.png")
up_stick_image = pygame.image.load("asset/up_stick.png")
left_stick_image = pygame.image.load("asset/left_stick.png")
right_stick_image = pygame.image.load("asset/right_stick.png")



# Scale images to fit in a grid cell
down_image = pygame.transform.scale(down_image, (CELL_SIZE, CELL_SIZE))
up_image = pygame.transform.scale(up_image, (CELL_SIZE, CELL_SIZE))
left_image = pygame.transform.scale(left_image, (CELL_SIZE, CELL_SIZE))
right_image = pygame.transform.scale(right_image, (CELL_SIZE, CELL_SIZE))
character_image = pygame.transform.scale(character_image, (CELL_SIZE, CELL_SIZE))
rightArrow_image = pygame.transform.scale(rightArrow_image, (CELL_SIZE, CELL_SIZE))
teleport_image = pygame.transform.scale(teleport_image, (CELL_SIZE, CELL_SIZE))
red_cell_image = pygame.transform.scale(red_cell_image, (CELL_SIZE, CELL_SIZE))
yellow_cell_image = pygame.transform.scale(yellow_cell_image, (CELL_SIZE, CELL_SIZE))
down_puzzle_image = pygame.transform.scale(down_puzzle_image, (CELL_SIZE, CELL_SIZE))
up_puzzle_image = pygame.transform.scale(up_puzzle_image, (CELL_SIZE, CELL_SIZE))
left_puzzle_image = pygame.transform.scale(left_puzzle_image, (CELL_SIZE, CELL_SIZE))
right_puzzle_image = pygame.transform.scale(right_puzzle_image, (CELL_SIZE, CELL_SIZE))
mist_image = pygame.transform.scale(mist_image, (CELL_SIZE, CELL_SIZE))

right_stick_image = pygame.transform.scale(right_stick_image, (stick_y, stick_x))
up_stick_image = pygame.transform.scale(up_stick_image, (stick_x, stick_y))
down_stick_image = pygame.transform.scale(down_stick_image, (stick_x, stick_y))
left_stick_image = pygame.transform.scale(left_stick_image, (stick_y, stick_x))


rows, cols = 11, 11

# arrow_position
left_side_arrow = (5, 0)
right_side_arrow = (5, 10)

# win_position
win_pos = (5, 10)


# right, left, up, down, teleport, portal, mist(1 for exist & 0 for not-exist)
maze = [
    ["0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000100", "0000000", "0000000",
     "0000000"],
    ["0000000", "0110000", "0011000", "1011000", "0011010", "0111000", "1010000", "0000000", "0111000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0000000", "0000000", "0000000", "1101000", "0000000", "0000000", "1000000",
     "0000000"],
    ["0000000", "0101000", "0101000", "0110000", "1011000", "0000000", "1001000", "0001000", "0110000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0100000", "0101000", "0001000", "0100000", "0001000", "0001000", "1001000",
     "0000000"],
    ["0000000", "0000000", "0000000", "0100000", "0100000", "0101000", "0100001", "0000001", "0000000", "0000000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0100000", "0101000", "0101000", "0001001", "1010011", "1001000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0101000", "0101000", "0001000", "0000000", "0100001", "1001001", "0000000", "1000000",
     "0000000"],
    ["0000000", "0100000", "0101000", "0001000", "0001000", "0001000", "0001001", "1001001", "0000000", "1000000",
     "0000000"],
    ["0000000", "0101000", "0000000", "0101000", "0001000", "0001000", "0001000", "0001000", "0001000", "1001000",
     "0000000"],
    ["0000000", "0000000", "0000100", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000",
     "0000000"],
]

puzzle_position = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
