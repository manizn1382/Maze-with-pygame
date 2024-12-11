import pygame

# Screen dimensions
WIDTH, HEIGHT = 550, 550  # Screen width and height
CELL_SIZE = 50  # Size of each grid cell

# Calculate the number of rows and columns
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# player_pos
player_x = 5
player_y = 1

# Load wall images
down_image = pygame.image.load("asset/down.png")
up_image = pygame.image.load("asset/up.png")
left_image = pygame.image.load("asset/left.png")
right_image = pygame.image.load("asset/right.png")
character_image = pygame.image.load("asset/character.png")
rightArrow_image = pygame.image.load("asset/right-arrow.png")
teleport_image = pygame.image.load("asset/teleport.png")

# Scale images to fit in a grid cell
down_image = pygame.transform.scale(down_image, (CELL_SIZE, CELL_SIZE))
up_image = pygame.transform.scale(up_image, (CELL_SIZE, CELL_SIZE))
left_image = pygame.transform.scale(left_image, (CELL_SIZE, CELL_SIZE))
right_image = pygame.transform.scale(right_image, (CELL_SIZE, CELL_SIZE))
character_image = pygame.transform.scale(character_image, (CELL_SIZE, CELL_SIZE))
rightArrow_image = pygame.transform.scale(rightArrow_image, (CELL_SIZE, CELL_SIZE))
teleport_image = pygame.transform.scale(teleport_image, (CELL_SIZE, CELL_SIZE))

rows, cols = 11, 11

# arrow_position
left_side_arrow = (5, 0)
right_side_arrow = (5, 10)
