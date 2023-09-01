import pygame

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')
sprite_sheet_image = pygame.image.load("walking_assets_player_friendly_1.png")

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale):
		image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))

		return image

sprite_sheet = SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)



# Create animation list 
last_update = pygame.time.get_ticks()
animation_cooldown = 50
frame = 0
animation_steps = [11, 11, 11, 11, 1]
action = 0

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
	print(j)
	temp_img_list = []
	for x in range(11):
		image = pygame.transform.rotate(animation_list[0][x], j)
		temp_img_list.append(image)

	animation_list.append(temp_img_list)



run = True
while run:

	#update background
	screen.fill(BG)

	#show frame image
	
	# update animation 
	current_time = pygame.time.get_ticks()

	if current_time - last_update >= animation_cooldown:
		frame += 1
		last_update = current_time
		if frame == 11: 
			frame = 0

	screen.blit(animation_list[action][frame], (0, 0))
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_a]:
		action = 2

	if keys_pressed[pygame.K_d]:
		action = 0 

	if keys_pressed[pygame.K_w]:
		action = 1
	
	if keys_pressed[pygame.K_s]:
		action = 3


	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()