import pygame

pygame.init()

available_fonts = pygame.font.get_fonts()
for font in available_fonts:
    print(font)
