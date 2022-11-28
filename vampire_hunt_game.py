################################################################################################################################################
#
# Katya Fuck You Vinnie
#
# 6/12/20
#
# This is a game about a vampire trying to survive as many nights as (s)he can
# by eating humans/hunters
#
################################################################################################################################################

import pygame # pygame module
pygame.init() # start the program
from pygame import mixer # for music
import random # for random num. generator

############################################################### VARIABLES AND CONSTANTS ###################################################################

#set up clock to keep track of time
clock = pygame.time.Clock

FPS =  120 # fps for game

# by default, game doesn't start. will only start once player reads instructions and decides to proceed
gamePlaying = False

# is player in the instructions section of the main menu? this is necessary for the gui to work properly
howToPlay = False

# set the seconds variable to 0
seconds = 0

# opacity for all dark images - on default they are invisible, but as the night comes, they will slowly appear
opacity = 0 # opacity also determines whether it is day or night (once opacity is at 0, that means day - 255 means night)

# this is the opacity for the lose screen (when player loses, it will fade in)
loseScreenOpacity = 0

# is player in shade? by default, yes (game starts in the day time)
playerShade = True

# variable for player health ( 1-2, each increment rep. a heart)
playerHealth = 2 # player starts with 2 health

# when player loses, the value will change to true and trigger lose events
gameLost = False

# this is the amount of humans/hunters currently on screen
numberOfHumans = 0

# this will tell the program what type of human the person that spawns is (hunter or human) 1 - human, 2 - hunter
humanType = 0

# amount of humans that've been attacked by the player
humansBitten = 0

# night counter - counts number of nights
nightCounter = 0

# custom window caption
pygame.display.set_caption("Vampire Hunt Game - Fuck You Vinnie")

# COLOR CONSTANTS
BLACK = (0,0,0)
RED = (181, 30, 13)
WHITE = (255, 255, 255)

# constants for widths and heights of different objects
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 700

BEHIND_ITEMS = 550 # the point at which the player will be drawn behind items rather than in front

FLOOR_END = 530 # the point at which the sidewalk ends and the walls of the stores starts

EDGE_OF_SCREEN_PERCENT = .25 # this is the percentage at which the screen will start scrolling

SUN_DEATH = 200 # point at which the opacity has to be at to kill the player if they step out of the shade

################# font variables
pixelFont = pygame.font.Font("pixel_font.ttf", 30)

# set up the game window
gameWindow = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

###### MOVEMENT SPEEDS
playerSpeed = 8

moonSpeed = 4

sunSpeed = 8

humanSpeed = playerSpeed - 2

opacitySpeed = 4 # this is how fast the opacity will change

#################################################### LOADING IMAGES AND GETTING THEIR DIMENSIONS/COLLISION RECTANGLES ############################################################
### these are the day versions of all the images (to be drawn first) and also of the images that won't be affected by the changing day/night cycle

##### player sprite

#load the character sprite
playerImageR = pygame.image.load("player.png")
# flip player image horizontally to create an image for each direction
playerImageL = pygame.transform.flip(playerImageR, True, False) # flip image to show player facing left

# get the player sprite image's rectangle
playerRect = playerImageR.get_rect
# p. sprite image width
playerW = playerImageR.get_rect().width
# p. sprite image height
playerH = playerImageR.get_rect().height

# player direction variable (this has to be preceded by the loading of the player images)
playerDirection = playerImageR ### this is the direction the character is facing on startup

RIGHT = playerImageR ## RIGHT uses the image of the sprite facing right
LEFT = playerImageL ## LEFT uses the image of the sprite facing left

######### human sprite

# load the normal human sprite
normalImageR = pygame.image.load("human.png")
normalImageL = pygame.transform.flip(normalImageR, True, False) # flip image to show human facing left

# load hunter sprite
hunterImageR = pygame.image.load("hunter.png")
hunterImageL = pygame.transform.flip(hunterImageR, True, False) # flip image to show hunter facing left

