import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bg = pygame.image.load("assests/bg.jpg")
bird_img = pygame.image.load("assests/birdup.png")
pipe_top_img = pygame.image.load("assests/pipedown.jpg")
pipe_bottom_img = pygame.image.load("assests/pipeup.jpg")

# Scale images
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(bird_img, (50, 35))
pipe_top_img = pygame.transform.scale(pipe_top_img, (70, 300))
pipe_bottom_img = pygame.transform.scale(pipe_bottom_img, (70, 300))

# Game variables
bird_x = 80
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.5
jump_strength = -8

pipes = []
pipe_gap = 160
pipe_speed = 3
pipe_spawn_event = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn_event, 1500)

score = 0
font = pygame.font.SysFont("Arial", 28)
game_over_font = pygame.font.SysFont("Arial", 36, bold=True)

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

game_over = False

def reset_game():
    global bird_y, bird_vel, pipes, score, start_ticks, game_over
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = []
    score = 0
    game_over = False
    start_ticks = pygame.time.get_ticks()


def draw_window():
    win.blit(bg, (0, 0))
    win.blit(bird_img, (bird_x, int(bird_y)))

    for pipe in pipes:
        win.blit(pipe_top_img, (pipe['x'], pipe['top']))
        win.blit(pipe_bottom_img, (pipe['x'], pipe['bottom']))

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_text = font.render(f"Time: {seconds}s", True, (255, 255, 255))
    win.blit(time_text, (WIDTH - 150, 10))

    if game_over:
        over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
        win.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
        win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()


def check_collision():
    bird_rect = bird_img.get_rect(topleft=(bird_x, int(bird_y)))
    for pipe in pipes:
        top_rect = pipe_top_img.get_rect(topleft=(pipe['x'], pipe['top']))
        bottom_rect = pipe_bottom_img.get_rect(topleft=(pipe['x'], pipe['bottom']))
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    if bird_y < 0 or bird_y > HEIGHT:
        return True
    return False


# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_vel = jump_strength
            if event.type == pipe_spawn_event:
                pipe_height = random.randint(100, 350)
                pipes.append({
                    'x': WIDTH,
                    'top': pipe_height - pipe_top_img.get_height(),
                    'bottom': pipe_height + pipe_gap,
                    'passed': False
                })

    if not game_over:
        # Bird movement
        bird_vel += gravity
        bird_y += bird_vel

        # Move pipes
        for pipe in pipes:
            pipe['x'] -= pipe_speed

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] > -80]

        # Update score
        for pipe in pipes:
            if pipe['x'] + 70 < bird_x and not pipe['passed']:
                score += 1
                pipe['passed'] = True

        # Collision check
        if check_collision():
            game_over = True

    draw_window()
