import sys

import pygame
from pygame import mixer
from PIL import Image

from Cell_status import Cell_status
from config import left_side_arrow, right_side_arrow, player_score, yellow_cell_image, red_cell_image
from config import GRAY, BLACK, character_image, player_x, player_y, teleport_image, CELL_SIZE
from config import rows, cols, WIDTH, HEIGHT, down_image, right_image, rightArrow_image, left_image, up_image

# Initialize Pygame
pygame.init()


# mixer.init()
# mixer.music.load("Nu - Man O To.mp3")
# mixer.music.play(-1)


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.player_x = x
        self.player_y = y
        self.score = player_score

    def __getitem__(self):
        return self.player_x, self.player_y

    def move(self, key, maze_status):

        cs = maze_status[self.player_x][self.player_y]

        if key[pygame.K_UP]:
            if self.player_x == 1 and self.player_y == 7:  # upside_teleport_position
                # place player in downside teleport
                self.player_x = 9
                self.player_y = 2
            else:
                up_cs = maze_status[self.player_x - 1][self.player_y] if self.player_x - 1 >= 0 else None
                if up_cs and (up_cs.down == 1 or cs.up == 1):
                    if up_cs.downPuzzle == 1 or cs.upPuzzle == 1:
                        pass  # Update logic for puzzles here
                    else:
                        pass
                elif up_cs and up_cs.track < 3:
                    self.player_x -= 1
                    up_cs.track += 1

        if key[pygame.K_DOWN]:
            if self.player_x == 9 and self.player_y == 2:  # downside_teleport_position
                # place player in upside teleport
                self.player_x = 1
                self.player_y = 7
            else:
                down_cs = maze_status[self.player_x + 1][self.player_y] if self.player_x + 1 < len(
                    maze_status) else None
                if down_cs and (down_cs.up == 1 or cs.down == 1):
                    if down_cs.upPuzzle or cs.downPuzzle:
                        pass  # Update logic for puzzles here
                elif down_cs and down_cs.track < 3:
                    self.player_x += 1
                    down_cs.track += 1

        if key[pygame.K_LEFT]:
            if self.player_x == left_side_arrow[0] and self.player_y == left_side_arrow[1] + 1:  # bound-check
                pass
            else:
                left_cs = maze_status[self.player_x][self.player_y - 1] if self.player_y - 1 >= 0 else None
                if left_cs and (left_cs.right == 1 or cs.left == 1):
                    if left_cs.rightPuzzle or cs.leftPuzzle:
                        pass  # Update logic for puzzles here
                elif left_cs and left_cs.track < 3:
                    self.player_y -= 1
                    left_cs.track += 1

        if key[pygame.K_RIGHT]:
            right_cs = maze_status[self.player_x][self.player_y + 1] if self.player_y + 1 < len(
                maze_status[0]) else None
            if right_cs and (right_cs.left == 1 or cs.right == 1):
                if right_cs.leftPuzzle or cs.rightPuzzle:
                    pass  # Update logic for puzzles here
            elif right_cs and right_cs.track < 3:
                self.player_y += 1
                right_cs.track += 1


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZE")

# right, left, up, down, teleport, portal, mist(1 for exist & 0 for not-exist)
cells_info = [
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
    ["0000000", "0000000", "0000100", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000", "0000000",
     "0000000"],
]

# maze = [[0 for _ in range(cols)] for _ in range(rows)]
maze = [[Cell_status(cells_info[i][j]) for j in range(cols)] for i in range(rows)]


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


def draw_maze(frame):
    """Draws the static maze grid."""
    for i in range(rows):
        for j in range(cols):
            # cs = Cell_status(grid[i][j])
            if maze[i][j].track == 2:
                draw_image_in_cell(yellow_cell_image, i, j)
            if maze[i][j].track == 3:
                draw_image_in_cell(red_cell_image, i, j)
            if maze[i][j].right == 1:
                draw_image_in_cell(right_image, i, j)
            if maze[i][j].left == 1:
                draw_image_in_cell(left_image, i, j)
            if maze[i][j].up == 1:
                draw_image_in_cell(up_image, i, j)
            if maze[i][j].down == 1:
                draw_image_in_cell(down_image, i, j)
            if maze[i][j].portal == 1:
                draw_image_in_cell(portalGif_frames[frame], i, j)
            if maze[i][j].teleport == 1:
                draw_image_in_cell(teleport_image, i, j)
            # maze[i][j] = cs


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

    draw_maze(portalGif_index)

    draw_image_in_cell(rightArrow_image, left_side_arrow[0], left_side_arrow[1])
    draw_image_in_cell(rightArrow_image, right_side_arrow[0], right_side_arrow[1])

    draw_image_in_cell(character_image, player.__getitem__()[0], player.__getitem__()[1])

    # Update the display
    pygame.display.flip()

    # Control the frame rate for the GIF animation (e.g., 10 FPS)
    clock.tick(10)
