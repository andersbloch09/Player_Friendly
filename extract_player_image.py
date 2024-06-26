import pygame as pg 

def extract_player_image_fall(sprite_sheet):
    temp_img_list = []
    animation_list = []

    for x in range(0, 5, 1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 35, 3.2))

    for x in range(6):
        temp_img_list.append(sprite_sheet.get_image(5, 25, 35, 3.2))

    for x in range(5, 0, -1): 
        temp_img_list.append(sprite_sheet.get_image(x, 25, 35, 3.2))

    animation_list.append(temp_img_list)
    
    temp_img_list = []
    for x in range(16):
        image = pg.transform.rotate(animation_list[0][x], 180)

        temp_img_list.append(image)

    animation_list.append(temp_img_list)
    

    return animation_list

def extract_player_image(sprite_sheet): 
    temp_img_list = []
    animation_list = []
    # This is for walking straight
    for x in range(3):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(3, 0, -1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(4, 6):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(6, 3, -1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))

    animation_list.append(temp_img_list)


    # This is for walking straight in the different directions 
    for j in range(90, 360, 90):
        temp_img_list = []
        for x in range(11):
            image = pg.transform.rotate(animation_list[0][x], j)
            
            temp_img_list.append(image)

        animation_list.append(temp_img_list)
    # This is for walking sideways in the different directions
    for j in range(45, 360, 90):
        
        temp_img_list = []
        for x in range(11):
            image = pg.transform.rotate(animation_list[0][x], j)
            
            
            temp_img_list.append(image)
            
        animation_list.append(temp_img_list)

    # Extracts still standning 
    temp_img_list = []
    for x in range(11): 
        image = temp_img_list.append(sprite_sheet.get_image(0, 25, 25, 3))
        
    animation_list.append(temp_img_list)
    
    # Extract invisible
    temp_img_list = []
    for x in range(11):
        image = sprite_sheet.get_image(0, 25, 25, 3)
        if image:
            image.set_alpha(0)
        temp_img_list.append(image)

    animation_list.append(temp_img_list)

    return animation_list


# gets center of the image for animation to match when running cross way
def get_center_coords(image, scale_factor):
	rect_rotated = image.get_rect()
		
	center = rect_rotated.center

	new_x = 0 - center[0] + int(37 * scale_factor)
	new_y = 0 - center[1] + int(37 * scale_factor)
	return new_x, new_y