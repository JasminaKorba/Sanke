import pygame, random

pygame.init()

# Set a display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
dispaly_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

# Set FPS and a clock
FPS = 15
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20

head_x = WINDOW_WIDTH // 2
head_y = WINDOW_HEIGHT // 2 + 100

snake_dx = 0
snake_dy = 0

score = 0

# Set colours
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255)

# Set font
font = pygame.font.SysFont("gabriola", 48)

# Set text
title_text = font.render("Snake", True, GREEN, DARKRED)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

score_text = font.render(f"Score: {score}", True, GREEN, DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("Game over", True, RED, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("To play again press any key...", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

# Set sound and music
picku_up_sound = pygame.mixer.Sound("pick_up.wav")

# Set images
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(dispaly_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(dispaly_surface, GREEN, head_coord)

body_coords = []

# The main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT:
                snake_dx = SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    # Add the head coords to the firs index of the body list
    # This will essentilalyl move all of the snakes body by one position in the list
    body_coords.insert(0, head_coord)
    body_coords.pop()

    # Update the x, y position of the snake head and make a new coords
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for GAME OVER
    if (
        head_rect.left < 0
        or head_rect.right > WINDOW_WIDTH
        or head_rect.top < 0
        or head_rect.bottom > WINDOW_HEIGHT
    ) or head_coord in body_coords:
        dispaly_surface.blit(game_over_text, game_over_rect)
        dispaly_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game untile the player press a key, then reset the game
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                # The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0

                    head_x = WINDOW_WIDTH // 2
                    head_y = WINDOW_HEIGHT // 2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0
                    is_pause = False
                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False

    # Checked for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        picku_up_sound.play()

        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)

    # Udate HUD
    score_text = font.render(f"Score: {score}", True, GREEN, DARKRED)

    # Fill the surface
    dispaly_surface.fill(WHITE)

    # Blit HUD
    dispaly_surface.blit(title_text, title_rect)
    dispaly_surface.blit(score_text, score_rect)

    # Blit assets
    for body in body_coords:
        pygame.draw.rect(dispaly_surface, DARKGREEN, body)
    head_rect = pygame.draw.rect(dispaly_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(dispaly_surface, RED, apple_coord)

    # Update display and tick a clock
    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()
