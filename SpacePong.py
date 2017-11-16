# Written by Florian Wolf, 15.11.2017
# imports
import pygame
import random
import math
from pygame.locals import *

# setup
pygame.init()
pygame.font.init()
res = (1280, 720)
width = 1280
height = 720
screen = pygame.display.set_mode(res)
screen.fill((0, 0, 0))

# point counter font
font = pygame.font.SysFont('Impact', 42)

# ball class
class Ball:
    def __init__(self):
        self.posX = width/2
        self.posY = height/2
        positions = [-1, 1]
        self.velX = positions[random.randint(0, 1)]
        self.velY = positions[random.randint(0, 1)]
        self.ballSize = 8
        self.ballColor = (255, 255, 255)


# block class
class Block:
    def __init__(self, x):
        self.x = x
        self.y = height/2
        self.velocity = 0.5


# star class
class Star:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)


# helper function - map values to 0-255 color range for star colors
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


# helper function - stop a value from overshooting a certain maximum, keep n within two bounds
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


# make stars
drawStars = True
starColor = (255, 255, 255)
starCount = 200
stars = []
if drawStars:
    for x in range(starCount):
        stars.append(Star())

# create the ball
ballSpeed = 2
ballMaxVelocity = 3
ballTorque = 0.003
ball = Ball()

# create two blocks
blockToSide = 100
blockHeight = 200
blockWidth = 10
blockSpeed = 2
blockVelocityIncrement = 0.04
blockL = Block(blockToSide)
blockR = Block(width-blockToSide)

# tracking key presses
arrowUpPressed = False
arrowDownPressed = False
wPressed = False
sPressed = False

# tracking the score
pointsL = 0
pointsR = 0

# ball positions below this height / past this height are out of bounds vertically (bounce from decoration lines instead of window edges)
bounceBounds = 10

