import pygame
import random

# Initialize Pygame
pygame.init()

# Window Dimensions
width, height = 800, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong vs Computer")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)

# Paddle Properties
paddleWidth, paddleHeight = 10, 80
playerSpeed = 5
aiSpeed = 5  # Speed of the AI opponent

# Ball Properties
ballRadius = 10
ballSpeeds = {"easy": 2, "medium": 3, "hard": 4}  # mess around with speed on easy///

# Score Variables
playerScore = 0
aiScore = 0
maxScore = 5  # First to reach this wins

# Game Control Variables
gameOver = False
paused = False

# Game Clock
clock = pygame.time.Clock()


# Reset Game Function
def resetGame():
    global playerScore, aiScore, gameOver
    playerScore = 0
    aiScore = 0
    gameOver = False
    gameLoop()


# Show Message Function
def showMessage(text, color):
    font = pygame.font.Font(None, 48)
    message = font.render(text, True, color)
    window.blit(message, (width // 2 - message.get_width() // 2, height // 2))


# Paddle Class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, paddleWidth, paddleHeight)

    def move(self, direction):
        if direction == "up" and self.rect.top > 10:
            self.rect.y -= playerSpeed
        elif direction == "down" and self.rect.bottom < height - 10:
            self.rect.y += playerSpeed

    def draw(self):
        pygame.draw.rect(window, black, self.rect)


class ComputerPaddle(Paddle):
    def __init__(self, x, y, difficulty):
        super().__init__(x, y)
        self.difficulty = difficulty
        self.predictedPosition = y  # Store predicted position

    def move(self, ball):
        # Predict where the ball will be after some time
        self.predictBallPosition(ball)

        # Move paddle towards predicted position
        if self.rect.centery < self.predictedPosition:
            self.rect.y += aiSpeed
        elif self.rect.centery > self.predictedPosition:
            self.rect.y -= aiSpeed

    # Predict where the ball will be when it reaches the AI paddle (making a prediction model)

    def predictBallPosition(self, ball):
        # Current ball position
        ballY = ball.rect.centery
        ballVelocity = ball.dy

        # Estimate time for the ball to reach the AI paddle
        timeToReach = abs((ballY - self.rect.centery) / ballVelocity)

        # Predict where the ball will be when it reaches the AI paddle
        predictedY = ballY + ballVelocity * timeToReach

        # Handle potential bouncing off top and bottom walls
        predictedY = self.handleBouncing(predictedY, ball)

        # Set the predicted position
        self.predictedPosition = predictedY

    def handleBouncing(self, predictedY, ball):
        # Ball bouncing off top wall (y = 10)
        if predictedY <= 10:
            predictedY = 10 + (10 - predictedY)

        # Ball bouncing off bottom wall (y = height - 10)
        elif predictedY >= height - 10:
            predictedY = height - 10 - (predictedY - (height - 10))

        return predictedY


# Ball Class
class Ball:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, ballRadius * 2, ballRadius * 2)
        self.speed = speed
        self.reset()

    def reset(self):
        global playerScore, aiScore, gameOver

        self.rect.x, self.rect.y = width // 2 - ballRadius, height // 2 - ballRadius
        angle = random.uniform(-0.4, 0.4)  # Random bounce angle
        self.dx = self.speed * (1 if random.randint(0, 1) == 0 else -1)
        self.dy = self.speed * angle

        # Check if someone won
        if playerScore >= maxScore or aiScore >= maxScore:
            gameOver = True

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def checkCollision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.dx *= -1  # Reverse direction
            self.dy += random.uniform(
                -0.8, 0.8
            )  # Randomize bounce (messs around with numbers**)
            return True
        return False

    def checkBoundaries(self):
        global playerScore, aiScore

        # Top and bottom wall collision
        if self.rect.top <= 10 or self.rect.bottom >= height - 10:
            self.dy *= -1

        # Right side (Player loses a point)
        if self.rect.right >= width - 10:
            aiScore += 1
            self.reset()

        # Left side (computrer loses a point)
        if self.rect.left <= 10:
            playerScore += 1
            self.reset()

    def draw(self):
        pygame.draw.circle(window, black, self.rect.center, ballRadius)


# Select Difficulty
def selectDifficulty():
    font = pygame.font.Font(None, 48)
    selected = False
    difficulty = None

    while not selected:
        window.fill(white)
        texts = [
            ("Select Difficulty", black, height // 2 - 100),
            ("Easy - Press 1", green, height // 2 - 50),
            ("Medium - Press 2", black, height // 2),
            ("Hard - Press 3", red, height // 2 + 50),
        ]
        for text, color, y in texts:
            renderedText = font.render(text, True, color)
            window.blit(renderedText, (width // 2 - renderedText.get_width() // 2, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "easy"
                    selected = True
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                    selected = True
                elif event.key == pygame.K_3:
                    difficulty = "hard"
                    selected = True

    return difficulty


# Show End Screen Function
def showEndScreen(winner):
    font = pygame.font.Font(None, 48)
    while True:
        window.fill(white)
        if winner == "Player":
            message = font.render(
                "Player Wins! Press R to Restart or Q to Quit", True, green
            )
        else:
            message = font.render(
                "Computer Wins! Press R to Restart or Q to Quit", True, black
            )

        window.blit(message, (width // 2 - message.get_width() // 2, height // 2 - 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    resetGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


# Main Game Loop
def gameLoop():
    global gameOver, paused

    difficulty = selectDifficulty()
    ballSpeed = ballSpeeds[difficulty]

    # Create Game Objects
    playerPaddle = Paddle(width - paddleWidth - 20, height // 2 - paddleHeight // 2)
    cPaddle = ComputerPaddle(20, height // 2 - paddleHeight // 2, difficulty)
    ball = Ball(width // 2 - ballRadius, height // 2 - ballRadius, ballSpeed)

    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    resetGame()

        if not gameOver and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                playerPaddle.move("up")
            if keys[pygame.K_DOWN]:
                playerPaddle.move("down")

            cPaddle.move(ball)
            ball.move()
            ball.checkCollision(playerPaddle)
            ball.checkCollision(cPaddle)
            ball.checkBoundaries()

            # Check for game over
            if gameOver:
                if playerScore >= maxScore:
                    showEndScreen("Player")
                elif aiScore >= maxScore:
                    showEndScreen("Computer")

        window.fill(white)

        pygame.draw.rect(window, black, (0, 0, width, 10))  # Top border
        pygame.draw.rect(window, black, (0, height - 10, width, 10))  # Bottom border
        pygame.draw.rect(window, black, (0, 0, 10, height))  # Left border
        pygame.draw.rect(window, black, (width - 10, 0, 10, height))  # Right border

        playerPaddle.draw()
        cPaddle.draw()
        ball.draw()
        scoreText = font.render(
            f"Player: {playerScore}  Computer: {aiScore}", True, black
        )
        window.blit(scoreText, (width // 2 - scoreText.get_width() // 2, 10))

        if paused:
            showMessage("PAUSED (Press P to Resume)", red)
        if gameOver:
            showMessage("GAME OVER! Press R to Restart", red)

        pygame.display.flip()
        clock.tick(144)  # 144 fps


gameLoop()
