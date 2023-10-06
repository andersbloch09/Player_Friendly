import pygame as pg
import random
import platform
from extract_player_image import extract_player_image, extract_player_image_fall
from Scale_function import calculate_scale_factors
from update_and_hit_func import point_counter, sprite_movement, sprite_movement_terran, first_lvl_update, point_object_update, large_stone_hit_fence, carrot_hit_fence
from user_interface import ui
from sys import exit
import time 

pg.init()


# Width and Height of window 
width, height = 1800, 800

scale_factor = calculate_scale_factors(width, height)

# Here are all the used global variables 
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Width and Height of window 
WIDTH, HEIGHT = 1800 * scale_factor, 800 * scale_factor
print(WIDTH, HEIGHT)

# Velocities 
player_vel = int(8 * scale_factor)
screen_vel = int(2 * scale_factor)
sprite_vel = screen_vel

# Variable to control screenscroll start
screen_starter = 0

# Player hit variable
hit_occured = False
hit_occured_carrot = False
hit_occured_stone = False

# change of the variable
distance_between_poles = 0

# List with sprites of different kinds for env
avoid_object_list = []
large_stone_list = []
carrot_list = []

# Variables to control flow of character animation

##########################################################################

# Makes the first display and its size
#WIN = pg.display.set_mode((WIDTH * scale_factor, HEIGHT * scale_factor)) 
# None scaled Change when done scaling
WIN = pg.display.set_mode((WIDTH, HEIGHT)) 
# Makes caption 
pg.display.set_caption('Player friendly.')

# Player size of rect
player_WIDTH = 40/3 * scale_factor
player_HEIGHT = 40/3 * scale_factor

# player = pg.Rect(0, 0, player_WIDTH, player_HEIGHT)

#This is the main background 
system_type = platform.system()

if system_type == "Darwin":
    print("macOS")
    GREEN_WORLD = pg.transform.scale(pg.image.load('Assets/GreenWorld.PNG').convert(), (WIDTH, HEIGHT)) 
    large_stone_image = pg.image.load("Assets/Small_stones_above_grey.png").convert_alpha()
    sprite_sheet_image = pg.image.load("Assets/walking_assets_player_friendly_1.png").convert_alpha()
    sprite_sheet_image_fall = pg.image.load("Assets/hit_fence_assets_done.png").convert_alpha()
    hegn_til_anders = pg.image.load("Assets/HegnTilAnders.png").convert_alpha()
    large_carrot = pg.image.load("Assets/large_carrot.png").convert_alpha()
elif system_type == "Windows":
    print("Windows")
    GREEN_WORLD = pg.transform.scale(pg.image.load('Assets\GreenWorld.PNG').convert(), (WIDTH, HEIGHT)) 
    large_stone_image = pg.image.load("Assets\Small_stones_above_grey.png").convert_alpha()
    sprite_sheet_image = pg.image.load("Assets\walking_assets_player_friendly_1.png").convert_alpha()
    sprite_sheet_image_fall = pg.image.load("Assets\hit_fence_assets_done.png").convert_alpha()
    hegn_til_anders = pg.image.load("Assets\HegnTilAnders.png").convert_alpha()
    large_carrot = pg.image.load("Assets\large_carrot.png").convert_alpha()

# Events based on the game progress
PLAYER_HIT_FRONT = pg.USEREVENT + 1
PLAYER_HIT_BACK = pg.USEREVENT + 2
CARROT_PICK = pg.USEREVENT + 3
STONE_HIT = pg.USEREVENT + 4

# Creates Text fonts 
HEALTH_FONT = pg.font.SysFont('comicsans', int(40 * scale_factor))
POINT_FONT = pg.font.SysFont('comicsans', int(40 * scale_factor))
LOSE_FONT = pg.font.SysFont('comicsans', int(100 * scale_factor))

#####################################################################################

