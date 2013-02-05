import pygame, sys, random
from pygame.locals import *


def terminate():
    # terminate the game
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    # waiting for pressing any key
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, True, WHITE, AZURE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
                
                
# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
pygame.mouse.set_visible(False)
mouseIsOn = False

# set up the window
WINDOWWIDTH = 500
WINDOWHEIGHT = 430
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Cherry picker game')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AZURE = (0, 153, 255)

#set up fonts
basicFont = pygame.font.SysFont(None, 20)
headerFont = pygame.font.SysFont(None, 54)
scoreFont = pygame.font.SysFont(None, 36)

# set up background
bgrImg = pygame.image.load('tree.png').convert()
menuBgrImg = pygame.image.load('tree_blur.png').convert()
bgrRect = bgrImg.get_rect()

# set up sound
pickupSound = pygame.mixer.Sound('pick.wav')
fallenSound = pygame.mixer.Sound('fall.wav')
soundIsOn = True

#set up score and fallen cherries
score = 0
fallen = 0

# set up the player and fruit data structure
fruitCounter = 0
NEWFRUIT = 60
FRUITSIZE = 20
INICIALFRUIT = 5
player = pygame.Rect(WINDOWWIDTH / 2, WINDOWHEIGHT - 50, 50, 50)
playerImg = pygame.image.load('fox.png')
playerStretchedImg = pygame.transform.scale(playerImg, (50, 50))
fruits = []
for i in range(INICIALFRUIT):
    newFruit = {"rect": pygame.Rect(random.randint(0 + WINDOWWIDTH / 50, WINDOWWIDTH - FRUITSIZE - WINDOWWIDTH / 50), random.randint(30, WINDOWHEIGHT * 0.6), FRUITSIZE, FRUITSIZE), "falling": False}
    fruits.append(newFruit)
fruitImg = pygame.image.load('cherry2.png')

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

# set up game speed and difficulcy
FPS = 80
MOVESPEED = 4
FRUIT_FALL_CHANCE = 300
FALLINGSPEED = 3

# show the "Start" screen
windowSurface.blit(menuBgrImg, bgrRect)
elipse = pygame.draw.ellipse(windowSurface, AZURE, (WINDOWWIDTH/2 -175, WINDOWHEIGHT / 2 - 150, 350, 250), 0)
drawText('The', headerFont, windowSurface, elipse.centerx - 30, elipse.centery - 110)
drawText('Cherry Picker', headerFont, windowSurface, elipse.centerx - 120, elipse.centery - 60)
drawText('Press any key to start.', basicFont, windowSurface, elipse.centerx - 140, elipse.centery)
drawText('Use arrow to move', basicFont, windowSurface, elipse.centerx - 120, elipse.centery + 30)
drawText('TAB to turn off sounds.', basicFont, windowSurface, elipse.centerx - 100, elipse.centery + 60)
fox = pygame.Rect(elipse.centerx + 60, elipse.centery - 20, 80, 80)
windowSurface.blit(playerImg, fox)
pygame.display.update()
waitForPlayerToPressKey()

# running the game loop
while True:
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_ESCAPE:
                terminate()
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
            if event.key == K_TAB:
                soundIsOn = not soundIsOn
            if event.key == ord('m'):
                mouseIsOn = not mouseIsOn
        if event.type == MOUSEMOTION and mouseIsOn:
            # if the mouse moves, and mouse is enabled, move the player where the cursor is
            player.move_ip(event.pos[0] - player.centerx, event.pos[1] - player.centery)

    # adding new fruit
    fruitCounter += 1
    if fruitCounter >= NEWFRUIT:
        fruitCounter = 0
        newFruit = {"rect": pygame.Rect(random.randint(0 + WINDOWWIDTH / 50, WINDOWWIDTH - FRUITSIZE - WINDOWWIDTH / 50), random.randint(30, WINDOWHEIGHT * 0.6), FRUITSIZE, FRUITSIZE), "falling": False}
        fruits.append(newFruit)
 
    # draw windowSurface background image
    windowSurface.blit(bgrImg, bgrRect)

    # move the player
    if moveDown and player.bottom < WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top > 30:
        player.top -= MOVESPEED
    if moveLeft and player.left > 0:
        player.left -= MOVESPEED
    if moveRight and player.right < WINDOWWIDTH:
        player.right += MOVESPEED

    # draw the player onto the surface
    windowSurface.blit(playerStretchedImg, player)

    # check if the player has collided with any fruit.
    for fruit in fruits[:]:
        if player.colliderect(fruit["rect"]):
            fruits.remove(fruit)
            score += 1
            if soundIsOn:
                pickupSound.play()

    # check if fruit will start falling down
    for fruit in fruits:
        if random.randint(0, FRUIT_FALL_CHANCE) == 1:
            fruit["falling"] = True

    # moving down of falling fruit
    for fruit in fruits:
        if fruit["falling"]:
            fruit["rect"].top += FALLINGSPEED

    # delete fruit that have fallen to the ground
        for fruit in fruits[:]:
            if fruit['rect'].bottom > WINDOWHEIGHT:
                fruits.remove(fruit)
                fallen += 1
                if soundIsOn:
                    fallenSound.play()

    # draw the fruits
    for fruit in fruits:
        windowSurface.blit(fruitImg, fruit["rect"])

    # draw score and fallens
    scoreText = scoreFont.render('Total score: ' + str(score), True, WHITE, AZURE)
    scoreRect = scoreText.get_rect()
    scoreRect.left = 0
    scoreRect.top = 0
    fallenText = scoreFont.render('Fallen cherries: ' + str(fallen), True, WHITE, AZURE)
    fallenRect = fallenText.get_rect()
    fallenRect.right = WINDOWWIDTH
    fallenRect.top = 0
    windowSurface.blit(scoreText, scoreRect)
    windowSurface.blit(fallenText, fallenRect)

    # update the screen at the end of itineration
    pygame.display.update()
    mainClock.tick(FPS)