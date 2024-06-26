import pygame
import pygame.locals as pl
import pygame_textinput as pt
import time

pygame.init()

# No arguments needed to get started
textinput = pt.TextInputVisualizer()

# But more customization possible: Pass your own font object
font = pygame.font.SysFont("Consolas", 55)
# Create own manager with custom input validator
manager = pt.TextInputManager(validator = lambda input: len(input) <= 5)
# Pass these to constructor
textinput_custom = pt.TextInputVisualizer(manager=manager, font_object=font)
# Customize much more
textinput_custom.cursor_width = 4
textinput_custom.cursor_blink_interval = 400 # blinking interval in ms
textinput_custom.antialias = False
textinput_custom.font_color = (0, 85, 170)

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)

def simulate_key_press(key):
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    pygame.event.post(event)

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)
    textinput_custom.update(events)

    # Get its surface to blit onto the screen
    screen.blit(textinput.surface, (10, 10))
    screen.blit(textinput_custom.surface, (10, 50))

    # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
    textinput_custom.font_color = [(c+10)%255 for c in textinput_custom.font_color]

    # Check if user is exiting or pressed return
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    
    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_BACKSPACE]:
        print(keys_pressed)
        if keys_pressed[pygame.K_BACKSPACE]:
            simulate_key_press(pygame.K_BACKSPACE)


        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(f"User pressed enter! Input so far: {textinput.value}")

    pygame.display.update()
    clock.tick(30)
    