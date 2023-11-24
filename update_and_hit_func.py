import pygame as pg
import time

def point_counter(point_timer_0, point_count, paused, point_count_paused):
    # Creates a variable to make sure the point_count does not get lost when pausing and then uses it again to reset when unpaused 
    # The variable has to be returned in order to be saved 
    if paused: 
        point_count_paused = point_count
    else: 
        point_scale = 13
        point_timer_1 = time.time()
        point_count = point_count_paused + ((point_timer_1 - point_timer_0) * point_scale) 
       
    return point_count, point_count_paused

# This changes the speed of the stones
def sprite_movement_terran(sprite_group):
    for sprite in sprite_group:
        sprite.update_speed()

# Draws the points
def point_object_update(point_carrots_group):
    for sprite in point_carrots_group:
        sprite.update_speed()

# This function uses a callback to the class to update the individual sprite location
def sprite_movement(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.update_speed()

def ui_draw(ui_button_group):
    for sprite in ui_button_group:
        sprite.draw_click()
        sprite.draw()

def draw_pause(WIN, WHITE, WIDTH, HEIGHT, PAUSED_FONT):
    text = PAUSED_FONT.render("Paused", 1, WHITE)
    WIN.blit(text, (WIDTH/2 - text.get_width() /
                        2, HEIGHT/2 - text.get_height()/2))

def large_stone_hit_fence(first_lvl_group, terran_large_stone):
    # This line of code checks for collision between the two groups and removes the one from terran_large_stone chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, terran_large_stone, False, True)

def carrot_hit_fence(first_lvl_group, point_carrots_group):
    # This line of code checks for collision between the two groups and removes the one from point_carrots_group chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, point_carrots_group, False, True)
