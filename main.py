import pygame as pg
import random
import platform
from extract_player_image import extract_player_image

pg.font.init()

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

# change of the variable
distance_between_poles = 0

# List with sprites of different kinds for env
avoid_object_list = []
large_stone_list = []

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
elif system_type == "Windows":
    print("Windows")
    GREEN_WORLD = pg.transform.scale(pg.image.load('Assets\GreenWorld.PNG'), (WIDTH, HEIGHT)) 
    large_stone_image = pg.image.load("Assets\Small_stones_above_grey.png").convert_alpha()
    sprite_sheet_image = pg.image.load("Assets\walking_assets_player_friendly_1.png")
    hegn_til_anders = pg.image.load("Assets\HegnTilAnders.png")

# Events based on the game progress
PLAYER_HIT = pg.USEREVENT + 1

# Creates Text fonts 
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
LOSE_FONT = pg.font.SysFont('comicsans', 100)

#####################################################################################

# This class is to controll the animation of the character
class PlayerSpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale):
		image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
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
        

###################################################################################

def create_large_stone(terran_large_stone, large_stone_list):
    global screen_starter

    if len(large_stone_list) < 2:
        if screen_starter == 0:
            pos_x = random.randint(0, 1750)
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
def terran_sprite_creation(terran_large_stone, large_stone_list):
    global screen_starter
    if screen_starter > 0 and len(large_stone_list) < 2:
        random_num = random.randint(0, 400)
        if random_num == 19:
            return create_large_stone(terran_large_stone, large_stone_list)
        else:
            for sprite in large_stone_list:
                terran_large_stone.add(sprite)
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
        sprite.add_image()

# This updates the fence of the groups and draws them 
def add_image_first_lvl(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.add_image()

# This changes the speed of the stones
def sprite_movement_terran(sprite_group):
    for sprite in sprite_group:
        sprite.update_speed()

# Draws the content on the window
def draw_window(player, green_world_move, first_lvl_group, start_line, player_health, terran_large_stone, action, frame, new_x, new_y, animation_list):
    WIN.fill((BLACK))
    WIN.blit(GREEN_WORLD, (green_world_move.x, green_world_move.y))
    # The two if statements resolve in the moving background refresh
    WIN.blit(GREEN_WORLD, (green_world_move.x + WIDTH, green_world_move.y))
    if green_world_move.x <= -WIDTH:
        green_world_move.x = 0

    # This draws the start line 
    if start_line.x > -10:
        pg.draw.rect(WIN, RED, start_line)
    # This updates the sprites
    first_lvl_group.update()
    # This function here draws the fences
    add_image_first_lvl(first_lvl_group)
    # This lines under draws the sprites black 
    # first_lvl_group.draw(WIN)
    terran_large_stone.update()
    terran_large_stone.draw(WIN)
    # Displays health 
    player_health = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)

    WIN.blit(player_health, (10, 10))

    # This draws the player 
    # pg.draw.rect(WIN, BLACK, player)
    WIN.blit(animation_list[action][frame], ((player.x - 18) + new_x, (player.y - 18) + new_y))
    # This updates everything onto the screen
    pg.display.update()

def get_center_coords(image):
	rect_rotated = image.get_rect()
		
	center = rect_rotated.center

	new_x = 0 - center[0] + 37
	new_y = 0 - center[1] + 37
	return new_x, new_y

# This function creates the movement for the player
def player_movement(keys_pressed, player, image, last_update_player, animation_cooldown, frame, action, new_x, new_y):
    current_time = pg.time.get_ticks()
    if current_time - last_update_player >= animation_cooldown:
        frame += 1
        last_update_player = current_time
        if frame == 11: 
            frame = 0
    new_y = 0
    new_x = 0
    if not any(keys_pressed):
        action = 8
    # This controls straight walks
    if keys_pressed[pg.K_a] and player.x > 0:
        player.x -= PLAYER_VEL
        action = 2
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3:
        player.x += PLAYER_VEL
        action = 0 
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_w] and player.y > 0:
        player.y -= PLAYER_VEL
        action = 1
        new_y = 0
        new_x = 0
    if keys_pressed[pg.K_s] and player.y < HEIGHT - player_HEIGHT*3:
        player.y += PLAYER_VEL
        action = 3
        new_y = 0
        new_x = 0

    # This controls the side walk 
    if keys_pressed[pg.K_d] and keys_pressed[pg.K_w] and player.x < WIDTH - player_WIDTH*3 and player.y > 0:
        action = 4
        new_x, new_y = get_center_coords(image)
    if keys_pressed[pg.K_w] and keys_pressed[pg.K_a] and player.x > 0 and player.y > 0:
        action = 5
        new_x, new_y = get_center_coords(image)
    if keys_pressed[pg.K_a] and keys_pressed[pg.K_s] and player.x > 0 and player.y < HEIGHT - player_HEIGHT*3:
        action = 6
        new_x, new_y = get_center_coords(image)
    if keys_pressed[pg.K_s] and keys_pressed[pg.K_d] and player.x < WIDTH - player_WIDTH*3 and player.y < HEIGHT - player_HEIGHT*3:
        action = 7
        new_x, new_y = get_center_coords(image)
    
    return action, frame, new_x, new_y