# load dead human sprite
deadNormalImageR = pygame.image.load("dead_human.png")
deadNormalImageL = pygame.transform.flip(deadNormalImageR, True, False) # flip image to show human facing left

# load dead hunter sprite
deadHunterImageR = pygame.image.load("dead_hunter.png")
deadHunterImageL = pygame.transform.flip(deadHunterImageR, True, False) # flip image to show human facing left

# these will be shared by both varieties of human (hunter and human) since the images are the same size
# get the human sprite image's rectangle
humanRect = normalImageR.get_rect
# p. sprite image width
humanW = normalImageR.get_rect().width
# p. sprite image height
humanH = normalImageR.get_rect().height

NORMAL_RIGHT = normalImageR ## RIGHT uses the image of the sprite facing right
NORMAL_LEFT = normalImageL ## LEFT uses the image of the sprite facing left

HUNTER_RIGHT = hunterImageR # this is the image of the hunter facing right
HUNTER_LEFT = hunterImageL # this is the image of the hunter facing right

# dead images
DEAD_NORMAL_RIGHT = deadNormalImageR
DEAD_NORMAL_LEFT = deadNormalImageL

DEAD_HUNTER_RIGHT = deadHunterImageR
DEAD_HUNTER_LEFT = deadHunterImageL

# human direction variable
humanDirection = 0 ### i just need to create a 'blank' variable for the direction of the human

backdropImage = pygame.image.load("backdrop.png") # load image for buildings/sidewalk

skyImage = pygame.image.load("sky.png") # load image for sky

streetItemsImage = pygame.image.load("street_items.png") # load the image for the items on the street - player can walk behind these

# load the sun
sunImage = pygame.image.load("sun.png")
#sun image width
sunW = sunImage.get_rect().width

# load the moon
moonImage = pygame.image.load("moon.png")
# moon image width
moonW = moonImage.get_rect().width

# load the heart image
heartImage = pygame.image.load("heart.png")

### loading gui images
mainMenuGUI = pygame.image.load("main_menu.png")
howToPlayGUI = pygame.image.load("how_to_play.png")

### collisions for menu buttons
playButton = pygame.Rect(347, 186, 506, 124)
howToPlayButton = pygame.Rect(347, 350, 506, 124)
exitButton = pygame.Rect(347, 514, 506, 124)
backButton = pygame.Rect (455, 576, 290, 71)

# loading lose screen
loseScreen = pygame.image.load("lose_screen.png").convert()

################## LOADING NIGHT VERSIONS OF IMAGES
###(im converting these darker images to a form that can have their opacity changed so it can fade in as the night comes)

backdropNightImage = pygame.image.load("backdrop_night.png").convert() # load night image for buildings/sidewalk

skyNightImage = pygame.image.load("sky_night.png").convert() # load night image for sky

streetItemsNightImage = pygame.image.load("street_items_night.png").convert()

#using a color key to remove the background from the clouds lets python see the transparent pixels as transparent and doesn't ruin the background-- python doesn't recongnize png transparent pixels properly
streetItemsNightImage.set_colorkey(BLACK)
backdropNightImage.set_colorkey(BLACK)

################### X AND Y POS OF DIFFERENT IMAGES ####################

playerX = 350 # since the game starts in the day time, it's important the player spawns in some shade upon startup
playerY = 480

humanX = 0
humanY = 0

backdropX = 0 # this will be shared by a lot of the background images and menu items
skyX = 0

BACKGROUND_Y = 0 # y constant is shared by sky and backdrop

# this is where the sun will be upon startup
sunX = DISPLAY_WIDTH/2
sunY = 0 - 50
# this is where the moon will be upon startup
moonX = sunSpeed * DISPLAY_WIDTH * -1 # this equation for the moon's position will make sure the sun and moon dont move out of sync, even at different speeds
moonY = 0 - 50

