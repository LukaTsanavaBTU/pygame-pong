import pygame, os, random
import pygame.math as math
from pygame.locals import *
pygame.init()
pygame.font.init()

#Constant Variables
SCREEN_SIZE = (1200, 800)
FPS = 60
PLAYER_SIZE = (25,200)
PLAYER_VEL = 20
AI_VEL = 5
BALL_RADIUS = 20
BALL_DEVIATION = 10
BALL_X_VEL = 30
TEXT_FONT = pygame.font.Font(os.path.join("data","OldSchoolAdventures-42j9.ttf"), 20)
MENU_FONT = pygame.font.Font(os.path.join("data","OldSchoolAdventures-42j9.ttf"), 100)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (77,166,255)
RED = (255,64,25)
GREY = (132,132,130)

#Dynamic Variables
player_1_y =  SCREEN_SIZE[1]/2 - PLAYER_SIZE[1]/2
player_2_y =  SCREEN_SIZE[1]/2 - PLAYER_SIZE[1]/2
ball_center = [SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2]
ball_vel= [BALL_X_VEL, random.randint(-BALL_DEVIATION,BALL_DEVIATION)]
player_1_score = 0
player_2_score = 0

#Player Rectangles
player_1 = pygame.Rect(25,player_1_y,PLAYER_SIZE[0], PLAYER_SIZE[1])
player_2 = pygame.Rect(SCREEN_SIZE[0] - 50, player_2_y, PLAYER_SIZE[0], PLAYER_SIZE[1])

#Ball
ball_vector = math.Vector2(ball_center[0],ball_center[1])
ball_rect = pygame.Rect(ball_vector.x, ball_vector.y, BALL_RADIUS*2, BALL_RADIUS*2)

#Sounds
bleep_1 = pygame.mixer.Sound(os.path.join("data","bleep1.mp3"))
bleep_2 = pygame.mixer.Sound(os.path.join("data","bleep2.mp3"))
game_won = pygame.mixer.Sound(os.path.join("data","gamewon.mp3"))
game_over = pygame.mixer.Sound(os.path.join("data","gameover.mp3"))

#Screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pong")
pygame.display.set_icon(pygame.image.load(os.path.join("data","pong.ico")))

#Main Menu Function
in_menu = True
def main_menu():
    global in_menu, running
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_menu = False

        screen.fill(BLACK)
        title_text = MENU_FONT.render("PONG", True, GREY)
        start_button_text = TEXT_FONT.render("PRESS ENTER TO START", True, WHITE)
        start_button_text_2 = TEXT_FONT.render("PRESS Q AT ANY POINT TO QUIT", True, WHITE)
        screen.blit(title_text, (SCREEN_SIZE[0] / 2 - 200, 40))
        screen.blit(start_button_text, (SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2))
        screen.blit(start_button_text_2, (SCREEN_SIZE[0] / 2 - 200, SCREEN_SIZE[1] / 2 +30))
        pygame.display.flip()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RETURN]:
            in_menu = False
        if keys_pressed[pygame.K_q]:
            running = False
            in_menu = False


#Main Loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Main Menu
    main_menu()

    #Draw Surfaces
    #Fill Screen
    screen.fill(BLACK)
    #Lines
    pygame.draw.line(screen, GREY, (SCREEN_SIZE[0]/2, 0), (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]), 20)
    pygame.draw.line(screen, GREY, (0, 0), (SCREEN_SIZE[0],0), 20)
    pygame.draw.line(screen, GREY, (0, SCREEN_SIZE[1]), (SCREEN_SIZE[0], SCREEN_SIZE[1]), 20)
    pygame.draw.line(screen, GREY, (SCREEN_SIZE[0] / 2, 0), (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1]), 20)
    pygame.draw.line(screen, GREY, (SCREEN_SIZE[0] / 2, 0), (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1]), 20)
    #Score
    player_1_score_text = TEXT_FONT.render("Player 1: " + str(player_1_score),True, WHITE)
    player_2_score_text = TEXT_FONT.render("Player 2: " + str(player_2_score),True, WHITE)
    screen.blit(player_1_score_text,(SCREEN_SIZE[0]/4-70,SCREEN_SIZE[1] - 35))
    screen.blit(player_2_score_text,(SCREEN_SIZE[0]/4*3-70,SCREEN_SIZE[1] - 35))
    #Players
    pygame.draw.rect(screen, RED, player_1)
    pygame.draw.rect(screen, BLUE, player_2)
    #The Ball
    #Drawing
    pygame.draw.circle(screen, WHITE, ball_vector.xy, BALL_RADIUS)
    #pygame.draw.rect(screen, WHITE, ball_rect)
    #Ball Movement
    ball_vector.x += ball_vel[0]
    ball_vector.y += ball_vel[1]
    ball_rect.x = ball_vector.x - BALL_RADIUS
    ball_rect.y = ball_vector.y - BALL_RADIUS
    if player_1.colliderect(ball_rect):
        ball_vel[0] *= -1
        ball_vel[1] = random.randint(-BALL_DEVIATION,BALL_DEVIATION)
        pygame.mixer.Sound.play(bleep_1)
    if player_2.colliderect(ball_rect):
        ball_vel[0] *= -1
        ball_vel[1] = random.randint(-BALL_DEVIATION, BALL_DEVIATION)
        pygame.mixer.Sound.play(bleep_2)
    if ball_vector.x - BALL_RADIUS < 25:
        player_2_score += 1
        ball_vector.x = ball_center[0]
        ball_vector.y =  ball_center[1]
        player_1.y = player_1_y
        player_2.y = player_2_y
        ball_vel[0] = BALL_X_VEL
        pygame.mixer.Sound.play(game_over)
        pygame.time.delay(2000)
    if ball_vector.x + BALL_RADIUS > SCREEN_SIZE[0] - 25:
        player_1_score += 1
        ball_vector.x = ball_center[0]
        ball_vector.y = ball_center[1]
        player_1.y = player_1_y
        player_2.y = player_2_y
        ball_vel[0] = BALL_X_VEL
        pygame.mixer.Sound.play(game_won)
        pygame.time.delay(2000)
    if ball_vector.y - BALL_RADIUS < 0 or ball_vector.y + BALL_RADIUS > SCREEN_SIZE[1]:
        ball_vel[1] *= -1






    #Movement
    keys_pressed = pygame.key.get_pressed()
    #Player I
    if keys_pressed[pygame.K_w] and player_1.y > 0:
        player_1.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s] and player_1.y + PLAYER_SIZE[1] < SCREEN_SIZE[1]:
        player_1.y += PLAYER_VEL
    #Quitting
    if keys_pressed[pygame.K_q]:
        running = False

    #AI
    if ball_vector.y > player_2.y + PLAYER_SIZE[1]/2 and player_2.y + PLAYER_SIZE[1] < SCREEN_SIZE[1]:
        player_2.y += AI_VEL
    if ball_vector.y < player_2.y + PLAYER_SIZE[1]/2 and player_2.y > 0:
        player_2.y -= AI_VEL




    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



#Player II
    #if keys_pressed[pygame.K_UP] and player_2.y > 0:
        #player_2.y -= PLAYER_VEL
    #if keys_pressed[pygame.K_DOWN] and player_2.y + PLAYER_SIZE[1] < SCREEN_SIZE[0]:
       #player_2.y += PLAYER_VEL