# This class is to controll the animation of the character
class PlayerSpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame_run, width, height, scale):
		image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame_run * width), 0, width, height))
		image = pg.transform.scale(image, (width * scale * scale_factor, height * scale * scale_factor))

		return image

# This class will create terran objects
class large_stone_one(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, initial_width, initial_height):
        pg.sprite.Sprite.__init__(self)
        # Note consider loading the image outside of the class
        self.image = large_stone_image
        self.image = pg.transform.scale(self.image, (initial_width, initial_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = screen_vel

    def update_speed(self):
        global screen_starter
        global large_stone_list
        if screen_starter >= 1 or player.x > 100 * scale_factor:
            self.rect.x -= screen_vel
            if self.rect.x <= -10 * scale_factor:
                self.kill()
                if large_stone_list:
                    large_stone_list.pop(0)
                else: 
                    pass
    
    def draw(self): 
        WIN.blit(self.image, (self.rect.topleft[0], self.rect.topleft[1]))
     
# Class for creation of sprites for poles 
class avoid_object(pg.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = sprite_vel
        self.hegn_til_anders = hegn_til_anders

    def update_speed(self):
        global screen_starter
        global avoid_object_list
        if screen_starter >= 1 or player.x > 100 * scale_factor:
            self.rect.x -= screen_vel
            if self.rect.x <= -10 * scale_factor:
                self.kill()
                if avoid_object_list:
                    avoid_object_list.pop(0)
                else: 
                    pass

# This need a lot of logic work 
    def add_image(self):
        image_size = self.image.get_size()
        hegn_til_anders = pg.transform.scale(self.hegn_til_anders, (int(20 * 1.5 * scale_factor), int(92 * 1.5 * scale_factor)))
        nrimages = image_size[1] // int(92 * scale_factor)
        if nrimages <= 1: 
            nrimages += 1
        if self.rect.topleft[1] == int(-10 * scale_factor): 
            j = int(-146 * scale_factor)
            rotated_image = pg.transform.rotate(hegn_til_anders, 180)
            for i in range(nrimages):
                WIN.blit(rotated_image, (self.rect.topleft[0] - int(5 * scale_factor), image_size[1] + j))
                j -= int(130 * scale_factor)

        if self.rect.topleft[1] > 0: 
            j = 0
            for i in range(nrimages):
                WIN.blit(hegn_til_anders, (self.rect.topleft[0] - int(5 * scale_factor), int(818 * scale_factor) - image_size[1] + j))
                j += int(130 * scale_factor) 

# Creates the points as carrots or other things and controls them
class point_object(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([int((57 * 0.7) * scale_factor), int((52 * 0.7) * scale_factor)])
        self.image.fill(BLACK)
        self.carrot = large_carrot
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = screen_vel

    def update_speed(self):
        global screen_starter
        global carrot_list
        if screen_starter >= 1 or player.x > 100 * scale_factor:
            self.rect.x -= screen_vel
            if self.rect.x <= -10 * scale_factor:
                self.kill()
                if carrot_list:
                    carrot_list.pop(0)
                else: 
                    pass

    def draw_carrot(self):
        # carrot is 57x52 in size before scaling
        large_carrot_scaled = pg.transform.scale(self.carrot, (int((57 * 0.7) * scale_factor), int((52 * 0.7) * scale_factor)))
        WIN.blit(large_carrot_scaled, (self.rect.topleft[0], self.rect.topleft[1]))

class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, player_rect):
        pg.sprite.Sprite.__init__(self)
        self.rect = player_rect

###################################################################################

# This function controlls the points spawn and pickup
def sprite_creation_points(point_carrots_group, carrot_list):
    global screen_starter
    if len(carrot_list) < 6: 
        if screen_starter == 0:
                pos_x = random.randint(int(101 * scale_factor), int(1750 * scale_factor))
                pos_y = random.randint(int(0 * scale_factor), int(750 * scale_factor))
        else:
            pos_x = WIDTH + 100
            pos_y = random.randint(int(0 * scale_factor), int(750 * scale_factor))

        carrot = point_object(pos_x, pos_y)

        carrot_list.append(carrot)

        point_carrots_group.add(carrot)

        for sprite in carrot_list:
            point_carrots_group.add(sprite)

    return point_carrots_group

# Creates stones
def create_large_stone(terran_large_stone, large_stone_list):
    global screen_starter

    if len(large_stone_list) < 3:
        if screen_starter == 0:
            pos_x = random.randint(int(101 * scale_factor), int(1750 * scale_factor))
            pos_y = random.randint(int(0 * scale_factor), int(750 * scale_factor))
        else:
            pos_x = WIDTH
            pos_y = random.randint(int(0 * scale_factor), int(750 * scale_factor))
            
        initial_width, initial_height = int(65 * scale_factor), int(65 * scale_factor)

        stone = large_stone_one(pos_x, pos_y, initial_width, initial_height)
        large_stone_list.append(stone)

        terran_large_stone.add(stone)
        
        for sprite in large_stone_list:
            terran_large_stone.add(sprite)
        
    return terran_large_stone

# Call this function to create and manage large stones
def sprite_creation_terran(terran_large_stone, large_stone_list):
    global screen_starter
    if screen_starter > 0 and len(large_stone_list) < 2:
        random_num = random.randint(int(0 * scale_factor), int(200 * scale_factor))
        if random_num == 20:
            return create_large_stone(terran_large_stone, large_stone_list)
        else:
            return terran_large_stone
    else:
        return create_large_stone(terran_large_stone, large_stone_list)

# Function which creates the sprites both on bottom and on top
def sprite_creation_first_lvl(first_lvl_group):
    global distance_between_poles
    global avoid_object_list
    # Top Sprite 
    if len(avoid_object_list) < 12:
        sprite_pos_y = int(-10 * scale_factor)
        sprite_pos_x = WIDTH - distance_between_poles
        sprite_width = int(20 * scale_factor)
        sprite_height = random.randint(int(100 * scale_factor), int(625 * scale_factor))
        # This variable desides the distance between the poles
        distance_between_poles -= int(300 * scale_factor)
        
        object_number = avoid_object(sprite_width, sprite_height, sprite_pos_x, sprite_pos_y, (BLACK))
        avoid_object_list.append(object_number)
    
        # Bottom Sprite
        sprite_width = int(20 * scale_factor)
        # This line is made to get the correct distance between the poles on each side
        sprite_height = int(800 * scale_factor) - (sprite_height + int(75 * scale_factor))

        sprite_pos_y = HEIGHT - sprite_height + int(20 * scale_factor)
        object_number = avoid_object(sprite_width, sprite_height, sprite_pos_x, sprite_pos_y, (BLACK))
        avoid_object_list.append(object_number)
        for sprite in avoid_object_list:
            first_lvl_group.add(sprite)

        return(first_lvl_group)
    else:
        distance_between_poles = 0
        for sprite in avoid_object_list:
            first_lvl_group.add(sprite)
        return first_lvl_group    


# Draws the content on the window
def draw_window(player, green_world_move, first_lvl_group, start_line, player_health, 
                terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count):
    WIN.fill((BLACK))
    WIN.blit(GREEN_WORLD, (green_world_move.x, green_world_move.y))
    # The two if statements resolve in the moving background refresh
    WIN.blit(GREEN_WORLD, (green_world_move.x + WIDTH, green_world_move.y))
    if green_world_move.x <= -WIDTH:
        green_world_move.x = 0

    # This draws the start line 
    if start_line.x > -10 * scale_factor:
        pg.draw.rect(WIN, RED, start_line)
   
###################################################################################################
   
    # This function here draws the fences
    first_lvl_update(first_lvl_group)
    #first_lvl_group.draw(WIN)
    # Draws the stones
    sprite_movement_terran(terran_large_stone)
    # Updates and draws carrots
    #point_carrots_group.draw(WIN)
    point_object_update(point_carrots_group)

###################################################################################################

    # Displays health 
    player_health = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)

    # Displays points
    point_count = format(point_count, ".0f")
    point_count = POINT_FONT.render(
        "Points: " + str(point_count), 1, WHITE)

    WIN.blit(point_count, (int(300 * scale_factor), int(10 * scale_factor)))
    WIN.blit(player_health, (int(10 * scale_factor), int(10 * scale_factor)))

    # This draws the player 
    # print(action_run, frame_run)
    WIN.blit(animation_list[action_run][frame_run], ((player.x - int(18 * scale_factor)) + new_x, (player.y - int(18 * scale_factor)) + new_y))
    #pg.draw.rect(WIN, BLACK, player)
    # This updates everything onto the screen
    pg.display.update()

# gets center of the image for animation to match when running cross way
def get_center_coords(image):
	rect_rotated = image.get_rect()
		
	center = rect_rotated.center

	new_x = 0 - center[0] + int(37 * scale_factor)
	new_y = 0 - center[1] + int(37 * scale_factor)
	return new_x, new_y

# This function creates the movement for the player
def player_movement(keys_pressed, player, still_player_image, last_update_player, animation_cooldown, frame_run, action_run, new_x, new_y, screen_starter):
    current_time = pg.time.get_ticks()
    if current_time - last_update_player >= animation_cooldown:
        frame_run += 1
        last_update_player = current_time
        if frame_run == 11: 
            frame_run = 0
    new_y = 0
    new_x = 0
    if not any(keys_pressed):
        action_run = 8
    if player.x <= 0 and screen_starter >= 1:
        action_run = 0
    # This controls straight walks
    if keys_pressed[pg.K_a] and player.x > 0:
        player.x -= player_vel
        action_run = 2
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3:
        player.x += player_vel
        action_run = 0 
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_w]:
        player.y -= player_vel
        action_run = 1
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_s]:
        player.y += player_vel
        action_run = 3
        new_y = 0
        new_x = 0

    # This controls the side walk 
    if keys_pressed[pg.K_d] and keys_pressed[pg.K_w] and player.x < WIDTH - player_WIDTH*3:
        action_run = 4
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_w] and keys_pressed[pg.K_a] and player.x > 0:
        action_run = 5
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_a] and keys_pressed[pg.K_s] and player.x > 0:
        action_run = 6
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_s] and keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3:
        action_run = 7
        new_x, new_y = get_center_coords(still_player_image)
    
    if player.y < -player_HEIGHT*3: 
        player.y = HEIGHT
    if player.y > HEIGHT:
        player.y = -player_HEIGHT*3
        
    return action_run, frame_run, new_x, new_y, last_update_player