####### dimensions of certain images (to set up collisions)
BIG_TREE_WIDTH = 59
SMALL_TREE_WIDTH = 26
TRASH_WIDTH = 27
PARKING_METER_WIDTH = 10
FIRE_HYDRANT_WIDTH = 27
NEWS_HOLDERS_WIDTH = 66

ITEM_HEIGHT = 10
ITEMS_Y = 552

# background width
BACKGROUND_IMAGE_WIDTH = 1450

SHADE_WIDTH = 125 # this is how wide the collision rectangles for the shade are
SHADE_HEIGHT = 64 # height for shade col. rects
SHADE_OFFSET = 54 # this is how many pixels offset the shade is from the already existing collisions is

#################font variables
pixelFontLargeText = pygame.font.Font("pixel_font.ttf", 100)
pixelFontSmallText = pygame.font.Font("pixel_font.ttf", 75)
pixelFontTinyText = pygame.font.Font("pixel_font.ttf", 30)


############### MUSIC AND SOUND EFFECTS
##play background music
pygame.mixer.music.load("dracula_chiptune.mp3")
pygame.mixer.music.set_volume(0.1) ### sets the volume of the music
pygame.mixer.music.play(-1) ### -1 means that the music will play again once its done

# LOAD SOUND FX
biteSound = pygame.mixer.Sound("hit_sound.wav")
pygame.mixer.Sound.set_volume(biteSound, 0.2)
menuNavigateSound = pygame.mixer.Sound("menu_navigate.wav")
pygame.mixer.Sound.set_volume(menuNavigateSound, .1)

#### CREATING LISTS
# when a human is bitten, their position and type will be added to these lists so a dead human can be drawn
deadHumansXPos = []
deadHumansYPos = []
deadHumanTypeAndDirection = []


# list of all the widths and x positions (in order) of the street items
streetItemsWidth = [SMALL_TREE_WIDTH, PARKING_METER_WIDTH, NEWS_HOLDERS_WIDTH, BIG_TREE_WIDTH, PARKING_METER_WIDTH, FIRE_HYDRANT_WIDTH, TRASH_WIDTH, PARKING_METER_WIDTH, SMALL_TREE_WIDTH, PARKING_METER_WIDTH, BIG_TREE_WIDTH]
streetItemsXPos = [69, 179, 242, 383, 557, 693, 880, 912, 998, 1256, 1323]

##################### FILLING LISTS ##########################

shadeRectangles = []
for i in streetItemsXPos:
    shadeRectangles.append(pygame.Rect(streetItemsXPos[0] - SHADE_OFFSET, ITEMS_Y, SHADE_WIDTH,
                                       SHADE_HEIGHT))  # it's important to tie most of the collisions with the same
    shadeRectangles.append(pygame.Rect(streetItemsXPos[3] - SHADE_OFFSET, ITEMS_Y, SHADE_WIDTH,
                                       SHADE_HEIGHT))  # x position as moving one point is easier than moving many for the
    shadeRectangles.append(
        pygame.Rect(streetItemsXPos[8] - SHADE_OFFSET, ITEMS_Y, SHADE_WIDTH, SHADE_HEIGHT))  # program
    shadeRectangles.append(pygame.Rect(streetItemsXPos[10] - SHADE_OFFSET, ITEMS_Y, SHADE_WIDTH, SHADE_HEIGHT))


############## FUNCTIONS ################
def sideScrollRight(): #this function will make an edge scrolling feature, moving all objects in correspondence with the edge scrolling (right)
    #####SIDE SCROLLING TO THE RIGHT (EVERYTHING MOVES TO THE LEFT)######
    global backdropX, streetItemsXPos, humanX

    backdropX -= playerSpeed # move background to the left when scrolling right
    humanX -= playerSpeed # scroll the human

    for i in range (0, 11):
        streetItemsXPos[i] -= playerSpeed

    for i in range (0, humansBitten): # move the dead bodies
        deadHumansXPos[i] -= playerSpeed

