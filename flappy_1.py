import pygame
from random import randint

# --- Khởi tạo ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# --- Màu sắc ---
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# --- Ảnh ---
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))

# --- Hằng số ---
TUBE_WIDTH = 50
TUBE_VELOCITY = 3
TUBE_GAP = 150
TUBE_DISTANCE = 200
GRAVITY = 0.5
BIRD_JUMP = -10
BIRD_X = 50

# --- Biến ---
score = 0
font = pygame.font.SysFont('sans', 24)
clock = pygame.time.Clock()
running = True
game_over = False

# --- Hàm reset game ---
def reset_game():
    global tube1_x, tube2_x, tube3_x
    global tube1_height, tube2_height, tube3_height
    global tube1_pass, tube2_pass, tube3_pass
    global bird_y, bird_drop_velocity, score, game_over

    tube1_x = 400
    tube2_x = tube1_x + TUBE_DISTANCE
    tube3_x = tube2_x + TUBE_DISTANCE

    tube1_height = randint(100, 400)
    tube2_height = randint(100, 400)
    tube3_height = randint(100, 400)

    tube1_pass = tube2_pass = tube3_pass = False

    bird_y = 300
    bird_drop_velocity = 0
    score = 0
    game_over = False

reset_game()

# --- Game loop ---
while running:
    clock.tick(60)
    screen.blit(background, (0, 0))  # Vẽ nền

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird_drop_velocity = BIRD_JUMP  # chim bay lên

    if not game_over:
        # Di chuyển ống
        tube1_x -= TUBE_VELOCITY
        tube2_x -= TUBE_VELOCITY
        tube3_x -= TUBE_VELOCITY

        # Cho chim rơi
        bird_y += bird_drop_velocity
        bird_drop_velocity += GRAVITY

        # Reset ống khi ra khỏi màn hình
        if tube1_x < -TUBE_WIDTH:
            tube1_x = tube3_x + TUBE_DISTANCE
            tube1_height = randint(100, 400)
            tube1_pass = False
        if tube2_x < -TUBE_WIDTH:
            tube2_x = tube1_x + TUBE_DISTANCE
            tube2_height = randint(100, 400)
            tube2_pass = False
        if tube3_x < -TUBE_WIDTH:
            tube3_x = tube2_x + TUBE_DISTANCE
            tube3_height = randint(100, 400)
            tube3_pass = False

        # --- Vẽ ống ---
        pygame.draw.rect(screen, BLUE, (tube1_x, 0, TUBE_WIDTH, tube1_height))
        pygame.draw.rect(screen, BLUE, (tube2_x, 0, TUBE_WIDTH, tube2_height))
        pygame.draw.rect(screen, BLUE, (tube3_x, 0, TUBE_WIDTH, tube3_height))

        pygame.draw.rect(screen, BLUE, (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height - TUBE_GAP))
        pygame.draw.rect(screen, BLUE, (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height - TUBE_GAP))
        pygame.draw.rect(screen, BLUE, (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height - TUBE_GAP))

        # --- Vẽ chim ---
        bird_rect = bird_img.get_rect(center=(BIRD_X + 15, bird_y + 15))
        screen.blit(bird_img, bird_rect)

        # --- Tính điểm ---
        if tube1_x + TUBE_WIDTH <= BIRD_X and not tube1_pass:
            score += 1
            tube1_pass = True
        if tube2_x + TUBE_WIDTH <= BIRD_X and not tube2_pass:
            score += 1
            tube2_pass = True
        if tube3_x + TUBE_WIDTH <= BIRD_X and not tube3_pass:
            score += 1
            tube3_pass = True

        # --- Va chạm ---
        tubes = [
            pygame.Rect(tube1_x, 0, TUBE_WIDTH, tube1_height),
            pygame.Rect(tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height - TUBE_GAP),
            pygame.Rect(tube2_x, 0, TUBE_WIDTH, tube2_height),
            pygame.Rect(tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height - TUBE_GAP),
            pygame.Rect(tube3_x, 0, TUBE_WIDTH, tube3_height),
            pygame.Rect(tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height - TUBE_GAP),
        ]
        for t in tubes:
            if bird_rect.colliderect(t):
                game_over = True
        if bird_y + bird_img.get_height() >= HEIGHT or bird_y <= 0:
            game_over = True

    # --- Hiển thị điểm ---
    score_txt = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_txt, (10, 10))

    # --- Game over ---
    if game_over:
        over_txt = font.render("GAME OVER - Press SPACE to restart", True, BLACK)
        screen.blit(over_txt, (30, 270))

    pygame.display.flip()

pygame.quit()