# This function should handle the animation time and movement for the fall animation
def fall_animation(animation_cooldown_fall, last_update_player, frame_run, fall_front, fall_back, fall, action_run):
    current_time = pg.time.get_ticks()
    # This lines removes bugs with frame_run from other animations
    if action_run < 10: 
        frame_run = 0

    if fall_front == True: 
        action_run = 10
        if frame_run < 6: 
            player.x -= 7 * scale_factor

    if fall_back == True:
        action_run = 11
        if frame_run < 6: 
            player.x += 7 * scale_factor

    if current_time - last_update_player >= animation_cooldown_fall:
        frame_run += 1
        last_update_player = current_time
        if frame_run == 16: 
            frame_run = 0
            fall_back = False 
            fall_front = False
            fall = 0

    return action_run, frame_run, fall_front, fall_back, fall, last_update_player

# This function decides when the screen will move and how fast 
def screen_movement(player, green_world_move):
    global screen_starter
    if screen_starter >= 1 or player.x > 100 * scale_factor: 
        green_world_move.x -= screen_vel
        screen_starter += 1
        if player.x > 0 * scale_factor:
            player.x += -screen_vel
    
# This function check colission of objects and the player 
def player_hit(first_lvl_group, player):
    global hit_occured
    player_sprite = PlayerSprite(player)
    collided_sprites = pg.sprite.spritecollide(player_sprite, first_lvl_group, False)

    #if collided_sprites:
        #print(abs(player.x + 40 - collided_sprites[0].rect.x))

    if not hit_occured and len(collided_sprites) == 1:
        hit_occured = True
        if abs(player.x + int(40 * scale_factor) - collided_sprites[0].rect.x) < int(30 * scale_factor): 
            pg.event.post(pg.event.Event(PLAYER_HIT_FRONT))
            
        elif abs((player.x + int(40 * scale_factor)) - collided_sprites[0].rect.x) > int(30 * scale_factor):
            pg.event.post(pg.event.Event(PLAYER_HIT_BACK))

    elif hit_occured and len(collided_sprites) < 1: 
        hit_occured = False

