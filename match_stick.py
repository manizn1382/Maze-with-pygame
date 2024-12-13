import pygame
import sys
from itertools import count
from time import sleep

from config import right_stick_image, left_stick_image, up_stick_image


class match_stick:
    def __init__(self, position, image, id):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.Id = id


# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drag and Drop PNG Example")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
Id = count(start=1)
mistake_count = 0

# Create rects for matchsticks
start_state = [
    # 1
    match_stick((50, 100), up_stick_image, next(Id)),
    match_stick((50, 20), up_stick_image, next(Id)),


    # +

    match_stick((100, 100), left_stick_image, next(Id)),
    match_stick((140, 60), up_stick_image, next(Id)),

    # 2
    match_stick((195, 100), left_stick_image, next(Id)),
    match_stick((205, 29), right_stick_image, next(Id)),
    match_stick((195, 100), up_stick_image, next(Id)),
    match_stick((195, 170), left_stick_image, next(Id)),
    match_stick((275, 29), up_stick_image, next(Id)),

    # -
    match_stick((315, 100), left_stick_image, next(Id)),

    # 3
    match_stick((490, 20), up_stick_image, next(Id)),
    match_stick((410, 100), left_stick_image, next(Id)),
    match_stick((410, 20), left_stick_image, next(Id)),
    match_stick((410, 170), left_stick_image, next(Id)),
    match_stick((490, 100), up_stick_image, next(Id)),

    # =
    match_stick((530, 100), left_stick_image, next(Id)),
    match_stick((530, 86), left_stick_image, next(Id)),

    # 1
    match_stick((637, 100), up_stick_image, next(Id)),
    match_stick((637, 20), up_stick_image, next(Id)),

    # 9

    match_stick((750, 100), up_stick_image, next(Id)),
    match_stick((750, 20), up_stick_image, next(Id)),
    match_stick((680, 20), right_stick_image, next(Id)),
    match_stick((680, 20), up_stick_image, next(Id)),
    match_stick((680, 100), left_stick_image, next(Id)),
    match_stick((680, 170), left_stick_image, next(Id)),

    # 9
    match_stick((850, 100), up_stick_image, next(Id)),
    match_stick((850, 20), up_stick_image, next(Id)),
    match_stick((780, 20), right_stick_image, next(Id)),
    match_stick((780, 20), up_stick_image, next(Id)),
    match_stick((780, 100), left_stick_image, next(Id)),
    match_stick((780, 170), left_stick_image, next(Id)),

]


# Button setup
button_rect = pygame.Rect(SCREEN_WIDTH // 3, SCREEN_HEIGHT - 50, 100, 30)
font = pygame.font.Font(None, 24)
result_message = ""

# Dragging state
dragging = None
offset_x, offset_y = 0, 0


def validate_expression():
    """
    Validate the matchstick arrangement by comparing the start_state and win_state.
    Returns True if both states are equal, otherwise False.
    """
    for i in start_state:
        if i.Id == 23 and i.rect.topleft == (100, 29):
            return True
    return False


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # Start dragging on mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # If button is clicked, validate the matchstick puzzle
                if validate_expression():
                    result_message = "Correct!"
                else:
                    mistake_count += 1
                    if mistake_count == 3:
                        result_message = "you lose!"
                    else:
                        result_message = "Try Again!"

            for stick in start_state:
                if stick.rect.collidepoint(event.pos):
                    dragging = stick
                    offset_x = event.pos[0] - stick.rect.x
                    offset_y = event.pos[1] - stick.rect.y
                    break

        # Stop dragging on mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        # Update position of dragged matchstick
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dragging.rect.x = event.pos[0] - offset_x
                dragging.rect.y = event.pos[1] - offset_y

    # Clear screen
    screen.fill(BLACK)

    # Draw matchsticks
    for stick in start_state:
        screen.blit(stick.image, stick.rect.topleft)

    # Draw button
    pygame.draw.rect(screen, GRAY, button_rect)
    button_text = font.render("Validate", True, BLACK)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

    # Display result message
    if result_message:
        result_color = GREEN if result_message == "Correct!" else RED
        result_text = font.render(result_message, True, result_color)
        screen.blit(result_text, (50, SCREEN_HEIGHT - 50))

    # Update display
    pygame.display.flip()

    if result_message == "you lose!" or result_message == "Correct!":
        sleep(1)
        sys.exit()

    # Limit frame rate
    pygame.time.Clock().tick(60)
