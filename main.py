import sys
from time import sleep

import pygame
from pygame import mixer
from PIL import Image
from Character import Character
from Cell_status import Cell_status
from config import left_side_arrow, right_side_arrow, yellow_cell_image, red_cell_image, maze, win_pos
from config import left_puzzle_image, right_puzzle_image, down_puzzle_image, up_puzzle_image, puzzle_position
from config import GRAY, BLACK, character_image, player_x, player_y, teleport_image, CELL_SIZE, mist_image
from config import rows, cols, WIDTH, HEIGHT, down_image, right_image, rightArrow_image, left_image, up_image

# Initialize Pygame
pygame.init()

mixer.init()
mixer.music.load("Nu - Man O To.mp3")
mixer.music.play(-1)


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZE")

maze = [[Cell_status(maze[i][j]) for j in range(cols)] for i in range(rows)]


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
            if maze[i][j].mist == 1:
                draw_image_in_cell(mist_image, i, j)


def display_score(score):
    font = pygame.font.Font(None, 20)
    text = f"player score: {score}"
    text_surface = font.render(text, True, (255, 255, 0))
    # Calculate cell position
    x = 0
    y = 1

    cell_x = x * CELL_SIZE
    cell_y = y * CELL_SIZE
    # Center text within the cell
    text_rect = text_surface.get_rect(center=(cell_y + CELL_SIZE // 2, cell_x + CELL_SIZE // 2))
    # Blit text to the screen
    screen.blit(text_surface, text_rect)


def won_message():
    font = pygame.font.Font(None, 20)
    text = f"you won!"
    text_surface = font.render(text, True, (148, 0, 211))
    # Calculate cell position
    x = 0
    y = 5

    cell_x = x * CELL_SIZE
    cell_y = y * CELL_SIZE
    # Center text within the cell
    text_rect = text_surface.get_rect(center=(cell_y + CELL_SIZE // 2, cell_x + CELL_SIZE // 2))
    # Blit text to the screen
    screen.blit(text_surface, text_rect)


player = Character(player_x, player_y)


clock = pygame.time.Clock()


def draw_puzzle():
    for i in range(rows):
        for j in range(cols):
            match puzzle_position[i][j]:
                case 1:
                    draw_image_in_cell(left_puzzle_image, i, j)
                    maze[i][j].leftPuzzle = True
                    maze[i][j - 1].rightPuzzle = True
                case 2:
                    draw_image_in_cell(up_puzzle_image, i, j)
                    maze[i][j].upPuzzle = True
                    maze[i - 1][j].downPuzzle = True
                case 3:
                    draw_image_in_cell(right_puzzle_image, i, j)
                    maze[i][j].rightPuzzle = True
                    maze[i][j + 1].leftPuzzle = True
                case 4:
                    draw_image_in_cell(down_puzzle_image, i, j)
                    maze[i][j].downPuzzle = True
                    maze[i + 1][j].upPuzzle = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.won = True if player.player_x == win_pos[0] and player.player_y == win_pos[1] else False

    keys = pygame.key.get_pressed()

    player.move(keys, maze)

    screen.fill(BLACK)

    draw_grid()

    portalGif_index = (portalGif_index + 1) % len(portalGif_frames)

    draw_maze(portalGif_index)

    draw_puzzle()

    draw_image_in_cell(rightArrow_image, left_side_arrow[0], left_side_arrow[1])
    draw_image_in_cell(rightArrow_image, right_side_arrow[0], right_side_arrow[1])

    draw_image_in_cell(character_image, player.__getitem__()[0], player.__getitem__()[1])

    display_score(min(player.score, 2000)) if player.won else display_score(player.score)

    won_message() if player.won else None

    pygame.display.flip()

    if player.won:
        sleep(2)
        sys.exit()

    clock.tick(10)
