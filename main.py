import pygame
import random

pygame.font.init()

WIDTH, HEIGHT = 1800, 800

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PLAYER_VEL = 15
SCREEN_VEL = 6
screen_starter = 0
SPRITE_VEL = SCREEN_VEL
hit_occured = False 
avoid_object_list = []
distance_between_poles = 0

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes the first display and its size
pygame.display.set_caption('Player friendly.') # Makes caption 

player_WIDTH = 25
player_HEIGHT = 25

player = pygame.Rect(0, 0, player_WIDTH, player_HEIGHT)

#This is the main background 
GREEN_WORLD = pygame.transform.scale(pygame.image.load('Assets\GreenWorld.PNG'), (WIDTH, HEIGHT)) 

PLAYER_HIT = pygame.USEREVENT + 1


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
                avoid_object_list.pop()

def sprite_creation_top(first_lvl_group):
    global avoid_object_list
    global distance_between_poles
    #if len(object_list) < 10:
    # Top Sprite 
    sprite_width = 20
    sprite_pos_y = 0 - 10
    sprite_pos_x = WIDTH - distance_between_poles

    # Starting variables for objects 
    # Here the objects are written
    sprite_height = random.randint(100, 350)
    distance_between_poles -= 300
    object_number = avoid_object(sprite_width, sprite_height, sprite_pos_x, sprite_pos_y, (BLACK))
    avoid_object_list.append(object_number)

    # Bottom Sprite
    sprite_width = 20
    # Starting variables for objects 
    # Here the objects are written
    sprite_height = 800 - (sprite_height + 75)
    
    sprite_pos_y = HEIGHT - sprite_height + 20
    object_number = avoid_object(sprite_width, sprite_height, sprite_pos_x, sprite_pos_y, (BLACK))
    avoid_object_list.append(object_number)
    first_lvl_group.add(*avoid_object_list)
    
    return(first_lvl_group)
        

def sprite_movement(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.update_speed()

def draw_window(player, green_world_move, first_lvl_group, start_line):
    WIN.fill((BLACK))
    WIN.blit(GREEN_WORLD, (green_world_move.x, green_world_move.y))
   
    # The two if statements resolve in the moving background refresh
    if green_world_move.x < 0: 
        WIN.blit(GREEN_WORLD, (green_world_move.x + WIDTH, green_world_move.y))
    if green_world_move.x == -WIDTH:
        green_world_move.x = 0
    pygame.draw.rect(WIN, BLACK, player)

    if start_line.x > -10:
        pygame.draw.rect(WIN, RED, start_line)
    
    first_lvl_group.update()
    first_lvl_group.draw(WIN)
    
    pygame.display.update()


def player_movement(keys_pressed, player): 
    if keys_pressed[pygame.K_a] and player.x > 0:
        player.x -= PLAYER_VEL
    if keys_pressed[pygame.K_d] and player.x < WIDTH - player_WIDTH:
        player.x += PLAYER_VEL
    if keys_pressed[pygame.K_w] and player.y > 0:
        player.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s] and player.y < HEIGHT - player_HEIGHT:
        player.y += PLAYER_VEL


def screen_movement(player, green_world_move):
    global screen_starter
    if screen_starter >= 1 or player.x > 100: 
       green_world_move.x -= SCREEN_VEL
       screen_starter += 1

def player_hit(first_lvl_group, player):
    global hit_occured
    #print(hit_occured)
    collided_sprites = [sprite 
                        for sprite in first_lvl_group 
                        if player.colliderect(sprite.rect)]
    if not hit_occured and len(collided_sprites) == 1:
        hit_occured = True
        pygame.event.post(pygame.event.Event(PLAYER_HIT))
    elif hit_occured and len(collided_sprites) < 1: 
        hit_occured = False
    #print(len(collided_sprites))
    #print(hit_occured)

def main():
    global screen_starter
    start_line = pygame.Rect(100, 0, 10, 800)
    first_lvl_group = pygame.sprite.Group()
    green_world_move = pygame.Rect(0, 0, WIDTH, HEIGHT)
    hit_count = 0
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
                print(hit_count)
        
        if screen_starter >= 1 or player.x > 100: 
            first_lvl_group = sprite_creation_top(first_lvl_group)
            sprite_movement(first_lvl_group)
            start_line.x -= SCREEN_VEL
        

        keys_pressed = pygame.key.get_pressed()
        player_hit(first_lvl_group, player)
        player_movement(keys_pressed, player)
        screen_movement(player, green_world_move)
        draw_window(player, green_world_move, first_lvl_group, start_line)
        
if __name__ == "__main__":
    main()