def sideScrollLeft(): ##this function will make an edge scrolling feature, moving all objects in correspondence with the edge scrolling (left)
    #####SIDE SCROLLING TO THE LEFT (EVERYTHING MOVES TO THE RIGHT)######
    global backdropX, streetItemsXPos, humanX

    backdropX += playerSpeed # move background to the right when scrolling left
    humanX += playerSpeed # scroll the human

    for i in range (0, 11):
        streetItemsXPos[i] += playerSpeed

    for i in range (0, humansBitten): # move the dead bodies
        deadHumansXPos[i] += playerSpeed

def collisionBottomEdge():
    for i in streetItemsBottomEdge:
        # if the player is touching the bottom edge of any of the street items or stores, return true
        if playerRect.colliderect(i) or playerY + playerH <= FLOOR_END:
            return True

def collisionTopEdge():
    for i in streetItemsTopEdge:
        # if the player is touching the top edge of any of the street items, return true
        if playerRect.colliderect(i):
            return True

def inShade():
    for i in shadeRectangles:
        # if the player is in the shade,
        if playerRect.colliderect(i):
            return True

def biteHuman(): # function to take out a human/hunter when player "bites" it
    global numberOfHumans, playerHealth, humansBitten

    pygame.mixer.Sound.play(biteSound) # play bite sound effect
    numberOfHumans = 0 # reset number of humans back to zero to enable another to spawn
    if humanType == 2: # if human type is a hunter
        hurtPlayer = random.randint(1,2) # 50% chance the hunter will hurt the player
        if hurtPlayer == 1:
            playerHealth += 1

        else:
            playerHealth -=1

    else: # if human type is a normal
        playerHealth += 1

    humansBitten += 1

def drawHealth(): # draw hearts according to amount of health player has
    global gameLost, playerHealth
    if playerHealth == 0: # game over when player's health reaches 0
        gameLost = True

    elif playerHealth == 1:
        gameWindow.blit(heartImage, (1121, 9)) # blit first heart

    elif playerHealth == 2:
        gameWindow.blit(heartImage, (1121, 9)) # blit first heart
        gameWindow.blit(heartImage, (1066, 9)) # blit second heart

    if playerHealth >= 2:
        playerHealth = 2 # make sure player health can never surpass 2

def createHuman(): # create a human at night
    global numberOfHumans, humanX, humanY, humanH, humanW, humanDirection, humanType

    humanType = random.randint(1,2) # come up with a random num. to determine type of human that spawns

    humanY = random.randint(580, 680) - humanH # generate a random y starting pos for the human (within boundaries)
    humanX = random.randint(1,2) # decide whether human comes from the right or left side of display

    if humanX == 1:
        if humanType == 1: # if the type of human is a human:
            humanDirection = NORMAL_LEFT # show image for human
        else: # if the type of human is a hunter:
            humanDirection = HUNTER_LEFT # show image for hunter

        humanX = DISPLAY_WIDTH + humanW  # human X will be on right side

### HUMAN WILL ALWAYS SPAWN WITHIN DISPLAY BOUNDARY - WILL NEVER SPAWN IN A PLACE THE PLAYER CAN'T SEE
    else:
        if humanType == 1:  # if the type of human is a human:
            humanDirection = NORMAL_RIGHT  # show image for human
        else:  # if the type of human is a hunter:
            humanDirection = HUNTER_RIGHT  # show image for hunter

        humanX = 0 - humanW  # human x will be on the left side

    numberOfHumans = 1  # set number of humans to 1 so program stops generating random integers


