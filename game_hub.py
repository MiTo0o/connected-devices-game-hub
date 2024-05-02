import pygame
from tic_tac_toe import TicTacToe
from simon_says import SimonSays

# Initialize Pygame
pygame.init()

# Set PiTFT resolution
screen = pygame.display.set_mode((240, 320))
pygame.mouse.set_visible(False)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
icon_size = 90
# Load game icons
tic_tac_toe = pygame.image.load("ttt_logo.png")
connect_4 = pygame.image.load("connect_4_logo.png")
battleship = pygame.image.load("battleship_logo.png")
simon_says = pygame.image.load("simon_logo.png")
# Load more game icons as needed...

# Resize game icons to 60x60 pixels
tic_tac_toe = pygame.transform.scale(tic_tac_toe, (90, 90))
connect_4 = pygame.transform.scale(connect_4, (90, 90))
battleship = pygame.transform.scale(battleship, (90, 90))
simon_says = pygame.transform.scale(simon_says, (90, 90))
# Resize more game icons as needed...

# Set icon positions
icon_spacing = 20
icon_x = 20
icon_y = 95 # Adjusted position for game icons

# Define icon bounding boxes
tic_tac_toe_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
connect_4_rect = pygame.Rect(icon_x, icon_y + 90 + icon_spacing, icon_size, icon_size)
battleship_rect = pygame.Rect(icon_x + 90 + icon_spacing, icon_y, icon_size, icon_size)
simon_rect = pygame.Rect(icon_x + 90 + icon_spacing, icon_y + 90 + icon_spacing, icon_size, icon_size)

# Set hub title
title_font = pygame.font.SysFont(None, 36)
title_text = title_font.render("Game Hub", True, BLACK)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            x, y = event.x * 240, event.y * 320

            if tic_tac_toe_rect.collidepoint(x,y):
                print('tic tac toe')
                ttt = TicTacToe(screen)
                ttt.run()

            elif connect_4_rect.collidepoint(x,y):
                print('connect 4')
                pass
            elif battleship_rect.collidepoint(x,y):
                print('battleship')
                pass
            elif simon_rect.collidepoint(x,y):
                print('simon')
                simon = SimonSays(screen)  # Pass the screen surface
                simon.run_game()
                pass

    # Clear the screen
    screen.fill(WHITE)

    # Draw hub title
    title_rect = title_text.get_rect(center=(240 // 2, 40))
    screen.blit(title_text, title_rect)

    # Draw background for game icons
    pygame.draw.rect(screen, GRAY, (10, 80, 220, 230))

    # Blit game icons onto the screen
    screen.blit(tic_tac_toe, (icon_x, icon_y))
    screen.blit(connect_4, (icon_x, icon_y + 90 + icon_spacing))
    screen.blit(battleship, (icon_x + 90 + icon_spacing, icon_y))
    screen.blit(simon_says, (icon_x + 90 + icon_spacing, icon_y + 90 + icon_spacing))

    # Blit more game icons as needed...

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
