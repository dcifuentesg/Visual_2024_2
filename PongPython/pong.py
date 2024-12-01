import pygame
import sys

pygame.init()

# window
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# paleta
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

# bola
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE, BALL_SIZE
        )
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with top or bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1
        self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

# inicializador(posiciones)
left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Puntaje
left_score = 0
right_score = 0
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()
FPS = 60

def draw_scores():
    score_text = font.render(f"{left_score}    {right_score}", True, WHITE)
    WINDOW.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

# Juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento
    keys = pygame.key.get_pressed()
   
    if keys[pygame.K_w]:
        left_paddle.move_up()
    if keys[pygame.K_s]:
        left_paddle.move_down()
    
    if keys[pygame.K_UP]:
        right_paddle.move_up()
    if keys[pygame.K_DOWN]:
        right_paddle.move_down()

    
    ball.move()

    # Colisicones
    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.speed_x *= -1

    # Puntaje update
    if ball.rect.left <= 0:
        right_score += 1
        ball.reset()
    if ball.rect.right >= WIDTH:
        left_score += 1
        ball.reset()


    WINDOW.fill(BLACK)
    left_paddle.draw(WINDOW)
    right_paddle.draw(WINDOW)
    ball.draw(WINDOW)
    draw_scores()

    pygame.display.flip()

    clock.tick(FPS)
