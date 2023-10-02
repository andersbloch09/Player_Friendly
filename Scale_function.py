import pygame as pg

# This function calculates the scale factors for the screen
def calculate_scale_factors(game_width, game_height):
    # Define the target screen resolution (1920x1080)
    target_width = 1920
    target_height = 1080

    # Get the current screen resolution
    screen_info = pg.display.Info()
    #screen_width = screen_info.current_w
    #screen_height = screen_info.current_h

    screen_width = 2400
    screen_height = 1500



    if screen_width != target_width or screen_height != target_height:
        # Calculate the scaling factors
        x_scale = screen_width / game_width
        y_scale = screen_height / game_height
        scale_factor = max(x_scale, y_scale)
    else:
        scale_factor = 1

    print("Screen Size  = ", screen_width, screen_height, "      Scale Factor = ", scale_factor)

    return scale_factor