def listDeadHumans(): # when a human is bitten, add its positioning and type to lists (so dead human can be drawn)
    global humanX, humanY, humanDirection, deadHumansXPos, deadHumansYPos, deadHumanTypeAndDirection

    if humanDirection == NORMAL_RIGHT: # convert images of live humans to dead humans
        humanDirection = DEAD_NORMAL_RIGHT

    if humanDirection == NORMAL_LEFT:
        humanDirection = DEAD_NORMAL_LEFT

    if humanDirection == HUNTER_RIGHT:
        humanDirection = DEAD_HUNTER_RIGHT

    if humanDirection == HUNTER_LEFT:
        humanDirection = DEAD_HUNTER_LEFT

    for i in range(0,1): # add x pos to list of dead human x positions
        deadHumansXPos.append(humanX)

    for i in range(0,1): # add y pos to list of dead human y pos
        deadHumansYPos.append(humanY + humanH/2)

    for i in range(0,1): # add type to list of dead human types (image to blit)
        deadHumanTypeAndDirection.append(humanDirection)

# these next few functions decide what order to draw the street items, human, dead bodies, and player in
# there are three scenarios: either the human is behind everything, in between the street items and the one human on screen
# or the player is in front of everything

def drawPlayerFront(): # draw player in front of everything
    global playerX, playerY, playerDirection, humanX, humanY, humanDirection

    gameWindow.blit(streetItemsImage, (backdropX, BACKGROUND_Y))# draw street items
    gameWindow.blit(streetItemsNightImage, (backdropX, BACKGROUND_Y))# draw night version of street items

    for i in range(0,humansBitten): # draw dead humans (humans bitten keeps track of amt of dead humans)
        gameWindow.blit(deadHumanTypeAndDirection[i], (deadHumansXPos[i], deadHumansYPos[i]))

    if numberOfHumans >= 1: # draw human (only if there is a human on screen)
        gameWindow.blit(humanDirection, (humanX, humanY))

    gameWindow.blit(playerDirection, (playerX, playerY)) # draw player


def drawPlayerMiddle(): # player is in between human and street items
    global playerX, playerY, playerDirection, humanX, humanY, humanDirection

    gameWindow.blit(streetItemsImage, (backdropX, BACKGROUND_Y))# draw street items
    gameWindow.blit(streetItemsNightImage, (backdropX, BACKGROUND_Y))# draw night version of street items

    for i in range(0, humansBitten):
        gameWindow.blit(deadHumanTypeAndDirection[i], (deadHumansXPos[i], deadHumansYPos[i]))

    gameWindow.blit(playerDirection, (playerX, playerY))# draw player

    if numberOfHumans >= 1:
        gameWindow.blit(humanDirection, (humanX, humanY))

def drawPlayerBehind(): # player is behind everything
    global playerX, playerY, playerDirection, humanX, humanY, humanDirection

    gameWindow.blit(playerDirection, (playerX, playerY))# draw player

    gameWindow.blit(streetItemsImage, (backdropX, BACKGROUND_Y)) # draw street items
    gameWindow.blit(streetItemsNightImage, (backdropX, BACKGROUND_Y)) # draw night version of street items

    for i in range(0, humansBitten):
        gameWindow.blit(deadHumanTypeAndDirection[i], (deadHumansXPos[i], deadHumansYPos[i]))

    if numberOfHumans >= 1:
        gameWindow.blit(humanDirection, (humanX, humanY))

playGame = True # control the game loop

################ GAME LOOP ####################
while playGame == True:
    nightsSurvived = nightCounter - 1 # this variable has to be in the loop since the nightCounter variable is always changing
    if nightsSurvived <= 0:
        nightsSurvived = 0 # make sure number of nights survived can never be a negative number
    # clock tick
    pygame.time.Clock().tick(60)

    numberOfImagesToBlit = 3 + numberOfHumans + humansBitten # variable to store amt of tuples in list of items to render
    ############################ TEXT VARIBLES ##############################
    loseMessage = pixelFontLargeText.render("Game Over", True, RED)

    nightCounterText = pixelFontLargeText.render("NIGHT " + str(nightCounter), True, RED)

    nightsSurvivedText = pixelFontSmallText.render("You survived: " + str(nightsSurvived) + " nights", True, RED)

    humansBittenText = pixelFontSmallText.render ("You bit: " + str(humansBitten) + " humans", True, RED)

    hungryText = pixelFontTinyText.render ("You're getting hungry...", True, RED)

    ############################# GETTING EVENTS #############################
    # get pygame events
    events = pygame.event.get()

    # get keypress events
    keys = pygame.key.get_pressed()

    # get mouse press events
    pygame.mouse.get_pressed()

