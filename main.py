from typing import Any
import pygame as pg
import random
import platform
from extract_player_image import extract_player_image

pg.font.init()
pg.mixer.init()

# Width and Height of window 
WIDTH, HEIGHT = 1800, 800

# Here are all the used global variables 
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Velocities 
PLAYER_VEL = 12
SCREEN_VEL = 5
SPRITE_VEL = SCREEN_VEL

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
WIN = pg.display.set_mode((WIDTH, HEIGHT)) 
# Makes caption 
pg.display.set_caption('Player friendly.')

# Player size of rect
player_WIDTH = 25
player_HEIGHT = 25

player = pg.Rect(0, 0, player_WIDTH, player_HEIGHT)

#This is the main background 
system_type = platform.system()

if system_type == "Darwin":
    print("macOS")
    GREEN_WORLD = pg.transform.scale(pg.image.load('Assets/GreenWorld.PNG'), (WIDTH, HEIGHT)) 
    large_stone_image = pg.image.load("Assets/Small_stones_above_grey.png").convert_alpha()
    sprite_sheet_image = pg.image.load("Assets/walking_assets_player_friendly_1.png")
    hegn_til_anders = pg.image.load("Assets/HegnTilAnders.png")
    large_carrot = pg.image.load("Assets/large_carrot.png")
elif system_type == "Windows":
    print("Windows")
    GREEN_WORLD = pg.transform.scale(pg.image.load('Assets\GreenWorld.PNG'), (WIDTH, HEIGHT)) 
    large_stone_image = pg.image.load("Assets\Small_stones_above_grey.png").convert_alpha()
    sprite_sheet_image = pg.image.load("Assets\walking_assets_player_friendly_1.png")
    hegn_til_anders = pg.image.load("Assets\HegnTilAnders.png")
    large_carrot = pg.image.load("Assets\large_carrot.png")

# Events based on the game progress
PLAYER_HIT = pg.USEREVENT + 1
CARROT_PICK = pg.USEREVENT + 2
STONE_HIT = pg.USEREVENT + 3

# Creates Text fonts 
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
POINT_FONT = pg.font.SysFont('comicsans', 40)
LOSE_FONT = pg.font.SysFont('comicsans', 100)

#####################################################################################

# This class is to controll the animation of the character
class PlayerSpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame_run, width, height, scale):
		image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame_run * width), 0, width, height))
		image = pg.transform.scale(image, (width * scale, height * scale))

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
        self.speed = SCREEN_VEL

    def update_speed(self):
        global screen_starter
        global large_stone_list
        if screen_starter >= 1 or player.x > 100:
            self.rect.x -= self.speed
            if self.rect.x <= -10:
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
        self.speed = SPRITE_VEL
        self.hegn_til_anders = hegn_til_anders

    def update_speed(self):
        global screen_starter
        global avoid_object_list
        if screen_starter >= 1 or player.x > 100:
            self.rect.x -= self.speed
            if self.rect.x <= -10:
                self.kill()
                if avoid_object_list:
                    avoid_object_list.pop(0)
                else: 
                    pass

# This need a lot of logic work 
    def add_image(self):
        image_size = self.image.get_size()
        hegn_til_anders = pg.transform.scale(self.hegn_til_anders, (20 * 1.5, 92 * 1.5))
        nrimages = image_size[1] // 92
        if nrimages == 1: 
            nrimages += 1
        if self.rect.topleft[1] == -10: 
            j = -146
            rotated_image = pg.transform.rotate(hegn_til_anders, 180)
            for i in range(nrimages):
                WIN.blit(rotated_image, (self.rect.topleft[0] - 5, image_size[1] + j))
                j -= 130

        if self.rect.topleft[1] > 0: 
            j = 0
            for i in range(nrimages):
                WIN.blit(hegn_til_anders, (self.rect.topleft[0] - 5, 818 - image_size[1] + j))
                j += 130

