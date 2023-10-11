import pygame
import sys

# Initialize Pygame
pygame.init()

# Define table parameters
table_x = 50
table_y = 50
cell_width = 200
cell_height = 50
visible_rows = 5
total_players = 10  # Total number of players in the high score table

# Sample player data (replace with your own data)
player_data = [
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    {"name": "Player 1", "score": 100},
    {"name": "Player 2", "score": 85},
    
    # Add more player data here
]

# Set up display
screen_width = cell_width + 2 * table_x
screen_height = cell_height * visible_rows + 2 * table_y
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("High Score Table")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Function to draw the high score table
def draw_table(start_index):
    screen.fill(white)

    for i in range(visible_rows):
        index = start_index + i
        if index < len(player_data):
            player = player_data[index]
            y = table_y + i * cell_height
            pygame.draw.rect(screen, black, (table_x, y, cell_width, cell_height), 1)
            font = pygame.font.Font(None, 36)
            text = font.render(f"{player['name']} - {player['score']}", True, black)
            text_rect = text.get_rect(center=(table_x + cell_width / 2, y + cell_height / 2))
            screen.blit(text, text_rect)

# Main game loop
running = True
start_index = 0  # Start index for displaying players

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if start_index + visible_rows < len(player_data):
                    start_index += 1
            elif event.key == pygame.K_UP:
                if start_index > 0:
                    start_index -= 1

    draw_table(start_index)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
