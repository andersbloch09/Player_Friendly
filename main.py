import pygame
import random
import platform

pygame.font.init()

# Width and Height of window 
WIDTH, HEIGHT = 1800, 800

# Here are all the used global variables 
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PLAYER_VEL = 12
SCREEN_VEL = 6
SPRITE_VEL = SCREEN_VEL
screen_starter = 0
hit_occured = False 
distance_between_poles = 0
avoid_object_list = []

# Makes the first display and its size
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
# Makes caption 
pygame.display.set_caption('Player friendly.')

# Player size of rect
player_WIDTH = 25
player_HEIGHT = 25

player = pygame.Rect(0, 0, player_WIDTH, player_HEIGHT)

#This is the main background 
system_type = platform.system()

if system_type == "Darwin":
    print("macOS")
    GREEN_WORLD = pygame.transform.scale(pygame.image.load('Assets/GreenWorld.PNG'), (WIDTH, HEIGHT)) 
elif system_type == "Windows":
    print("Windows")
    GREEN_WORLD = pygame.transform.scale(pygame.image.load('Assets\GreenWorld.PNG'), (WIDTH, HEIGHT)) 

# Events based on the game progress
PLAYER_HIT = pygame.USEREVENT + 1

# Creates Text fonts 
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
LOSE_FONT = pygame.font.SysFont('comicsans', 100)

# Class for creation of sprites for poles 
class avoid_object(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.speed = SPRITE_VEL

    def update_speed(self):
        global screen_starter
        if screen_starter >= 1 or player.x > 100:
            self.rect.x -= self.speed
            if self.rect.x <= -10:
                self.kill()
                

# Function which creates the sprites both on bottom and on top
def sprite_creation(first_lvl_group):
    global distance_between_poles
    global avoid_object_list
    # Top Sprite 
    sprite_width = 20
    sprite_pos_y = 0 - 10
    sprite_pos_x = WIDTH - distance_between_poles
    print(distance_between_poles)
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

# This function uses a callback to the class to update the individual sprite location
def sprite_movement(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.update_speed()

# Draws the content on the window
def draw_window(player, green_world_move, first_lvl_group, start_line, player_health):
    WIN.fill((BLACK))
    WIN.blit(GREEN_WORLD, (green_world_move.x, green_world_move.y))
    # The two if statements resolve in the moving background refresh
    if green_world_move.x < 0: 
        WIN.blit(GREEN_WORLD, (green_world_move.x + WIDTH, green_world_move.y))
    if green_world_move.x == -WIDTH:
        green_world_move.x = 0
    # This draws the player 
    pygame.draw.rect(WIN, BLACK, player)
    # This draws the start line 
    if start_line.x > -10:
        pygame.draw.rect(WIN, RED, start_line)
    # This updates the sprites 
    first_lvl_group.update()
    first_lvl_group.draw(WIN)
    
    # Displays health 
    player_health = HEALTH_FONT.render(
        "Health: " + str(player_health), 1, WHITE)

    WIN.blit(player_health, (10, 10))

    # This updates everything onto the screen
    pygame.display.update()

# This function creates the movement for the player
def player_movement(keys_pressed, player): 
    if keys_pressed[pygame.K_a] and player.x > 0:
        player.x -= PLAYER_VEL
    if keys_pressed[pygame.K_d] and player.x < WIDTH - player_WIDTH:
        player.x += PLAYER_VEL
    if keys_pressed[pygame.K_w] and player.y > 0:
        player.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s] and player.y < HEIGHT - player_HEIGHT:
        player.y += PLAYER_VEL

# This function decides when the screen will move and how fast 
def screen_movement(player, green_world_move):
    global screen_starter
    if screen_starter >= 1 or player.x > 100: 
       green_world_move.x -= SCREEN_VEL
       screen_starter += 1

# This function check colission of objects and the player 
def player_hit(first_lvl_group, player):
    global hit_occured
    collided_sprites = [sprite 
                        for sprite in first_lvl_group 
                        if player.colliderect(sprite.rect)]
    if not hit_occured and len(collided_sprites) == 1:
        hit_occured = True
        pygame.event.post(pygame.event.Event(PLAYER_HIT))
    elif hit_occured and len(collided_sprites) < 1: 
        hit_occured = False

def draw_lose(player, green_world_move, first_lvl_group, start_line, player_health):
    draw_window(player, green_world_move, first_lvl_group, start_line, player_health)
    
    draw_text = LOSE_FONT.render("LOSER!", 1, RED)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global screen_starter
    global player
    global distance_between_poles
    avoid_object_list.clear()
    distance_between_poles = 0
    screen_starter = 0
    player = pygame.Rect(0, 0, player_WIDTH, player_HEIGHT)
    start_line = pygame.Rect(100, 0, 10, 800)
    first_lvl_group = pygame.sprite.Group()
    green_world_move = pygame.Rect(0, 0, WIDTH, HEIGHT)
    hit_count = 0
    player_health = 1

    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == PLAYER_HIT:
                hit_count += 1
                player_health -= 1
                print(hit_count)
        # Draw if you lose
        if player_health <= 0: 
            draw_lose(player, green_world_move, first_lvl_group, start_line, player_health)
            break
        # These lines are for the sprites creation and updates 
        if screen_starter >= 1 or player.x > 100: 
            first_lvl_group = sprite_creation(first_lvl_group)
            sprite_movement(first_lvl_group)
            start_line.x -= SCREEN_VEL
        
        keys_pressed = pygame.key.get_pressed()
        player_hit(first_lvl_group, player)
        player_movement(keys_pressed, player)
        screen_movement(player, green_world_move)
        draw_window(player, green_world_move, first_lvl_group, start_line, player_health)

    main()

if __name__ == "__main__":
    main()