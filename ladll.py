import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Las aventuras de Luisa Longaniza')



#define font
font = pygame.font.Font('VT323-Regular.ttf', 30)
font_score = pygame.font.Font('VT323-Regular.ttf', 30)

font2 = pygame.font.Font('VT323-Regular.ttf', 50)

font3 = pygame.font.Font('Network_Font.ttf', 50)
#define game variables
tile_size = 50
game_over = 0
main_menu = True
creditos = False
max_levels = 45
score = 0


#define colours
white = (255, 255, 255)
blue = (0, 0, 255)
grey = (0, 0, 0)

#load images

bg_img = pygame.image.load('img/sky.png')
bg_img2 = pygame.image.load('img/sky2.png')
bg_img3 = pygame.image.load('img/sky3.png')
bg_img4 = pygame.image.load('img/sky4.png')
bg_img5 = pygame.image.load('img/sky5.png')
bg_img6 = pygame.image.load('img/sky6.png')
bg_img7 = pygame.image.load('img/sky7.png')
bg_img8 = pygame.image.load('img/sky8.png')
franco = pygame.image.load('img/guya1.png')
franco = pygame.transform.scale(franco, (40, 80))
francof = pygame.transform.flip(franco, True, False)
ramon = pygame.image.load('img/ramon.png')
ramon = pygame.transform.scale(ramon, (40, 80))

restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
credits_img = pygame.image.load('img/credits_btn.png')
logo_img = pygame.image.load('img/logo_btn.png')

#load sounds


coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
coin2_fx = pygame.mixer.Sound('img/coin2.wav')
coin2_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.6)

game_over_fx2 = pygame.mixer.Sound('img/game_over2.wav')
game_over_fx2.set_volume(0.6)

game_over_fx3 = pygame.mixer.Sound('img/game_over3.wav')
game_over_fx3.set_volume(0.6)

game_over_fx4 = pygame.mixer.Sound('img/game_over4.wav')
game_over_fx4.set_volume(0.6)

grito1 = pygame.mixer.Sound('img/grito1.wav')
grito1.set_volume(0.7)
grito2 = pygame.mixer.Sound('img/grito2.wav')
grito2.set_volume(0.7)
        
def readp():
    read = open('test.txt', mode='r')
    level = read.readline()
    read.close()
    return(level)

def savep(level):
    save = open('test.txt', mode='w')
    level = str(level)
    save.write(level)
    save.close()
    return(level)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_text2(text, font2, text_col, x, y):
    img = font2.render(text, True, text_col)
    screen.blit(img, (x, y))


#function to reset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    #load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    #create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action


