# setup
import pygame
import random
from pygame.locals import *

pygame.init()
pygame.font.init()
res = (1280, 720)
height = 720
width = 1280
screen = pygame.display.set_mode(res)
screen.fill((0, 0, 0))

# point counter font
font = pygame.font.SysFont('Comic Sans MS', 30)

# ball class
class Ball:
    def __init__(self):
        self.posX = width/2
        self.posY = height/2
        positions = [-1, 1]
        self.velX = positions[random.randint(0, 1)]
        self.velY = positions[random.randint(0, 1)]


# block class
class Block:
    def __init__(self, x):
        self.x = x
        self.y = height/2


# create the ball
ballSize = 20
ballSpeed = 1
ball = Ball()


# create two blocks
blockToSide = 100
blockHeight = 120
blockSpeed = 2
blockL = Block(blockToSide)
blockR = Block(width-blockToSide)

# tracking key presses
arrowUpPressed = False
arrowDownPressed = False
wPressed = False
sPressed = False

# tracking points
pointsL = 0
pointsR = 0

# game loop
running = True
while running:
    # redraw screen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), ((width / 2)-1, 0, 2, height))
    textSurfaceL = font.render(str(pointsL), False, (255, 255, 255))
    textSurfaceR = font.render(str(pointsR), False, (255, 255, 255))

    screen.blit(textSurfaceL, (width/4, 50))
    screen.blit(textSurfaceR, (width - (width /4), 50))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # inputs
        if event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                arrowUpPressed = True
            if event.key == pygame.K_DOWN:
                arrowDownPressed = True
            if event.key == pygame.K_w:
                wPressed = True
            if event.key == pygame.K_s:
                sPressed = True

        if event.type == KEYUP:
            if event.key == pygame.K_UP:
                arrowUpPressed = False
            if event.key == pygame.K_DOWN:
                arrowDownPressed = False
            if event.key == pygame.K_w:
                wPressed = False
            if event.key == pygame.K_s:
                sPressed = False

    # moving the blocks
    if arrowUpPressed:
        if blockR.y - blockSpeed > 0+blockHeight/2:
            blockR.y -= blockSpeed
    elif arrowDownPressed:
        if blockR.y + blockSpeed < height-blockHeight/2:
            blockR.y += blockSpeed
    if wPressed:
        if blockL.y - blockSpeed > 0+blockHeight/2:
            blockL.y -= blockSpeed
    elif sPressed:
        if blockL.y + blockSpeed < height-blockHeight/2:
            blockL.y += blockSpeed

    # moving the ball
    newX = ball.posX + ball.velX
    newY = ball.posY + ball.velY

    reset = False
    # the ball is still within the playing field
    if newX > 0 and newX < width:

        # the ball touches the left block
        if newX == blockToSide and blockL.y - blockHeight/2 < ball.posY and blockL.y + blockHeight/2 > ball.posY:
            ball.velX = ball.velX * -1
            newX = ball.posX + ball.velX
            newY = ball.posY + ball.velY

        # the ball touches the right block
        elif newX == width-blockToSide and blockR.y - blockHeight/2 < ball.posY and blockR.y + blockHeight/2 > ball.posY:
            ball.velX = ball.velX * -1
            newX = ball.posX + ball.velX
            newY = ball.posY + ball.velY

        # the ball can move around freely
        elif newY > 0 and newY < height:
            ball.posX = newX
            ball.posY = newY

        # the ball bounces from the top
        elif newY >= 0:
            ball.velY = ball.velY * -1
            newX = ball.posX + ball.velX
            newY = ball.posY + ball.velY

        # the ball bounces from the bottom
        elif newY <= height:
            ball.velY = ball.velY * -1
            newX = ball.posX + ball.velX
            newY = ball.posY + ball.velY

    # reset the ball and add a point
    else:
        if newX <= 0:
            pointsR += 1
        if newX >= width:
            pointsL += 1
        ball = Ball()


    # update blocks
    pygame.draw.rect(screen, (255, 255, 255), (blockL.x, blockL.y - blockHeight / 2, 5, blockHeight))
    pygame.draw.rect(screen, (255, 255, 255), (blockR.x, blockR.y - blockHeight / 2, 5, blockHeight))

    # update ball
    pygame.draw.rect(screen, (255, 255, 255), (int(ball.posX-ballSize/2), int(ball.posY-ballSize/2), ballSize, ballSize))

    pygame.display.update()
pygame.quit()
