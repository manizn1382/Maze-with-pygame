

import pygame
import sys

import self
from PIL import Image
from Cell_status import Cell_status

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 550, 550  # Screen width and height
CELL_SIZE = 50  # Size of each grid cell

# Calculate the number of rows and columns
COLUMNS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# player_pos
player_x = 5
player_y = 1


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.player_x = x
        self.player_y = y

    def __getitem__(self):
        return self.player_x, self.player_y

    def move(self, key, maze_status):
        cs = maze_status[self.player_x][self.player_y]

        if key[pygame.K_UP]:
            up_cs = maze_status[self.player_x - 1][self.player_y] if self.player_x - 1 >= 0 else ''
            if up_cs.down == 1 or cs.up == 1:
                if up_cs.downPuzzle == 1 or cs.upPuzzle == 1:
                    pass  # Update logic for puzzles here
                else:
                    pass
            else:
                self.player_x = max(0, self.player_x - 1)

        if key[pygame.K_DOWN]:
            down_cs = maze_status[self.player_x + 1][self.player_y] if self.player_x + 1 < len(maze_status) else ''
            if down_cs.up == 1 or cs.down == 1:
                if down_cs.upPuzzle or cs.downPuzzle:
                    pass  # Update logic for puzzles here
            else:
                self.player_x = min(len(maze_status) - 1, self.player_x + 1)

        if key[pygame.K_LEFT]:
            left_cs = maze_status[self.player_x][self.player_y - 1] if self.player_y - 1 >= 0 else ''
            if left_cs.right == 1 or cs.left == 1:
                if left_cs.rightPuzzle or cs.leftPuzzle:
                    pass  # Update logic for puzzles here
            else:
                self.player_y = max(0, self.player_y - 1)

        if key[pygame.K_RIGHT]:
            right_cs = maze_status[self.player_x][self.player_y + 1] if self.player_y + 1 < len(
                maze_status[0]) else ''
            if right_cs.left == 1 or cs.right == 1:
                if right_cs.leftPuzzle or cs.rightPuzzle:
                    pass  # Update logic for puzzles here
            else:
                self.player_y = min(len(maze_status[0]) - 1, self.player_y + 1)


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZE")

# Load wall images
down_image = pygame.image.load("asset/down.png")
up_image = pygame.image.load("asset/up.png")
left_image = pygame.image.load("asset/left.png")
right_image = pygame.image.load("asset/right.png")
character_image = pygame.image.load("asset/character.png")
rightArrow_image = pygame.image.load("asset/right-arrow.png")

# Scale images to fit in a grid cell
down_image = pygame.transform.scale(down_image, (CELL_SIZE, CELL_SIZE))
up_image = pygame.transform.scale(up_image, (CELL_SIZE, CELL_SIZE))
left_image = pygame.transform.scale(left_image, (CELL_SIZE, CELL_SIZE))
right_image = pygame.transform.scale(right_image, (CELL_SIZE, CELL_SIZE))
character_image = pygame.transform.scale(character_image, (CELL_SIZE, CELL_SIZE))
rightArrow_image = pygame.transform.scale(rightArrow_image, (CELL_SIZE, CELL_SIZE))

rows, cols = 11, 11

# right, left, up, down, teleport, portal, mist(1 for exist & 0 for not-exist)
cells_info = [
    ["0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000",
     "0000000"],
    ["0000000", "0110000", "0011000", "1011000", "0011010", "0111000", "1010000", "0000000", "0111000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0000000", "0000000", "0000000", "1101000", "0000000", "0000000", "1000000",
     "0000000"],
    ["0000000", "0101000", "0101000", "0110000", "1011000", "0000000", "1001000", "0001000", "0110000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0100000", "0101000", "0001000", "0100000", "0001000", "0001000", "1001000",
     "0000000"],
    ["0000000", "0000000", "0000000", "0100000", "0100000", "0101000", "0100000", "0000000", "0000000", "0000000",
     "0000000"],
    ["0000000", "0100000", "0100000", "0100000", "0101000", "0101000", "0001000", "1010010", "1001000", "1010000",
     "0000000"],
    ["0000000", "0100000", "0101000", "0101000", "0001000", "0000000", "0100000", "1001000", "0000000", "1000000",
     "0000000"],
    ["0000000", "0100000", "0101000", "0001000", "0001000", "0001000", "0001000", "1001000", "0000000", "1000000",
     "0000000"],
    ["0000000", "0101000", "0000000", "0101000", "0001000", "0001000", "0001000", "0001000", "0001000", "1001000",
     "0000000"],
    ["0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000",
     "0000000"],
]

maze = [[0 for _ in range(cols)] for _ in range(rows)]


# Load GIF frames
def load_gif_frames(gif_path, cell_size):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")  # Ensure RGBA mode
            data = frame.getdata()  # Get pixel data

            # Replace white background with transparency using a lambda function
            new_data = list(map(lambda item: (0, 0, 0, 0) if item[:3] == (255, 255, 255) else item, data))

            frame.putdata(new_data)  # Update frame data

            # Convert to Pygame surface
            frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frame_surface = pygame.transform.scale(frame_surface, (cell_size, cell_size))
            frames.append(frame_surface)

            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # End of GIF
    return frames


# Load GIF frames for animation
portalGif_frames = load_gif_frames("asset/portal.gif", CELL_SIZE)
portalGif_index = 0  # Current frame index


def draw_grid():
    """Draws the grid on the screen."""
    for x in range(0, WIDTH, CELL_SIZE):  # Vertical lines
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):  # Horizontal lines
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_image_in_cell(im, row, column):
    """Places the image in a specific grid cell."""
    x = column * CELL_SIZE
    y = row * CELL_SIZE
    screen.blit(im, (x, y))


def draw_maze(grid, frame):
    """Draws the static maze grid."""
    for i in range(rows):
        for j in range(cols):
            cs = Cell_status(grid[i][j])
            if cs.right == 1:
                draw_image_in_cell(right_image, i, j)
            if cs.left == 1:
                draw_image_in_cell(left_image, i, j)
            if cs.up == 1:
                draw_image_in_cell(up_image, i, j)
            if cs.down == 1:
                draw_image_in_cell(down_image, i, j)
            if cs.portal == 1:
                draw_image_in_cell(portalGif_frames[frame], i, j)
            maze[i][j] = cs


player = Character(player_x, player_y)

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    player.move(keys, maze)

    screen.fill(BLACK)

    draw_grid()

    portalGif_index = (portalGif_index + 1) % len(portalGif_frames)

    draw_maze(cells_info, portalGif_index)

    draw_image_in_cell(rightArrow_image, 5, 0)
    draw_image_in_cell(rightArrow_image, 5, 10)

    draw_image_in_cell(character_image, player.__getitem__()[0], player.__getitem__()[1])

    # Update the display
    pygame.display.flip()

    # Control the frame rate for the GIF animation (e.g., 10 FPS)
    clock.tick(10)