##################### MAIN MENU SECTION ####################
    if gamePlaying == False: # main menu will start on default
        if howToPlay == False: #when the how to play menu is closed, the main menu will appear
            gameWindow.blit(mainMenuGUI, (backdropX, BACKGROUND_Y))

        else: # otherwise,  the game instructions will show (this is a boolean value since there's only two menus to really pick from)
            gameWindow.blit(howToPlayGUI, (backdropX, BACKGROUND_Y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close game if exit button is pressed
                playGame = False
                break
            # this block is executed once for each MOUSEBUTTONDOWN event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right
                if event.button == 1:
                    # 'event.pos' is the mouse pointer's current position
                    if playButton.collidepoint(event.pos) and howToPlay == False: # making sure howToPlay is false makes sure the user can't use any of the buttons
                        gamePlaying = True                                        # in the main menu while they're in the instructions menu

                    elif exitButton.collidepoint(event.pos) and howToPlay == False: # exit game if user presses exit button
                        playGame = False
                        break

                    elif howToPlayButton.collidepoint(event.pos): # if user presses 'how to play' button, show instructions
                        howToPlay = True

                    elif backButton.collidepoint(event.pos) and howToPlay == True:  # if user is on the instructions screen and presses the back button, take user back to main menu
                        howToPlay = False
                        gameWindow.blit(mainMenuGUI, (backdropX, BACKGROUND_Y))
                pygame.mixer.Sound.play(menuNavigateSound)  # play a menu navigation sound

        if keys[pygame.K_ESCAPE]:  # when the player presses the escape key:
            playGame = False  # stop the while loop
            break  # stop the program

    #################### PLAYING THE GAME ###################

    else: # this is for every instance where the player is not in the main menu (playing the actual game)

    ##################### CREATING LISTS AND COLLISIONS FOR MOVING OBJECTs
        streetItemsBottomEdge = []
        for i in range(0, 11):  # this list keeps track of the bottom edges of all the street items
            streetItemsBottomEdge.append(
                pygame.Rect(pygame.Rect(streetItemsXPos[i], ITEMS_Y + ITEM_HEIGHT, streetItemsWidth[i], ITEM_HEIGHT/2)))

        streetItemsTopEdge = []
        for i in range (0, 11): # this list keeps track of all the top edges of the street items
            streetItemsTopEdge.append(pygame.Rect(pygame.Rect(streetItemsXPos[i], ITEMS_Y, streetItemsWidth[i], ITEM_HEIGHT/2)))

        ######## it would be unnecessary to create side boundaries for all the street objects as it would limit player movement and the player will always be either in front of or
        ######## behind an item on the street anyways

        ### boundary collision rectangle for player
        playerRect = pygame.Rect(playerX, playerY + playerH, playerW, playerH / 2)

        #### bite collision rectangle for player
        playerBiteRect = pygame.Rect(playerX, playerY, playerW, playerH)

        # the player has two different col. rects because the boundary rectangle only counts the bottom half of the player ( i think it makes the game look nicer)
        # while the bite rectangle counts the whole player's rectangle

    ### collision rectangle for the human
        humanRect = pygame.Rect(humanX, humanY, humanW, humanH)

    ################################################### USER'S INPUT ####################################################
        if gameLost == False: # only let player move if the game hasnt been lost
            if keys[pygame.K_RIGHT]:  #### when the player presses the right arrow key:
                if DISPLAY_WIDTH - playerX <= EDGE_OF_SCREEN_PERCENT * DISPLAY_WIDTH:  ## if characterX is at around 75% of screen......
                    if backdropX >= BACKGROUND_IMAGE_WIDTH * -1 + DISPLAY_WIDTH:  ### only scroll the screen if there is background to scroll
                        sideScrollRight()
                    elif playerX <= DISPLAY_WIDTH - playerW:  ###only let character move right if not at the right side boundary of the screen
                        playerX += playerSpeed
                        playerDirection = RIGHT
                else:  ### if not edge scrolling or touching the boundaries, let character move as normal
                    playerX += playerSpeed
                    playerDirection = RIGHT

            if keys[pygame.K_LEFT]:  # when the player presses the left arrow key:
                if playerX <= EDGE_OF_SCREEN_PERCENT * DISPLAY_WIDTH:  ## if characterX is at around 25% of screen......
                    if backdropX <= 0:  # only scroll if character has scrolled some to the right, and needs to go back
                        sideScrollLeft()
                    elif playerX >= 0:  ###only let character move right if not at the right side boundary of the screen
                        playerX -= playerSpeed
                        playerDirection = LEFT
                else:  # if not edge scrolling or touching the boundaries, let character move as normal
                    playerX -= playerSpeed
                    playerDirection = LEFT


            if keys[pygame.K_DOWN]:  # when the player presses the down arrow key:
                if not collisionTopEdge() and not playerY >= DISPLAY_HEIGHT - playerH: # if player isn't colliding with the top edge of anything and not at the bottom screen boundaries, walk like normal
                    playerY += playerSpeed

            if keys[pygame.K_UP]:  # when the player presses the up arrow key:
                if not collisionBottomEdge(): # if player isn't colliding with the bottom edge of anything, walk like normal
                    playerY -= playerSpeed

            if keys[pygame.K_SPACE]: # when the player presses the space bar:
                if playerBiteRect.colliderect(humanRect): # only carry out functions if player is actually in contact with another human
                    biteHuman()
                    listDeadHumans()

        inShade() # check if player is in shade

        if keys[pygame.K_ESCAPE]:  # when the player presses the escape key:
            playGame = False  # stop the while loop
            break  # stop the program

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close game if exit button is pressed
                playGame = False
                break

        ############# DAY/NIGHT CYCLE
        # move the sun
        sunX += sunSpeed

        # move the moon
        moonX += moonSpeed

        # this will make the screen darker as the day comes to an end
        if sunX >= DISPLAY_WIDTH - (255 * sunSpeed)/opacitySpeed:
            opacity += opacitySpeed

        # this will make the screen lighter as the night comes to an end
        elif moonX >= DISPLAY_WIDTH - (255 * moonSpeed)/opacitySpeed:
            opacity -= opacitySpeed

        # when the sun leaves the screen boundaries...
        if sunX >= DISPLAY_WIDTH:
            moonX = moonW * -1
            sunX = sunSpeed * DISPLAY_WIDTH * -1 # move sun back to the start

        # when the moon leaves the screen boundaries...
        elif moonX >= DISPLAY_WIDTH:
            sunX = sunW * -1
            moonX = moonSpeed * DISPLAY_WIDTH * -1 # move moon back to start

        ###### MAKING A HUMAN ON SCREEN
        if numberOfHumans == 0 and opacity >= 255:
            createHuman()

        #### MOVING THE HUMAN
        if humanDirection == NORMAL_RIGHT or humanDirection == HUNTER_RIGHT:
            humanX += humanSpeed
            # turn human opposite direction if it hits right side of screen
            if opacity >= 255: # (only at night, during day, human will walk off screen)
                if humanX + playerW >= DISPLAY_WIDTH:
                    if humanDirection == HUNTER_RIGHT:
                        humanDirection = HUNTER_LEFT
                    elif humanDirection == NORMAL_RIGHT:
                        humanDirection = NORMAL_LEFT

        elif humanDirection == HUNTER_LEFT or humanDirection == NORMAL_LEFT:
            humanX -= humanSpeed
            # turn human opposite direction if it hits left side of screen (only at night, during day, human will walk off screen)
            if opacity >= 255:  # (only at night, during day, human will walk off screen)
                if humanX <= 0:
                    if humanDirection == HUNTER_LEFT:
                        humanDirection = HUNTER_RIGHT
                    elif humanDirection == NORMAL_LEFT:
                        humanDirection = NORMAL_RIGHT

        if opacity < 255:
            if humanX >= DISPLAY_WIDTH or humanX <= 0:
                numberOfHumans = 0 # delete human once they walk off the screen (only during the day)


        # night/day cycle related health changes
        if opacity <= SUN_DEATH and not inShade(): # if player isn't in shade when sun comes out
            playerHealth = 0   # player dies

        if moonX == DISPLAY_WIDTH/2 + 1: # when the moon hits half the screen... (i added the +1 because the moonX skips over even numbers, and i only wanted the player to lose ONE heart)
            playerHealth -= 1 # player loses a heart
            pygame.mixer.Sound.play(menuNavigateSound) # play a little 'beep' sound to alert player to new message


    #################################################### DRAWING IMAGES #################################################

        # draw the sky
        gameWindow.blit(skyImage, (skyX, BACKGROUND_Y))
        gameWindow.blit(skyNightImage, (skyX, BACKGROUND_Y))

        # draw the sun
        gameWindow.blit(sunImage, (sunX, sunY))

        # draw the moon
        gameWindow.blit(moonImage, (moonX, moonY))

        # draw the backdrop (buildings and sidewalk in front of sky)
        gameWindow.blit(backdropImage, (backdropX, BACKGROUND_Y))
        gameWindow.blit(backdropNightImage, (backdropX, BACKGROUND_Y))

    # initially, to make the player move in and around the different objects, i made a list of tuples
    # but unfortunately, pygame doesn't actually change tuple values once they're in a list, so nothing would move
    # this inefficient system will have to do :D
        if playerY + playerH <= BEHIND_ITEMS: # if player is behind the street items (visually, on the sidewalk)
            drawPlayerBehind()

        else: # if player is in front of street items
            if playerY + playerH <= humanY + playerH: # draw player behind human and in front of street items if player's y is lower than human's y
                drawPlayerMiddle()
            else: # draw player in front of everything, otherwise
                drawPlayerFront()

        # set opacity of night images
        skyNightImage.set_alpha(opacity)
        backdropNightImage.set_alpha(opacity)
        streetItemsNightImage.set_alpha(opacity)

        # draw the health based on health variable
        drawHealth()

        # night counter
        if sunX > moonX: # only do this as the sun is setting
            if opacity >= SUN_DEATH and opacity <= 255:
                if opacity == SUN_DEATH: # SUN_DEATH is one specific number i know opacity will hit only ONCE, so night counter will only increase ONCE
                    nightCounter = nightCounter + 1 # make sure to add one 'night' to the counter!
                else:
                    gameWindow.blit(nightCounterText, (403, 286)) # blit text

            print nightCounter # debug

        if moonX > DISPLAY_WIDTH/2 and moonX < DISPLAY_WIDTH/2 + moonSpeed * 30: # this shows a sort of 'window' when the message will be blit
            gameWindow.blit(hungryText, (437, 43)) # draw text to tell player they're getting hungry (when player loses a heart)

        ################## LOSE CONDITIONS
        if gameLost == True: # player loses game when health = 0
            # lose screen fades in
            loseScreen.set_alpha(loseScreenOpacity)
            loseScreenOpacity += 25
            # blit lose screen along with amnt of nights survived and number of humans bitten (invisible until player loses)
            gameWindow.blit(loseScreen, (0, BACKGROUND_Y))
            gameWindow.blit(nightsSurvivedText, (207, 332))
            gameWindow.blit(humansBittenText, (253, 442))
    pygame.display.update()