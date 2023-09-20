import pygame as pg 

def extract_player_image_fall(sprite_sheet):
    temp_img_list = []
    animation_list = []

    for x in range(0, 4, -1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 35, 3))
    for x in range(0, 4, -1): 
        temp_img_list.append(sprite_sheet.get_image(x, 25, 35, 3))
    
    animation_list.append(temp_img_list)

    return animation_list

def extract_player_image(sprite_sheet): 
    temp_img_list = []
    animation_list = []

    for x in range(3):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(3, 0, -1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(4, 6):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))
    for x in range(6, 3, -1):
        temp_img_list.append(sprite_sheet.get_image(x, 25, 25, 3))

    animation_list.append(temp_img_list)


    for j in range(90, 360, 90):
        
        temp_img_list = []
        for x in range(11):
            image = pg.transform.rotate(animation_list[0][x], j)

            rect = image.get_rect()
            center = rect.center
            

            temp_img_list.append(image)

        animation_list.append(temp_img_list)

    for j in range(45, 360, 90):
        
        temp_img_list = []
        for x in range(11):
            image = pg.transform.rotate(animation_list[0][x], j)
            
            
            temp_img_list.append(image)
            
        animation_list.append(temp_img_list)


    temp_img_list = []
    for x in range(11): 
        image = temp_img_list.append(sprite_sheet.get_image(0, 25, 25, 3))
        
    animation_list.append(temp_img_list)

    return animation_list