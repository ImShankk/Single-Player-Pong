import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Player Pong")

# Define colors
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

# Define paddle properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5

# Define ball properties
BALL_RADIUS = 10
BALL_SPEED_EASY = 3
BALL_SPEED_MEDIUM = 4
BALL_SPEED_HARD = 6

# Define game variables
score = 0
game_over = False

# Set up the game clock
clock = pygame.time.Clock()


# Define the Paddle class (OOP REQUIREMENT)
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move_up(self):
        self.rect.y -= PADDLE_SPEED

    def move_down(self):
        self.rect.y += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(window, BLACK, self.rect)


# Define the Ball class (OOP REQUIREMENT)
class Ball:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = speed
        self.dy = speed

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def check_collision(self):
        if self.rect.colliderect(paddle.rect):
            self.dx *= -1
            return True
        return False

    def check_boundaries(self):
        if self.rect.top <= 10 or self.rect.bottom >= HEIGHT - 10:
            self.dy *= -1

        if self.rect.right >= WIDTH - 10:
            return True

        if self.rect.left <= 10:
            self.dx *= -1

        return False

    def end(self):
        self.rect.x = WIDTH // 2 - BALL_RADIUS
        self.rect.y = HEIGHT // 2 - BALL_RADIUS
        self.dx = ball_speed
        self.dy = ball_speed

    def draw(self):
        pygame.draw.circle(window, BLACK, self.rect.center, BALL_RADIUS)


# Create paddle
paddle = Paddle(WIDTH - PADDLE_WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)

# Difficulty selection menu
selected_difficulty = False
difficulty = None
font = pygame.font.Font(None, 48)

while not selected_difficulty:
    #FIRST SCREEN (fixed)
    window.fill(WHITE)
    title_text = font.render("Select Difficulty", True, BLACK)
    easy_text = font.render("Easy - Press 1", True, BLACK)
    medium_text = font.render("Medium - Press 2", True, BLACK)
    hard_text = font.render("Hard - Press 3", True, BLACK)

    #DISPLAY THE SCREEN
    window.blit(
        title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 96)
    )
    window.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 48))
    window.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
    window.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 48))

    pygame.display.flip()

    # DIFFICULTY SELECT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selected_difficulty = True
            game_over = True
            #EASY
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulty = "easy"
                selected_difficulty = True
            #MEDIUM
            elif event.key == pygame.K_2:
                difficulty = "medium"
                selected_difficulty = True
            #HARD
            elif event.key == pygame.K_3:
                difficulty = "hard"
                selected_difficulty = True

# Create ball object based on difficulty
if difficulty == "easy":
    ball_speed = BALL_SPEED_EASY
elif difficulty == "medium":
    ball_speed = BALL_SPEED_MEDIUM
elif difficulty == "hard":
    ball_speed = BALL_SPEED_HARD

#Ball size and shape and speed
ball = Ball(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, ball_speed)

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and ball.check_boundaries():
                score = 0
                ball.end()
                game_over = False

    # Move the paddle
    keys = pygame.key.get_pressed()
    # UP
    if keys[pygame.K_UP] and paddle.rect.top > 10:
        paddle.move_up()
    # DOWN
    if keys[pygame.K_DOWN] and paddle.rect.bottom < HEIGHT - 10:
        paddle.move_down()

    # Move the ball
    ball.move()

    # Check collision with paddle and update score
    if ball.check_collision():
        score += 1

    # Check boundaries and handle game over
    if ball.check_boundaries() and ball.rect.right >= WIDTH - 10:
        game_over = True

    # Clear the screen
    window.fill(WHITE)

    # Draw borders
    pygame.draw.rect(window, PURPLE, pygame.Rect(0, 0, 10, HEIGHT))  # Left border
    pygame.draw.rect(window, PURPLE, pygame.Rect(WIDTH - 10, 0, 10, HEIGHT))  # Right border
    pygame.draw.rect(window, PURPLE, pygame.Rect(0, 0, WIDTH, 10))  # Top border
    pygame.draw.rect(window, PURPLE, pygame.Rect(0, HEIGHT - 10, WIDTH, 10))  # Bottom border

    # Draw the paddle
    paddle.draw()

    # Draw the ball
    ball.draw()

    # Draw the score
    score_text = font.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the game's frame rate
    clock.tick(60)

# Game over screen
window.fill(WHITE)
game_over_text = font.render("GAME OVER", True, BLACK)
score_text = font.render("Score: " + str(score), True, BLACK)
instruction_text = font.render("To End The Game Press ESCAPE", True, BLACK)
window.blit(
    game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 96)
)
window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 48))
window.blit(
    instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 48)
)
pygame.display.flip()

# Wait for the "Escape" key to end the game
endGame = False
while not endGame:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                endGame = True

# Quit the game
pygame.quit()
