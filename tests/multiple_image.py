import pygame
import sys

pygame.init()

# Set up your screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite with Multiple Images")

# Define a custom Sprite class
class MultiImageSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, width, height, scale):
        super().__init__()

        # Initialize the sprite's image and rect
        self.index = 0  # Index for the current image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.image1 = pygame.transform.scale(image, (width * scale, height * scale))

    def update(self):
        # Update the sprite's image (animation logic)
        self.image = self.image1



# Load your images
image1 = pygame.image.load("Assets\HegnTilAnders.png")  # Replace with your image file paths
image2 = pygame.image.load("Assets\HegnTilAnders.png")
image3 = pygame.image.load("Assets\HegnTilAnders.png")

print("dimensions_of_image    = ", image1.get_size())
# Create a list of images for your sprite
sprite_images = [image1, image2, image3]

# Create a sprite group and add the sprite to it
all_sprites = pygame.sprite.Group()

j = 0

for sprite in sprite_images:
    multi_image_sprite = MultiImageSprite(sprite, (100, 100 + j), 20, 92, 1.5)
    all_sprites.add(multi_image_sprite)
    j += 130
    print(j)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Update the sprite (for animation)
    all_sprites.update()

    # Clear the screen
    screen.fill((0, 0, 0))  # Fill the screen with a black background color

    # Draw the sprite
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    clock.tick(10)  # Adjust the frame rate as needed