# game logic loop
running = True
respawn = False
respawnTime = 1000
respawnTimer = 0
while running:
    # erase screen each frame
    screen.fill((0, 0, 0))

    # check the pygame events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # inputs
        # registering the begin of a keypress and adjusting the block velocity
        if event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                blockR.velocity = abs(blockR.velocity) * -1
                arrowUpPressed = True
            if event.key == pygame.K_DOWN:
                blockR.velocity = abs(blockR.velocity)
                arrowDownPressed = True
            if event.key == pygame.K_w:
                blockL.velocity = abs(blockL.velocity) * -1
                wPressed = True
            if event.key == pygame.K_s:
                blockL.velocity = abs(blockL.velocity)
                sPressed = True

        # registering the end of a keypress and adjusting the block velocity
        if event.type == KEYUP:
            if event.key == pygame.K_UP:
                arrowUpPressed = False
                blockR.velocity = 1
            if event.key == pygame.K_DOWN:
                arrowDownPressed = False
                blockR.velocity = 1
            if event.key == pygame.K_w:
                wPressed = False
                blockL.velocity = 1
            if event.key == pygame.K_s:
                sPressed = False
                blockL.velocity = 1

    # moving the blocks if keys are pressed
    if arrowUpPressed:
        if blockR.y - blockSpeed > bounceBounds+blockHeight/2:
            blockR.velocity -= blockVelocityIncrement
            blockR.y += blockSpeed * blockR.velocity
    elif arrowDownPressed:
        if blockR.y + blockSpeed < height-blockHeight/2-bounceBounds:
            blockR.velocity += blockVelocityIncrement
            blockR.y += blockSpeed * blockR.velocity
    if wPressed:
        if blockL.y - blockSpeed > bounceBounds+blockHeight/2:
            blockL.velocity -= blockVelocityIncrement
            blockL.y += blockSpeed * blockL.velocity
    elif sPressed:
        if blockL.y + blockSpeed < height-blockHeight/2-bounceBounds:
            blockL.velocity += blockVelocityIncrement
            blockL.y += blockSpeed * blockL.velocity

    # we are currently playing, not respawning
    if not respawn:
        # moving the ball
        newX = int(ball.posX + ball.velX * ballSpeed)
        newY = int(ball.posY + ball.velY * ballSpeed)

        # the ball is still within the playing field => check if it hits the top/button or the blocks
        if 0 < newX < width:

            # the ball bounces from the top
            if newY <= bounceBounds+ball.ballSize:
                ball.velY = ball.velY * -1
                newX = int(ball.posX + ball.velX * ballSpeed)
                newY = int(ball.posY + ball.velY * ballSpeed)

            # the ball bounces from the bottom
            elif newY >= height-bounceBounds:
                ball.velY = ball.velY * -1
                newX = int(ball.posX + ball.velX * ballSpeed)
                newY = int(ball.posY + ball.velY * ballSpeed)

            # the ball touches the left block => bounce
            elif blockToSide + blockWidth + ball.ballSize - 7 <= newX <= blockToSide + blockWidth + ball.ballSize and blockL.y - blockHeight/2 - ball.ballSize <= ball.posY <= blockL.y + blockHeight/2 + ball.ballSize:
                ball.velX = clamp((ball.velX * -1) + abs(translate(blockL.velocity, -4.7, 4.7, -3, 3)), -ballMaxVelocity, ballMaxVelocity)
                newVelY = ball.velY + translate(blockL.velocity, -4.7, 4.7, -3, 3)
                if newVelY > 0:
                    ball.velY = clamp(newVelY, 1.1, ballMaxVelocity)
                elif newVelY <= 0:
                    ball.velY = clamp(newVelY, -1.1, -ballMaxVelocity)
                newX = ball.posX + ball.velX * ballSpeed
                newY = ball.posY + ball.velY * ballSpeed

            # the ball touches the right block => bounce
            elif width - blockToSide - ball.ballSize <= newX <= width - blockToSide - ball.ballSize + 7 and blockR.y - blockHeight/2 - ball.ballSize <= ball.posY <= blockR.y + blockHeight/2 + ball.ballSize:
                ball.velX = clamp((ball.velX * -1) - abs(translate(blockR.velocity, -4.7, 4.7, -3, 3)), -ballMaxVelocity, ballMaxVelocity)
                newVelY = ball.velY + translate(blockR.velocity, -4.7, 4.7, -3, 3)
                if newVelY > 0:
                    ball.velY = clamp(newVelY, 1.1, ballMaxVelocity)
                elif newVelY <= 0:
                    ball.velY = clamp(newVelY, -1.1, -ballMaxVelocity)
                newX = int(ball.posX + ball.velX)
                newY = int(ball.posY + ball.velY)

            # the ball can move around freely
            elif 0 < newY < height:
                ball.posX = newX
                ball.posY = newY

                # remove velocity over time
                if ball.velY > 1 + ballTorque:
                    ball.velY -= ballTorque
                if ball.velY < -1 - ballTorque:
                    ball.velY += ballTorque
                if ball.velX > 1 + ballTorque:
                    ball.velX -= ballTorque
                if ball.velX < -1 - ballTorque:
                    ball.velX += ballTorque

        # reset the ball and add a point for the enemy
        else:
            if newX <= 0:
                pointsR += 1
            if newX >= width:
                pointsL += 1

            # save the current ticks in order to stop the game for a second
            respawnTimer = pygame.time.get_ticks()
            respawn = True

    # we are currently respawning => move the ball smoothly back to the center
    elif pygame.time.get_ticks() - respawnTime < respawnTimer:
        speed = 5

        # distance in pixels between the ball and the center (vector calculations, google it)
        distanceToCenter = math.sqrt((width/2 - ball.posX) ** 2 + (height/2 - ball.posY) ** 2)

        # angle between ball and center
        deltaX = width/2 - ball.posX
        deltaY = height/2 - ball.posY
        angle_rad = math.atan2(deltaY, deltaX)

        # vector to add to the ball position
        vectorX = speed * math.cos(angle_rad)
        vectorY = speed * math.sin(angle_rad)

        # new ball position
        ball.posX = int(ball.posX + vectorX)
        ball.posY = int(ball.posY + vectorY)

        # fading in the ball as it comes closer to the center
        color = int(translate(clamp(distanceToCenter, 0, 300), 0, 300, 255, 0))
        ball.ballColor = (color, color, color)

    # we are done respawning and now we continue to play
    elif pygame.time.get_ticks() - respawnTime >= respawnTimer:

        # allow the game loop to run with the next iteration
        respawn = False

        # instantiate the ball again, resetting/overwriting its position, color, size and velocity to the default values
        ball = Ball()

    # draw the stars - only draws stars if drawStars == True !!! If this gets removed, the game runs significantly faster and is thus harder!
    for star in stars:
        # distance between star and ball
        distanceToMouse = math.sqrt((star.x - ball.posX)**2 + (star.y - ball.posY)**2)

        # speed modifier, aka how much should the star move based on its distance to the ball
        speed = (distanceToMouse/100) + 1

        # size based on its distance to the ball
        starSize = int((distanceToMouse / (math.sqrt(height**2 + width**2))) * 10)

        # color based on its distance to the ball
        starColorValue = int(translate(distanceToMouse, 0, (math.sqrt(height**2 + width**2)), 15, 150))
        randColorMulti = random.uniform(0.2, 1)
        starColorValue = clamp(starColorValue * randColorMulti, 0, 150)
        starColor = (starColorValue, starColorValue, starColorValue)

        # angle between star and ball position
        deltaX = star.x - ball.posX
        deltaY = star.y - ball.posY
        angle_rad = math.atan2(deltaY, deltaX)

        # vector to add to the star position
        vectorX = speed * math.cos(angle_rad)
        vectorY = speed * math.sin(angle_rad)

        # new star position
        star.x = int(star.x + vectorX)
        star.y = int(star.y + vectorY)

        # draw the star
        pygame.draw.circle(screen, starColor, (star.x, star.y), starSize, 0)

        # star exits the screen => change its position to be within the radius (offset) of the ball
        if star.x < 0 or star.x > width or star.y < 0 or star.y > height:
            offset = 300
            star.x = random.randint(ball.posX-offset, ball.posX+offset)
            star.y = random.randint(ball.posY-offset, ball.posY+offset)

    # draw ball
    pygame.draw.circle(screen, ball.ballColor, (int(ball.posX - ball.ballSize / 2), int(ball.posY - ball.ballSize / 2)), ball.ballSize, 0)

    # draw blocks
    pygame.draw.rect(screen, (255, 255, 255), (blockL.x, blockL.y - blockHeight / 2, blockWidth, blockHeight))
    pygame.draw.rect(screen, (255, 255, 255), (blockR.x, blockR.y - blockHeight / 2, blockWidth, blockHeight))

    # draw point counter
    textSurfaceL = font.render(str(pointsL), False, (255, 255, 255))
    textSurfaceR = font.render(str(pointsR), False, (255, 255, 255))
    screen.blit(textSurfaceL, (3 * (width / 7)-21, 20))
    screen.blit(textSurfaceR, (width - (3 * (width / 7)), 20))

    # draw point counter decoration
    decorationColor = (150, 150, 150)
    pygame.draw.rect(screen, decorationColor, (0, 10, width / 2 - 40, 1))
    pygame.draw.rect(screen, decorationColor, (width / 2 + 40, 10, width, 1))
    pygame.draw.aalines(screen, decorationColor, False, [(width / 2 - 40, 10), (width / 2, 80), (width / 2 + 40, 10)], 1)
    pygame.draw.rect(screen, decorationColor, (0, height-10, width, 1))

    pygame.display.update()
pygame.quit()