# This function is for colission check of carrots and player point count 
def carrot_pick(point_carrots_group, player_sprite):
    global hit_occured_carrot 
    collided_sprites = pg.sprite.spritecollide(player_sprite, point_carrots_group, True)
    
    if not hit_occured_carrot and len(collided_sprites) == 1:
        hit_occured_carrot = True
        collided_sprite = collided_sprites[0]
        # if collided_sprite in carrot_list:
        if collided_sprite in carrot_list:
            carrot_list.remove(collided_sprite)
        pg.event.post(pg.event.Event(CARROT_PICK))
    elif hit_occured_carrot and len(collided_sprites) < 1: 
        hit_occured_carrot = False


def stone_hit(terran_large_stone, player_sprite):
    global hit_occured_stone
    collided_sprites = pg.sprite.spritecollide(player_sprite, terran_large_stone, False)
    if not hit_occured_stone and len(collided_sprites) == 1:
        hit_occured_stone = True
        pg.event.post(pg.event.Event(STONE_HIT))
    elif hit_occured_stone and len(collided_sprites) < 1: 
        hit_occured_stone = False


def draw_lose(player, green_world_move, first_lvl_group, start_line, player_health,
               terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count):
    frame_run = 0
    draw_window(player, green_world_move, first_lvl_group, start_line, player_health,
                 terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count)
    
    draw_text = LOSE_FONT.render("LOSER!", 1, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pg.display.update()
    pg.time.delay(1000)


def main():
    global screen_starter
    global player
    global distance_between_poles
    global large_stone_list
    global screen_vel
    global player_vel
    # List clearing to avoid large ram issues
    avoid_object_list.clear()
    large_stone_list.clear()
    carrot_list.clear()
    # init of the starter variables
    distance_between_poles = 0
    screen_starter = 0
    player = pg.Rect(0 * scale_factor, HEIGHT//2, player_WIDTH*3, player_HEIGHT*3)
    start_line = pg.Rect(100 * scale_factor, 0 * scale_factor, 10 * scale_factor, 800 * scale_factor)
    first_lvl_group = pg.sprite.Group()
    terran_large_stone = pg.sprite.Group()
    point_carrots_group = pg.sprite.Group()
    green_world_move = pg.Rect(0 * scale_factor, 0 * scale_factor, WIDTH, HEIGHT)
    hit_count = 0
    player_health = 10000
    point_count = 0
    screen_vel = int(2 * scale_factor)
    player_vel = int(8 * scale_factor)

    # Counter for animation of character 
    sprite_sheet = PlayerSpriteSheet(sprite_sheet_image)
    last_update_player = pg.time.get_ticks()
    animation_cooldown = 20
    frame_run = 0 
    action_run = 8
    new_x = 0
    new_y = 0

    # Variables for fall animation
    sprite_sheet_fall = PlayerSpriteSheet(sprite_sheet_image_fall)
    # Function from other doc
    animation_list_fall = extract_player_image_fall(sprite_sheet_fall)
    # Variable to detect if fall is happening
    fall = 0
    fall_front = 0
    fall_back = 0
    animation_cooldown_fall = 50

    # Init function to save the animation images
    animation_list = extract_player_image(sprite_sheet)
    for x in range(len(animation_list_fall)):
        animation_list.append(animation_list_fall[x])
    still_player_image = pg.transform.rotate(animation_list[0][0], 315)
    # User interface variables
    user_interface = 1

    # Sprite for player rect to check for colissions with the pygame functions 
    player_sprite = PlayerSprite(player)

    # Timers to control speed and points
    speed_timer_0 = time.time()
    point_timer_0 = time.time()

    clock = pg.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                exit()

            # Event for player hit 
            if event.type == PLAYER_HIT_FRONT:
                hit_count += 1
                player_health -= 1
                fall_front = True 
                fall = 1

            if event.type == PLAYER_HIT_BACK:
                hit_count += 1
                player_health -= 1
                fall_back = True
                fall = 1
        
            if event.type == CARROT_PICK: 
                point_timer_0 -= 10

            if event.type == STONE_HIT:
                point_timer_0 += 25

        # Draw if you lose
        if player_health <= 0: 
            frame_run = 0
            draw_lose(player, green_world_move, first_lvl_group, start_line, player_health,
                    terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count)
            break
        if player.x <= -15:
            player_health = 0

        speed_timer_1 = time.time()
        if speed_timer_1 - speed_timer_0 > 10:
            # Put change in speed here if wanted
            if screen_vel < 3 * scale_factor:
                screen_vel += 1
                speed_timer_0 = speed_timer_1
        if speed_timer_1 - speed_timer_0 > 25:
            if screen_vel < 4 * scale_factor:
                screen_vel += 1
                speed_timer_0 = speed_timer_1
        if point_count > 5000 and screen_vel < 5 * scale_factor: 
            player_vel += 1 
            screen_vel += 1 
        print(screen_vel)
        print(player_vel)

        # These lines are for the sprites creation and updates 
        if screen_starter >= 1 or player.x > int(100 * scale_factor):
            first_lvl_group = sprite_creation_first_lvl(first_lvl_group)
            sprite_movement(first_lvl_group)
            start_line.x -= screen_vel
            point_count = point_counter(point_timer_0)
        # This line makes the point timer restart until the game actually starts 
        else:
            point_timer_0 = time.time()
        
        point_carrots_group = sprite_creation_points(point_carrots_group, carrot_list)
        terran_large_stone = sprite_creation_terran(terran_large_stone, large_stone_list)
        large_stone_hit_fence(first_lvl_group, terran_large_stone)
        carrot_hit_fence(first_lvl_group, point_carrots_group)
        keys_pressed = pg.key.get_pressed()
        carrot_pick(point_carrots_group, player_sprite)
        stone_hit(terran_large_stone, player_sprite) 
        player_hit(first_lvl_group, player)

        if user_interface == 1: 
            if fall == 0: 
                action_run, frame_run, new_x, new_y, last_update_player = player_movement(keys_pressed, player, still_player_image, last_update_player,
                                                        animation_cooldown, frame_run, action_run, new_x, new_y, screen_starter)

            if fall == 1:
                action_run, frame_run, fall_front, fall_back, fall, last_update_player = fall_animation(animation_cooldown_fall, last_update_player, frame_run, fall_front, fall_back, fall, action_run)

        screen_movement(player, green_world_move)

        draw_window(player, green_world_move, first_lvl_group, start_line, player_health,
                    terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count)
        
        if user_interface == 0:
            ui()
        # Checks for button reset of game
        if keys_pressed[pg.K_PLUS]:
            main()
    main()

if __name__ == "__main__":
    main()
