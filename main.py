import pygame, sys
from pygame import mixer
from pygame.locals import *
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
font = pygame.font.SysFont(None, 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
mainClock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
MARTIAL_SIZE = 200
MARTIAL_SCALE = 4
MARTIAL_OFFSET = [72, 75]
MARTIAL_DATA = [MARTIAL_SIZE, MARTIAL_SCALE, MARTIAL_OFFSET]
HUNTER_SIZE = 150
HUNTER_SCALE = 4.3
HUNTER_OFFSET = [72, 52]
HUNTER_DATA = [HUNTER_SIZE, HUNTER_SCALE, HUNTER_OFFSET]
NECRO_SIZE = 125
NECRO_SCALE = 4
NECRO_OFFSET = [72, 40]
NECRO_DATA = [NECRO_SIZE, NECRO_SCALE, NECRO_OFFSET]
HERO_SIZE = 180
HERO_SCALE = 3.6
HERO_OFFSET = [72, 60]
HERO_DATA = [HERO_SIZE, HERO_SCALE, HERO_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/pixel_art___does_not_think_by_vidreview_df88ngk-fullview.jpg").convert_alpha()
bg_menu = pygame.image.load("assets/images/background/Background Menu.jpeg").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
martial_sheet = pygame.image.load("assets\images\Martial Hero\Sprites\Merged_document__3_-removebg.png").convert_alpha()
hunter_sheet = pygame.image.load("assets\images\Huntress\Sprites\Merged_document__4_-removebg.png").convert_alpha()
necromancer_sheet = pygame.image.load("assets\images\Evil Wizard\Sprites\MergedImages (2).png").convert_alpha()
hero_sheet = pygame.image.load("assets\images\Hero Knight\MergedImages (1).png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
MARTIAL_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
HUNTER_ANIMATION_STEPS = [8, 8, 2, 4, 7, 3, 8]
NECROMANCER_ANIMATION_STEPS = [8, 8, 8, 8, 8, 4, 5]
HERO_ANIMATION_STEPS = [11, 8, 3, 7, 7, 4, 11]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def load_images(sprite_sheet, animation_steps, size, image_scale):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * size, y * size, size, size)
        temp_img_list.append(pygame.transform.scale(temp_img, (size * image_scale, size * image_scale)))
      animation_list.append(temp_img_list)
    return animation_list

def menu_select(warrior_sheet, wizard_sheet, x, y):
  warrior_photo = pygame.image.load("assets/images/warrior/Sprites/warrior.png")
  # image1 =  load_images(warrior_sheet, WARRIOR_ANIMATION_STEPS, WARRIOR_DATA[0], WARRIOR_DATA[1])[0][0]
  # img1 = pygame.transform.flip(warrior_photo)
  pygame.draw.rect(screen, RED, (x-2, y-2, 40, 60))
  screen.blit(warrior_photo, (x - (10 * 4), y - (10 * 4)))

  wizard_photo = pygame.image.load("assets/images/wizard/Sprites/wizard.png")
  # image2 =  load_images(warrior_sheet, WIZARD_ANIMATION_STEPS, WIZARD_DATA[0], WIZARD_DATA[1])[0][0]
  # img2 = pygame.transform.flip(wizard_photo)
  pygame.draw.rect(screen, RED, (x+60-2, y-2, 40, 60))
  screen.blit(wizard_photo, (x + 40 - (10 * 4), y - (10 * 4)))

#create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#game loop

def game(fighter_1, fighter_2, intro_count, last_count_update, round_over):
  run = True
  time = 5400
  while run:
    Refscore = score[0] + score[1]
    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    #time  
    if time // 3600 ==1:
      if time%3600 // 60 < 10:
        draw_text("Time: 01:0"+ str(time%3600 // 60), score_font, RED, 430, 20)  
      else:      
        draw_text("Time: 01:"+ str(time%3600 // 60), score_font, RED, 430, 20)
    else:
      if time%3600 // 60 < 10:
        draw_text("Time: 00:0"+ str(time%3600 // 60), score_font, RED, 430, 20)  
      else:      
        draw_text("Time: 00:"+ str(time%3600 // 60), score_font, RED, 430, 20)  
    time = time-1
    if time == 0:
       run = False

    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 920, 60)

    #update countdown
    if intro_count <= 0:
      #move fighters
      fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
      fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
      #display count timer
      draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update count timer
      if (pygame.time.get_ticks() - last_count_update) >= 1000:
        intro_count -= 1
        last_count_update = pygame.time.get_ticks()

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      #display victory image
      screen.blit(victory_img, (360, 150))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
    if score[0] + score[1] !=  Refscore:
       time = 5400
    #update display
    pygame.display.update()

def draw_textt(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu(fighter_1, fighter_2, intro_count, last_count_update, round_over):
    fighter = [None, None]

    while True:

        scaled_bg = pygame.transform.scale(bg_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
        draw_textt('Main Menu', score_font, (255,255,255), screen, 440, 40)
 
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(395, 100, 230, 50)
        button_2 = pygame.Rect(395, 180, 230, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                if fighter[0] == None:
                  game(fighter_1, fighter_2, intro_count, last_count_update, round_over)
                else:  
                  game(fighter[0], fighter[1], intro_count, last_count_update, round_over)

        if button_2.collidepoint((mx, my)):
            if click:
                options(intro_count, last_count_update, round_over) 

        pygame.draw.rect(screen, (255, 0, 0), button_1, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_2, width=4, border_radius=10)
 
        #writing text on top of button
        draw_textt('PLAY', score_font, (255,255,255), screen, 485, 105)
        draw_textt('SELECT PLAYER', score_font, (255,255,255), screen, 410, 185)

        draw_textt('Press ESC to quit!', score_font, (255,255,255), screen, 410, 555)



        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)

def options(intro_count, last_count_update, round_over):
    running = True
    step = 1
    fighter_1 = None
    fighter_2 = None
    while running:
        click = False
        
        scaled_bg = pygame.transform.scale(bg_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
        draw_textt('OPTIONS SCREEN', score_font, (255, 255, 255), screen, 400, 40)
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(395, 100, 200, 50)
        button_2 = pygame.Rect(395, 180, 200, 50)
        button_3 = pygame.Rect(395, 260, 200, 50)
        button_4 = pygame.Rect(395, 340, 200, 50)
        button_5 = pygame.Rect(395, 420, 200, 50)
        button_6 = pygame.Rect(395, 500, 200, 50)
        
        if step == 3:
            game(fighter_1, fighter_2, intro_count, last_count_update, round_over)
            running = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    print(click)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1
                fighter_2 = Fighter(2, 700, 310, True, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)  
              
              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)

        if button_2.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1                
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx) 

              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  

        if button_3.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1                
                fighter_2 = Fighter(2, 700, 310, True, MARTIAL_DATA, martial_sheet, MARTIAL_ANIMATION_STEPS, sword_fx) 

              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, MARTIAL_DATA, martial_sheet, MARTIAL_ANIMATION_STEPS, sword_fx)  

        if button_4.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1                
                fighter_2 = Fighter(2, 700, 310, True, HUNTER_DATA, hunter_sheet, HUNTER_ANIMATION_STEPS, sword_fx) 

              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, HUNTER_DATA, hunter_sheet, HUNTER_ANIMATION_STEPS, sword_fx)  
        
        if button_5.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1                
                fighter_2 = Fighter(2, 700, 310, True, NECRO_DATA, necromancer_sheet, NECROMANCER_ANIMATION_STEPS, magic_fx) 

              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, NECRO_DATA, necromancer_sheet, NECROMANCER_ANIMATION_STEPS, magic_fx)

        if button_6.collidepoint((mx, my)):
            if click:
              if step == 2:
                step = step + 1                
                fighter_2 = Fighter(2, 700, 310, True, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx) 

              if step == 1:
                step = step + 1
                fighter_1 = Fighter(1, 200, 310, False, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx)

        pygame.draw.rect(screen, (255, 0, 0), button_1, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_2, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_3, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_4, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_5, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), button_6, width=4, border_radius=10)

        #writing text on top of button
        draw_textt('WARRIOR', score_font, (255,255,255), screen, 450, 105)
        draw_textt('WIZARD', score_font, (255,255,255), screen, 450, 185)
        draw_textt('MARTIAL HERO', score_font, (255,255,255), screen, 410, 265)
        draw_textt('HUNTRESS', score_font, (255,255,255), screen, 430, 345)
        draw_textt('EVIL WIZARD', score_font, (255,255,255), screen, 420, 425)
        draw_textt('CYBERTRON', score_font, (255,255,255), screen, 430, 505)

        draw_textt('Press ESC to go back!', score_font, (255,255,255), screen, 380, 555)
       
        pygame.display.update()
        clock.tick(60)

main_menu(fighter_1, fighter_2, intro_count, last_count_update, round_over) 
#exit pygame
pygame.quit()