class Player():

    
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        contador = random.randint(0,3)
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                if level >= 25 and level <34:
                    self.vel_y = -21
                else:
                    self.vel_y = -16
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0    
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False


            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                if level <= 33:
                    if contador == 0:
                        game_over_fx.play()
                    if contador == 1:
                        game_over_fx2.play()
                    if contador == 2:
                        game_over_fx3.play()
                    if contador == 3:
                        game_over_fx4.play()
                if level >= 34 and level <= 44:
                    if contador == 0 or contador == 1:
                        grito1.play()
                    if contador == 2 or contador == 3:
                        grito2.play()
                    

                    
            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                if level <= 33:
                    if contador == 0:
                        game_over_fx.play()
                    if contador == 1:
                        game_over_fx2.play()
                    if contador == 2:
                        game_over_fx3.play()
                    if contador == 3:
                        game_over_fx4.play()
                if level >= 34:
                    if contador == 0 or contador == 1:
                        grito1.play()
                    if contador == 2 or contador == 3:
                        grito2.play()

                    

            #check for collision with exit
            if level == 20:
                if score >= 5:
                    if pygame.sprite.spritecollide(self, exit_group, False):
                        game_over = 1
            if level == 21:
                if score >= 7:
                    if pygame.sprite.spritecollide(self, exit_group, False):
                        game_over = 1
            if level == 22:
                if score >= 8:
                    if pygame.sprite.spritecollide(self, exit_group, False):
                        game_over = 1
            if level == 23:
                if score >= 10:
                    if pygame.sprite.spritecollide(self, exit_group, False):
                        game_over = 1 
            else:
                if pygame.sprite.spritecollide(self, exit_group, False):
                    game_over = 1


            #check for collision with platforms
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction


            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            draw_text('Has muerto', font2, white, (screen_width // 2) - 90, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


#level load
level = readp()
level = int(level)

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        if level < 13:
            dirt_img = pygame.image.load('img/dirt.png')
            grass_img = pygame.image.load('img/grass.png')
        if level < 25 and level >=13:
            dirt_img = pygame.image.load('img/dirt2.png')
            grass_img = pygame.image.load('img/grass2.png')
        if level < 34 and level >= 25:
            dirt_img = pygame.image.load('img/dirt3.png')
            grass_img = pygame.image.load('img/grass3.png')
        if level < 45 and level >= 34:
            if level == 38:
                dirt_img = pygame.image.load('img/dirt2.png')
                grass_img = pygame.image.load('img/grass2.png')
            else:
                dirt_img = pygame.image.load('img/dirt.png')
                grass_img = pygame.image.load('img/grass.png')
        if level >= 45:
            dirt_img = pygame.image.load('img/dirt2.png')
            grass_img = pygame.image.load('img/grass2.png')
            
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                col_count += 1
            row_count += 1


    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if level <= 24:
            self.image = pygame.image.load('img/blob.png')
        if level >= 25:
            self.image = pygame.image.load('img/blob2.png')            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y


    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1





class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if level > 19 and level < 24:
            img = pygame.image.load('img/coin2.png')
        else:
            img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if level == 23:
            img = pygame.image.load('img/exit2.png')
        else:
            img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)



#load in level data and create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)


#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 140, screen_height // 2 -60, start_img)
credits_button = Button(screen_width //2- 120, screen_height // 2 + 90, credits_img)
exit_button = Button(screen_width // 2 - 120, screen_height // 2 +240, exit_img)
logo_button = Button(screen_width // 2 - 125, screen_height // 10, logo_img)


## BGM
if level <=9:
    pygame.mixer.music.load('img/music.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level  >= 10 and level < 13:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/boss.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level >= 13 and level <19:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/forest.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level >= 20 and level <24:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/boss.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level == 24:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/forest.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)  
if level >= 25 and level <33:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/skyb.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level >= 34 and level <45:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/triped.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
if level >= 45:
    pygame.mixer.music.unload()
    pygame.mixer.music.load('img/forest.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)

run = True
while run:


    clock.tick(fps)

    if level < 6:
        screen.blit(bg_img, (0, 0))
    if level < 10 and level >= 6:
        screen.blit(bg_img2, (0, 0))
    if level < 13 and level >= 10:
        screen.blit(bg_img3, (0,0))
    if level < 19 and level >= 13:
        screen.blit(bg_img4, (0,0))
        if level == 13:
            screen.blit(franco, (160,370))
    if level == 19:
        screen.blit(bg_img5, (0,0))
    if level < 25 and level > 19:
        screen.blit(bg_img6, (0,0))
        if level == 24:
            screen.blit(francof, (160,520))
    if level < 34 and level >= 25:
        screen.blit(bg_img7, (0,0))
    if level == 34:
        screen.blit(bg_img8, (0,0))
    if level >= 45:
        screen.blit(bg_img4, (0,0))
        screen.blit(francof, (500,620))
        screen.blit(ramon, (500, 620))

    if creditos == True:
        draw_text('Dibujos, Edicion,', font, white, (screen_width // 2) - 450, screen_height // 2 -21*3)
        draw_text('canciones y mapas:', font, white, (screen_width // 2) - 450, screen_height // 2 -21*2)
        draw_text('Franco Barría Rosas ', font, white, (screen_width // 2) - 450, screen_height // 2 -21)
        draw_text('Efectos:', font, white, (screen_width // 2) - 450, screen_height // 2)
        draw_text('sonidosmp3gratis.com', font, white, (screen_width // 2) - 450, screen_height // 2 +21)
        draw_text('Hecho para Navidad', font, white, (screen_width // 2) + 200, screen_height // 2 +21)
        draw_text('del 2021, un regalo para', font, white, (screen_width // 2) + 200, screen_height // 2 +21*2)
        draw_text('una persona muy  ', font, white, (screen_width // 2) + 200, screen_height // 2 +21*3)
        draw_text('especial para mi...', font, white, (screen_width // 2) + 200, screen_height // 2 + 21*4)
        draw_text('...El nombre de esa', font, white, (screen_width // 2) + 200, screen_height // 2 + 21*5)
        draw_text('persona es obvio', font, white, (screen_width // 2) + 200, screen_height // 2 + 21*6)
        draw_text('El honor de que te', font, white, (screen_width // 2) - 450, screen_height // 2 + 21*6)
        draw_text('encuentres jugando', font, white, (screen_width // 2) - 450, screen_height // 2 + 21*7)
        draw_text('mi primer juego es', font, white, (screen_width // 2) - 450, screen_height // 2 + 21*8)
        draw_text('magnifico, sea quien', font, white, (screen_width // 2) - 450, screen_height // 2 + 21*9)
        draw_text('sea el jugador.', font, white, (screen_width // 2) - 450, screen_height // 2 + 21*10)        
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
            creditos = False
        if credits_button.draw():
            creditos = True
        if logo_button.draw():
            creditos = True
    else:
        world.draw()



        if game_over == 0:
            blob_group.update()
            platform_group.update()
            #update score
            #check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                if level > 19 and level < 24:
                    coin2_fx.play()
                else:           
                    coin_fx.play()
            draw_text('= ' + str(score), font_score, white, tile_size - 10, 10)
        
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        #if player has died
        if game_over == -1:
            savep(level)
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

       #map writting
        if game_over == 0 and level == 1:
            draw_text('Me presento, soy la voz de tu cabeza, y...', font, white, (screen_width // 2) - 350, screen_height // 2 -21 *3)
            draw_text('...¡Las chinitas se han robado tu conejo!', font, white, (screen_width // 2) - 350, screen_height // 2 -21 *2)
            draw_text('aunque te den miedo, no eres alguien', font, white, (screen_width // 2) - 350, screen_height // 2 -21)
            draw_text('que mate animalitos, ¡EVITALAS!', font, white, (screen_width // 2) - 350, screen_height // 2)
        if game_over == 0 and level == 2:
            draw_text('¡Debes recoger las DogeCoins!', font, white, (screen_width // 2) - 350, screen_height // 8 -21 *2)
            draw_text('Aunque no sirvan de nada, ¡te guiaran!', font, white, (screen_width // 2) - 350, screen_height // 8 -21)
        if game_over == 0 and level == 4:
            draw_text('¡Tocar los pinchos te da más puntuacion!', font, white, (screen_width // 2) - 350, screen_height // 8 -21 *2)
        if game_over == 0 and level == 6:
            draw_text('Cayo la noche, y Luisa aun no encontraba a su conejo...', font, white, (screen_width // 2) - 350, screen_height // 8 -21 *2)
        if game_over == 0 and level == 8:
            draw_text('Notas que todo se vuelve más rocoso', font, white, (screen_width // 2) - 350, screen_height // 8 -21 *2)
        if game_over == 0 and level == 10:
            draw_text('Has encontrado el escondite', font, white, (screen_width // 2) - 400, screen_height // 2 -21*10)
            draw_text('de las chinitas, ¡encuentra a', font, white, (screen_width // 2) - 400, screen_height // 2 -21*9)
            draw_text('tu conejo!', font, white, (screen_width // 2) - 400, screen_height // 2 -21*8)
        if game_over == 0 and level == 12:
            draw_text('Al parecer aqui hay solo', font, white, (screen_width // 2 - 400) , screen_height //4 + 300)
            draw_text('chinitas, hay que salir de aqui', font, white, (screen_width // 2 - 400) , screen_height //4 + 300+21)
        if game_over == 0 and level == 13:
            draw_text('"¿Que haces aqui?', font, white, (screen_width // 2) - 400, screen_height // 2 -21*10)
            draw_text('Oh, se te ha perdido tu conejo,', font, white, (screen_width // 2) - 400, screen_height // 2 -21*9)
            draw_text('hay un arbol en lo más profundo', font, white, (screen_width // 2) - 400, screen_height // 2 -21*8)
            draw_text('de este bosque, el nos podra', font, white, (screen_width // 2) - 400, screen_height // 2 -21*7)
            draw_text('ayudar, me adelantare ya que', font, white, (screen_width // 2) - 400, screen_height // 2 -21*6)
            draw_text('al programar este juego se como', font, white, (screen_width // 2) - 400, screen_height // 2 -21*5)
            draw_text('saltarme niveles, ¡nos vemos!"', font, white, (screen_width // 2) - 400, screen_height // 2 -21*4)
        if game_over == 0 and level == 14:
            draw_text('Impresionante, llegamos a un bosque', font, white, (screen_width // 2) - 350, screen_height // 2 -21 *9)
            draw_text('¡A los conejos les gustan los bosques!', font, white, (screen_width // 2) - 350, screen_height // 2 -21 *8)
        if game_over == 0 and level == 18:
            draw_text('Recomendacion: ¡quedate en la moneda y que te aplasten!', font, white, (screen_width // 2) - 400, screen_height // 2 -21*10)
        if game_over == 0 and level == 19:
            draw_text('"Wow, otro viajero, asi que', font, white, (screen_width // 2) - 350, screen_height //4 -21)
            draw_text('tambien buscas a un conejo...', font, white, (screen_width // 2) - 350, screen_height //4)
            draw_text('...Ayudame a vencer a las arañas', font, white, (screen_width // 2) - 350, screen_height //4 + 21)
            draw_text('que viven dentro de mi, para', font, white, (screen_width // 2) - 350, screen_height //4 + 21*2)
            draw_text('ayudarte a buscar desde el cielo...', font, white, (screen_width // 2) - 350, screen_height //4 + 21*3)
            draw_text('...Pero cuidado, el viajero de antes', font, white, (screen_width // 2) - 350, screen_height //4 + 21*5)
            draw_text('intento ayudarme, y no ha salido."', font, white, (screen_width // 2) - 350, screen_height //4 + 21*6)
        if game_over == 0 and level == 20:
            draw_text('Debes quitar todas las arañas', font, white, (screen_width // 2 ) -200 , screen_height //4 -21)
            draw_text('para pasar de nivel', font, white, (screen_width // 2 ) -200 , screen_height //4)
        if game_over == 0 and level == 21:
            draw_text('a veces hay caminos secretos', font, white, (screen_width // 2 ) -200 , screen_height //4 -21)            
        if game_over == 0 and level == 23:
            draw_text('"¡AYUDAME!, las arañas', font, white, (screen_width // 2 + 170) , screen_height //4 + 200)
            draw_text('me han atrapado"', font, white, (screen_width // 2 + 170) , screen_height //4 + 221)
        if game_over == 0 and level == 24:
            draw_text('"Muchas gracias por salvarme', font, white, (screen_width // 2) - 350, screen_height // 2)
            draw_text('de las arañas, debes tener hambre,', font, white, (screen_width // 2) - 350, screen_height // 2+21)
            draw_text('come estos hongos que encontre"', font, white, (screen_width // 2) - 350, screen_height // 2+42)
        if game_over == 0 and level == 25:
            draw_text('Ahora puedes saltar mas alto', font, grey, (screen_width // 2 ) -200 , screen_height //4)
            draw_text('¡y las chinitas volar!', font, grey, (screen_width // 2 ) -200 , screen_height //4 +21)
        if game_over == 0 and level == 26:
            draw_text('Despues de comer, te sientes', font, grey, (screen_width // 2 ) -200 , screen_height //4)
            draw_text('demasiado liviana', font, grey, (screen_width // 2 ) -200 , screen_height //4 +21)
        if game_over == 0 and level == 27:
            draw_text('Aunque tienes un poco de nauseas', font, grey, (screen_width // 2 ) -200 , screen_height //4)
        if game_over == 0 and level == 32:
            draw_text('mmmmmmmmmmm ', font, grey, (screen_width // 2 ) -440 , screen_height //4 - 84)
            draw_text('¿porque estamos buscando', font, grey, (screen_width // 2 ) -440, screen_height //4-63)
            draw_text('un conejo en el cielo?', font, grey, (screen_width // 2 ) -440, screen_height //4- 42)
        if game_over == 0 and level == 33:
            draw_text('Ha sido una gran', font, grey, (screen_width // 2 ) -70 , screen_height //4)
            draw_text('aventura, aunque', font, grey, (screen_width // 2 ) -70 , screen_height //4 +21)
            draw_text('aun queda buscar', font, grey, (screen_width // 2 ) -70 , screen_height //4 +21*2)
            draw_text('en el infierno', font, grey, (screen_width // 2 ) -70 , screen_height //4 +21*3)
        if game_over == 0 and level == 34:
            draw_text('Este es el nivel final', font, white, (screen_width // 2 ) -200 , screen_height //4)
        if game_over == 0 and level == 35:
            draw_text('EstE es El Nivel Final', font, white, (screen_width // 2 ) -200 , screen_height //4+10)
        if game_over == 0 and level == 36:
            draw_text('Esta es El nivEL FiNaL', font, white, (screen_width // 2 ) -200 , screen_height //4)
        if game_over == 0 and level == 37:
            draw_text('EsTe Es ll NivEL FiNaL', font3, white, (screen_width // 2 ) -200 , screen_height //4)
        if game_over == 0 and level == 38:
            draw_text('"ayudame a vencer a los demonios', font3, white, (screen_width // 2) - 350, screen_height //4 + 21)
            draw_text('que viven dentro de mi, para', font3, white, (screen_width // 2) - 350, screen_height //4 + 52)
            draw_text('ayudarte a tocar el infierno"', font3, white, (screen_width // 2) - 350, screen_height //4 + 83)
        if game_over == 0 and level == 39:
            draw_text('MUERTE', font3, white, (screen_width // 2 ) -200 , screen_height //4)
            draw_text('ayudaaaaaa', font3, white, (screen_width // 2 - 370) , screen_height //4 + 200)
            draw_text('me muero', font3, white, (screen_width // 2 + 170) , screen_height //4 + 221)
            draw_text('MUERTE', font3, white, (screen_width // 2) , screen_height //4 -21)            
            draw_text('muerte', font, white, (screen_width // 2) - 350, screen_height // 8 -21 *2)
            draw_text('muerte', font, white, (screen_width // 2 - 400) , screen_height //4 + 300)
            draw_text('MUERTE', font, white, (screen_width // 2 - 400) , screen_height //4 + 300+21)
            draw_text('Al parecer aqui hay solo hay muerte', font, white, (screen_width // 2 - 400) , screen_height //4 + 300)
            draw_text('MueRTe', font, white, (screen_width // 2 - 400) , screen_height //4 + 300+21)
            draw_text('a veces hay caminos secretos', font3, white, (screen_width // 2 ) , screen_height //4 -21)   
        if game_over == 0 and level == 45:        
            draw_text('Creo que tenemos que dejar los hongos,', font, white, (screen_width // 2 ) - 100, screen_height //4 + 300 -21)
            draw_text('tu conejo siempre estuvo aqui', font, white, (screen_width // 2 ) - 100, screen_height //4 + 300)
        #if player has completed the level
        if game_over == 1:
            #reset game and go to next level
            level += 1
            if level == 1:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/music.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 10:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/boss.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 13:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/forest.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 20:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/boss.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 24:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/forest.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 25:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/skyb.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 34:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/triped.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)
            if level == 45:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('img/forest.wav')
                pygame.mixer.music.play(-1, 0.0, 5000)

            if level <= max_levels:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('  Felicidades, has completado', font, white, (screen_width // 2) - 160, screen_height // 2 -21*3)
                draw_text('los 45 niveles que he preparado', font, white, (screen_width // 2) - 160, screen_height // 2 -21*2)
                draw_text(' en este pequeño juego, espero', font, white, (screen_width // 2) - 160, screen_height // 2 -21)
                draw_text('que lo hayas disfrutado al igual', font, white, (screen_width // 2) - 160, screen_height // 2)
                draw_text('       que yo programandolo', font, white, (screen_width // 2) - 160, screen_height // 2 +21)
                if restart_button.draw():
                    level = 1


                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