# Creates the points as carrots or other things and controls them
class point_object(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pg.sprite.Sprite.__init__(self)
        self.image = large_carrot
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = SCREEN_VEL

    def update_speed(self):
        global screen_starter
        global carrot_list
        if screen_starter >= 1 or player.x > 100:
            self.rect.x -= self.speed
            if self.rect.x <= -10:
                self.kill()
                if carrot_list:
                    carrot_list.pop(0)
                else: 
                    pass

    def draw_carrot(self):
        # carrot is 57x52 in size before scaling
        large_carrot = pg.transform.scale(self.image, (57 * 0.7, 52 * 0.7))
        WIN.blit(large_carrot, (self.rect.topleft[0], self.rect.topleft[1]))

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
                pos_x = random.randint(101, 1750)
                pos_y = random.randint(0, 750)
        else:
            pos_x = 1800
            pos_y = random.randint(0, 750)

        carrot = point_object(pos_x, pos_y)

        carrot_list.append(carrot)

        point_carrots_group.add(carrot)

        for sprite in carrot_list:
            point_carrots_group.add(sprite)

    return point_carrots_group



def create_large_stone(terran_large_stone, large_stone_list):
    global screen_starter

    if len(large_stone_list) < 2:
        if screen_starter == 0:
            pos_x = random.randint(101, 1750)
            pos_y = random.randint(0, 750)
        else:
            pos_x = 1800
            pos_y = random.randint(0, 750)
            
        initial_width, initial_height = 65, 65

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
        random_num = random.randint(0, 200)
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
        sprite_width = 20
        sprite_pos_y = 0 - 10
        sprite_pos_x = WIDTH - distance_between_poles
        sprite_height = random.randint(100, 350)
        # This variable desides the distance between the poles
        distance_between_poles -= 300
        object_number = avoid_object(sprite_width, sprite_height, sprite_pos_x, sprite_pos_y, (BLACK))
        avoid_object_list.append(object_number)
    
        # Bottom Sprite
        sprite_width = 20
        # This line is made to get the correct distance between the poles on each side
        sprite_height = 800 - (sprite_height + 75)
        
        sprite_pos_y = HEIGHT - sprite_height + 20
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

# This function uses a callback to the class to update the individual sprite location
def sprite_movement(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.update_speed()

# This updates the fence of the groups and draws them 
def first_lvl_update(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.add_image()

# Draws the points
def point_object_update(point_carrots_group):
    for sprite in point_carrots_group:
        sprite.update_speed()
        sprite.draw_carrot()

# This changes the speed of the stones
def sprite_movement_terran(sprite_group):
    for sprite in sprite_group:
        sprite.update_speed()
        sprite.draw()

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
    if start_line.x > -10:
        pg.draw.rect(WIN, RED, start_line)
   
###################################################################################################
   
    # This function here draws the fences
    first_lvl_update(first_lvl_group)
    # Draws the stones
    sprite_movement_terran(terran_large_stone)
    # Updates and draws carrots
    point_object_update(point_carrots_group)

###################################################################################################

    # Displays health 
    player_health = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)

    # Displays points
    point_count = POINT_FONT.render(
        "Carrots: " + str(point_count), 1, WHITE)

    WIN.blit(point_count, (300, 10))
    WIN.blit(player_health, (10, 10))

    # This draws the player 
    # pg.draw.rect(WIN, BLACK, player)
    WIN.blit(animation_list[action_run][frame_run], ((player.x - 18) + new_x, (player.y - 18) + new_y))
    # This updates everything onto the screen
    pg.display.update()

# gets center of the image for animation to match when running cross way
def get_center_coords(image):
	rect_rotated = image.get_rect()
		
	center = rect_rotated.center

	new_x = 0 - center[0] + 37
	new_y = 0 - center[1] + 37
	return new_x, new_y

# This function creates the movement for the player
def player_movement(keys_pressed, player, still_player_image, last_update_player, animation_cooldown, frame_run, action_run, new_x, new_y):
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
    # This controls straight walks
    if keys_pressed[pg.K_a] and player.x > 0:
        player.x -= PLAYER_VEL
        action_run = 2
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3:
        player.x += PLAYER_VEL
        action_run = 0 
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_w] and player.y > 0:
        player.y -= PLAYER_VEL
        action_run = 1
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_s] and player.y < HEIGHT - player_HEIGHT*3:
        player.y += PLAYER_VEL
        action_run = 3
        new_y = 0
        new_x = 0

    # This controls the side walk 
    if keys_pressed[pg.K_d] and keys_pressed[pg.K_w] and player.x < WIDTH - player_WIDTH*3 and player.y > 0:
        action_run = 4
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_w] and keys_pressed[pg.K_a] and player.x > 0 and player.y > 0:
        action_run = 5
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_a] and keys_pressed[pg.K_s] and player.x > 0 and player.y < HEIGHT - player_HEIGHT*3:
        action_run = 6
        new_x, new_y = get_center_coords(still_player_image)
    if keys_pressed[pg.K_s] and keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3 and player.y < HEIGHT - player_HEIGHT*3:
        action_run = 7
        new_x, new_y = get_center_coords(still_player_image)
    
    return action_run, frame_run, new_x, new_y

