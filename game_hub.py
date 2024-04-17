import pygame

# Initialize Pygame
pygame.init()

# Set PiTFT resolution
screen = pygame.display.set_mode((240, 320))
pygame.mouse.set_visible(False)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Load game icons
game_icon_1 = pygame.image.load("ttt_logo.png")
game_icon_2 = pygame.image.load("connect_4_logo.png")
game_icon_3 = pygame.image.load("battleship_logo.png")
game_icon_4 = pygame.image.load("simon_logo.png")
# Load more game icons as needed...

# Resize game icons to 60x60 pixels
game_icon_1 = pygame.transform.scale(game_icon_1, (90, 90))
game_icon_2 = pygame.transform.scale(game_icon_2, (90, 90))
game_icon_3 = pygame.transform.scale(game_icon_3, (90, 90))
game_icon_4 = pygame.transform.scale(game_icon_4, (90, 90))
# Resize more game icons as needed...

# Set icon positions
icon_spacing = 20
icon_x = 20
icon_y = 95 # Adjusted position for game icons

# Set hub title
title_font = pygame.font.SysFont(None, 36)
title_text = title_font.render("Game Hub", True, BLACK)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check if the click is within the bounds of any game icon
            # Implement game selection logic here

    # Clear the screen
    screen.fill(WHITE)

    # Draw hub title
    title_rect = title_text.get_rect(center=(240 // 2, 40))
    screen.blit(title_text, title_rect)

    # Draw background for game icons
    pygame.draw.rect(screen, GRAY, (10, 80, 220, 230))

    # Blit game icons onto the screen
    screen.blit(game_icon_1, (icon_x, icon_y))
    screen.blit(game_icon_2, (icon_x, icon_y + 90 + icon_spacing))
    screen.blit(game_icon_3, (icon_x + 90 + icon_spacing, icon_y))
    screen.blit(game_icon_4, (icon_x + 90 + icon_spacing, icon_y + 90 + icon_spacing))

    # Blit more game icons as needed...

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
