import pygame as pg

def point_counter(point_timer_0):
    point_timer_1 = pg.time.get_ticks()
    point_count = (point_timer_1 - point_timer_0)//100

    return point_count

# This changes the speed of the stones
def sprite_movement_terran(sprite_group):
    for sprite in sprite_group:
        sprite.update_speed()
        sprite.draw()

# Draws the points
def point_object_update(point_carrots_group):
    for sprite in point_carrots_group:
        sprite.update_speed()
        sprite.draw_carrot()

# This updates the fence of the groups and draws them 
def first_lvl_update(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.add_image()

# This function uses a callback to the class to update the individual sprite location
def sprite_movement(first_lvl_group):
    for sprite in first_lvl_group:
        sprite.update_speed()

def large_stone_hit_fence(first_lvl_group, terran_large_stone):
    # This line of code checks for collision between the two groups and removes the one from terran_large_stone chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, terran_large_stone, False, True)

def carrot_hit_fence(first_lvl_group, point_carrots_group):
    # This line of code checks for collision between the two groups and removes the one from point_carrots_group chosen by the True, False.
    pg.sprite.groupcollide(first_lvl_group, point_carrots_group, False, True)