# This function decides when the screen will move and how fast 
def screen_movement(player, green_world_move, action):
    global screen_starter
    if screen_starter >= 1 or player.x > 100: 
        green_world_move.x -= SCREEN_VEL
        screen_starter += 1
        if player.x > 0:
            player.x += -SCREEN_VEL
        if player.x <= 0: 
            action = 0
    
    return action

# This function check colission of objects and the player 
def player_hit(first_lvl_group, player):
    global hit_occured
    collided_sprites = [sprite 
                        for sprite in first_lvl_group 
                        if player.colliderect(sprite.rect)]
    if not hit_occured and len(collided_sprites) == 1:
        hit_occured = True
        pg.event.post(pg.event.Event(PLAYER_HIT))
    elif hit_occured and len(collided_sprites) < 1: 
        hit_occured = False

def large_stone_hit(first_lvl_group, terran_large_stone):
    # This line of code checks for collision between the two groups and removes the one from terran_large_stone chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, terran_large_stone, False, True)

def draw_lose(player, green_world_move, first_lvl_group, start_line, player_health,
               terran_large_stone, action, frame, new_x, new_y, animation_list):
    draw_window(player, green_world_move, first_lvl_group, start_line, player_health,
                 terran_large_stone, action, frame, new_x, new_y, animation_list)
    
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
    # List clearing to avoid large ram issues
    avoid_object_list.clear()
    large_stone_list.clear()
    # init of the starter variables
    distance_between_poles = 0
    screen_starter = 0
    player = pg.Rect(0, HEIGHT//2, 40, 40)
    start_line = pg.Rect(100, 0, 10, 800)
    first_lvl_group = pg.sprite.Group()
    terran_large_stone = pg.sprite.Group()
    green_world_move = pg.Rect(0, 0, WIDTH, HEIGHT)
    hit_count = 0
    player_health = 1

    # Counter for animation of character 
    sprite_sheet = PlayerSpriteSheet(sprite_sheet_image)
    last_update_player = pg.time.get_ticks()
    animation_cooldown = 75
    frame = 0 
    action = 8
    new_x = 0
    new_y = 0
    
    # Init function to save the animation images
    animation_list = extract_player_image(sprite_sheet)
    image = pg.transform.rotate(animation_list[0][0], 315)

    clock = pg.time.Clock()
    run = True

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
                # print(hit_count)
            
        # Draw if you lose
        if player_health <= 0: 
            draw_lose(player, green_world_move, first_lvl_group, start_line, player_health, terran_large_stone, action, frame, new_x, new_y, animation_list)
            break
        # These lines are for the sprites creation and updates 
        if screen_starter >= 1 or player.x > 100:
            first_lvl_group = sprite_creation_first_lvl(first_lvl_group)
            sprite_movement(first_lvl_group)
            start_line.x -= SCREEN_VEL
        
        terran_large_stone = terran_sprite_creation(terran_large_stone, large_stone_list)
        sprite_movement_terran(terran_large_stone)
        large_stone_hit(first_lvl_group, terran_large_stone)
        keys_pressed = pg.key.get_pressed()
        player_hit(first_lvl_group, player)



        action, frame, new_x, new_y = player_movement(keys_pressed, player, image, last_update_player,
                                                       animation_cooldown, frame, action, new_x, new_y)


        action = screen_movement(player, green_world_move, action)
        draw_window(player, green_world_move, first_lvl_group, start_line, player_health,
                     terran_large_stone, action, frame, new_x, new_y, animation_list)

    main()

if __name__ == "__main__":
    main()