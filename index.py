import os
from random import randint
import pygame, sys
import random
import time
from pygame.locals import *
from collections import OrderedDict
import pyautogui


def loopFunction():
    pygame.init()

    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('Pong')
    clock = pygame.time.Clock()
    run = True
    start = gameover = False

    playerSpeed = 4
    opponentSpeed = 4
    playerCooY = opponnentCooY = 225
    playerCooX = 40
    opponentCooX = 460
    direction = "null"

    counterBeforeBonus = 6

    ballSpeed = 3
    ballCooX = 300
    ballCooY = 255
    ballSize = 10
    ballDirectionX = ballDirectionY = 0

    bonusCooX = 2000
    bonusCooY = 2000
    playerScore = opponentScore = 0

    bonusOccuring = False

    pygame.draw.line(screen, (125, 125, 125), (300, 0), (300, 600), 1)
    pygame.draw.circle(screen, (255, 255, 255), (ballCooX, ballCooY), ballSize)
    pygame.draw.rect(screen, (255, 255, 255), Rect(20, playerCooY, 10, 50))
    pygame.draw.rect(screen, (255, 255, 255), Rect(570, opponnentCooY, 10, 50))
    font = pygame.font.Font('freesansbold.ttf', 32)
    beginText = font.render("Press any key to begin", True, (255, 255, 255))
    screen.blit(beginText, (125, 300))
    playerText = font.render("Player", True, (255, 255, 255))
    screen.blit(playerText, (100, 400))
    opponentText = font.render("Opponent", True, (255, 255, 255))
    screen.blit(opponentText, (370, 400))

    while run:
        while gameover:
            font = pygame.font.SysFont(None, 50)
            end = font.render('Press Enter to restart game', True, (255, 255, 255))
            screen.blit(end, (350, 250))
            clock.tick(60)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        loopFunction()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if start is False:
                        start = True
                        ballDirection = randint(0, 1)
                        ballDirectionY = randint(1.0, 3.0)
                        ballDirectionYAngle = randint(0, 1)
                        if ballDirectionYAngle == 0:
                            ballDirectionY = ballDirectionY * -1
                    if event.key == pygame.K_UP:
                        direction = "up"
                    if event.key == pygame.K_DOWN:
                        direction = "down"
                if event.type == pygame.KEYUP:
                    direction = "null"
            if direction == "up":
                if playerCooY > 0:
                    playerCooY -= playerSpeed
            if direction == "down":
                if playerCooY < 450:
                    playerCooY += playerSpeed
            if opponnentCooY > 0:
                opponnentCooY -= opponentSpeed
            if opponnentCooY < 450:
                opponnentCooY += opponentSpeed
            ballCooY += ballDirectionY
            if start is True:
                screen.fill((0, 0, 0))
                pygame.draw.line(screen, (125, 125, 125), (300, 0), (300, 600), 1)
                pygame.draw.circle(screen, (255, 255, 255), (ballCooX, ballCooY), ballSize)
                pygame.draw.rect(screen, (255, 255, 255), Rect(20, playerCooY, 10, 50))
                pygame.draw.rect(screen, (255, 255, 255), Rect(570, opponnentCooY, 10, 50))
                pygame.draw.circle(screen, (255, 228, 54), (bonusCooX, bonusCooY), 10)
                playerScoreText = font.render(str(playerScore), True, (255, 255, 255))
                opponentScoreText = font.render(str(opponentScore), True, (255, 255, 255))
                screen.blit(playerScoreText, (400, 20))
                screen.blit(opponentScoreText, (100, 20))
                if ballDirection == 0:
                    ballCooX -= ballSpeed
                if ballDirection == 1:
                    ballCooX += ballSpeed
                if ballCooY < 0 or ballCooY > 495:
                    ballDirectionY *= -1

                # Collision avec les curseurs
                if Rect.colliderect(Rect(ballCooX, ballCooY, ballSize, ballSize), Rect(20 + 10, playerCooY, 10, 50)):
                    ballDirection = 1
                    counterBeforeBonus -= 1
                if Rect.colliderect(Rect(ballCooX + 10, ballCooY, ballSize, ballSize), Rect(570, opponnentCooY, 10, 50)):
                    ballDirection = 0
                    counterBeforeBonus -= 1

                # Collision avec l'opponent
                if ballCooX > 595:
                    playerCooY = opponnentCooY = 225
                    opponentScore += 1
                    ballCooX = 300
                    ballCooY = 255
                    ballDirection = randint(0, 1)
                    ballDirectionY = random.randrange(-2, 2)
                    ballDirectionY = randint(1, 3)
                    ballDirectionYAngle = randint(0, 1)
                    if ballDirectionYAngle == 0:
                        ballDirectionY = ballDirectionY * -1
                    ballSpeed = 3
                    opponentSpeed = 4
                    playerSpeed = 4
                    ballSize = 10
                    time.sleep(1)
                # Collision avec le joueur
                if ballCooX < 0:
                    playerCooY = opponnentCooY = 225
                    playerScore += 1
                    ballCooX = 300
                    ballCooY = 255
                    ballDirection = randint(0, 1)
                    ballDirectionY = randint(1.0, 3.0)
                    ballDirectionYAngle = randint(0, 1)

                    if ballDirectionYAngle == 0:
                        ballDirectionY = ballDirectionY * -1
                    ballSpeed = 3
                    opponentSpeed = 4
                    ballSize = 10
                    playerSpeed = 4
                    time.sleep(1)

                # Mouvement de l'opponent
                if opponnentCooY < ballCooY:
                    opponnentCooY += opponentSpeed
                if opponnentCooY + 50 > ballCooY + ballSize:
                    opponnentCooY -= opponentSpeed

                bonusCooX -= 1

                if counterBeforeBonus == 0:
                    counterBeforeBonus = 6
                    bonusCooX = 295
                    bonusCooY = randint(0, 495)
                    ballSpeed += 0.5
                if bonusOccuring == True:
                    time.sleep(1)
                    bonusOccuring = False

                if Rect.colliderect(Rect(playerCooX-15, playerCooY, 10, 50), Rect(bonusCooX, bonusCooY, 10, 10)):
                    opponentSpeed = 4
                    bonusEffect = randint(0, 4)
                    bonusCooX = 2000
                    if bonusEffect == 0:
                        if ballSpeed-2 > 1:
                            ballSpeed -= 2
                        bonusText = font.render(str("ball slowed"), True, (255, 0, 0))
                        screen.blit(bonusText, (400, 20))
                    if bonusEffect == 1:
                        opponentSpeed = 1
                        bonusText = font.render(str("opponent slowed"), True, (255, 0, 0))
                        screen.blit(bonusText, (400, 20))
                    if bonusEffect == 2:
                        ballSize = 5
                        opponentSpeed = 1
                        bonusText = font.render(str("ball is smaller"), True, (255, 0, 0))
                        screen.blit(bonusText, (400, 20))
                    if bonusEffect == 3:
                        playerSpeed = 1
                        bonusText = font.render(str("player slowed"), True, (255, 0, 0))
                        screen.blit(bonusText, (400, 20))
                    if bonusEffect == 4:
                        ballSpeed += 1
                        bonusText = font.render(str("ball is faster"), True, (255, 0, 0))
                        screen.blit(bonusText, (400, 20))
                    bonusOccuring = True
        clock.tick(60)
        pygame.display.flip()


loopFunction()