# This function decides when the screen will move and how fast 
def screen_movement(player, green_world_move, action_run):
    global screen_starter
    if screen_starter >= 1 or player.x > 100: 
        green_world_move.x -= SCREEN_VEL
        screen_starter += 1
        if player.x > 0:
            player.x += -SCREEN_VEL
        if player.x <= 0: 
            action_run = 0
    
    return action_run

# This function check colission of objects and the player 
def player_hit(first_lvl_group, player):
    global hit_occured
    player_sprite = PlayerSprite(player)
    collided_sprites = pg.sprite.spritecollide(player_sprite, first_lvl_group, False)

    if not hit_occured and len(collided_sprites) == 1:
        hit_occured = True
        pg.event.post(pg.event.Event(PLAYER_HIT))
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

def large_stone_hit_fence(first_lvl_group, terran_large_stone):
    # This line of code checks for collision between the two groups and removes the one from terran_large_stone chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, terran_large_stone, False, True)

def carrot_hit_fence(first_lvl_group, point_carrots_group):
    # This line of code checks for collision between the two groups and removes the one from point_carrots_group chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, point_carrots_group, False, True)

def draw_lose(player, green_world_move, first_lvl_group, start_line, player_health,
               terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count):
    
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
    global SCREEN_VEL
    # List clearing to avoid large ram issues
    avoid_object_list.clear()
    large_stone_list.clear()
    carrot_list.clear()
    # init of the starter variables
    distance_between_poles = 0
    screen_starter = 0
    player = pg.Rect(0, HEIGHT//2, 40, 40)
    start_line = pg.Rect(100, 0, 10, 800)
    first_lvl_group = pg.sprite.Group()
    terran_large_stone = pg.sprite.Group()
    point_carrots_group = pg.sprite.Group()
    green_world_move = pg.Rect(0, 0, WIDTH, HEIGHT)
    hit_count = 0
    player_health = 3
    point_count = 0

    # Counter for animation of character 
    sprite_sheet = PlayerSpriteSheet(sprite_sheet_image)
    last_update_player = pg.time.get_ticks()
    animation_cooldown = 75
    frame_run = 0 
    action_run = 8
    new_x = 0
    new_y = 0
    
    # Init function to save the animation images
    animation_list = extract_player_image(sprite_sheet)
    still_player_image = pg.transform.rotate(animation_list[0][0], 315)

    clock = pg.time.Clock()
    run = True

    player_sprite = PlayerSprite(player)
    speed_timer_0 = pg.time.get_ticks()


    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            # Event for player hit 
            if event.type == PLAYER_HIT:
                hit_count += 1
                player_health -= 1
                player.x = player.x - 100
        
            if event.type == CARROT_PICK: 
                point_count += 1

            if event.type == STONE_HIT:
                point_count -= 3

        # Draw if you lose
        if player_health <= 0: 
            draw_lose(player, green_world_move, first_lvl_group, start_line, player_health,
                       terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count)
            break
        if player.x <= -10:
            player_health = 0

        speed_timer_1 = pg.time.get_ticks()
        if speed_timer_1 - speed_timer_0 > 500:
            SCREEN_VEL += 1
            speed_timer_0 = speed_timer_1

        # These lines are for the sprites creation and updates 
        if screen_starter >= 1 or player.x > 100:
            first_lvl_group = sprite_creation_first_lvl(first_lvl_group)
            sprite_movement(first_lvl_group)
            start_line.x -= SCREEN_VEL


        point_carrots_group = sprite_creation_points(point_carrots_group, carrot_list)
        terran_large_stone = sprite_creation_terran(terran_large_stone, large_stone_list)
        large_stone_hit_fence(first_lvl_group, terran_large_stone)
        carrot_hit_fence(first_lvl_group, point_carrots_group)
        keys_pressed = pg.key.get_pressed()
        carrot_pick(point_carrots_group, player_sprite)
        stone_hit(terran_large_stone, player_sprite) 
        player_hit(first_lvl_group, player)

        action_run, frame_run, new_x, new_y = player_movement(keys_pressed, player, still_player_image, last_update_player,
                                                       animation_cooldown, frame_run, action_run, new_x, new_y)


        action_run = screen_movement(player, green_world_move, action_run)
        draw_window(player, green_world_move, first_lvl_group, start_line, player_health,
                     terran_large_stone, action_run, frame_run, new_x, new_y, animation_list, point_carrots_group, point_count)

    main()

if __name__ == "__main__":
    main()
