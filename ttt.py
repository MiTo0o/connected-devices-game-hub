import pygame
import os
import RPi.GPIO as GPIO
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
QUIT_BUTTON = 17  # GPIO pin for the quit button
GPIO.setup(QUIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320
# Function to display pause pop-up
def show_pause_popup():
    # Create a font object
    font = pygame.font.Font(None, 36)
    
    # Render the pause message
    text = font.render("Game Paused", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    
    # Render the quit button
    quit_button_text = font.render("Quit", True, RED)
    quit_button_rect = quit_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    # Main loop for the pop-up window
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GPIO.cleanup()
                return
            elif event.type == pygame.FINGERDOWN:
                x, y = event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT
                # print(x, y)
                # print('quit', quit_button_rect)
                if quit_button_rect.collidepoint(x, y):
                    pygame.quit()
                    GPIO.cleanup()
                    return
        if GPIO.input(QUIT_BUTTON) == GPIO.HIGH:
            paused = False
        # Fill the screen with black background
        screen.fill(BLACK)
        
        # Draw the pause message onto the screen
        screen.blit(text, text_rect)
        
        # Draw the quit button
        screen.blit(quit_button_text, quit_button_rect)
        
        # Update the display
        pygame.display.flip()

# Initialize Pygame
pygame.init()


# Set PiTFT resolution
screen = pygame.display.set_mode((240, 320))

# Define Tic Tac Toe grid
grid = [['' for _ in range(3)] for _ in range(3)]

# Define cell size and padding
CELL_SIZE = 80
CELL_PADDING = 1

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Variable to track current player
current_player = 'X'

# Font for displaying current player
font = pygame.font.SysFont(None, 30)

# Function to check for a winner
def check_winner():
    for row in grid:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] != '':
            return grid[0][col]
    if grid[0][0] == grid[1][1] == grid[2][2] != '':
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != '':
        return grid[0][2]
    return None

# Function to check for a tie
def check_tie():
    for row in grid:
        for cell in row:
            if cell == '':
                return False
    return True

def draw_grid():
    # Draw Tic Tac Toe grid and symbols
    for y in range(3):
        for x in range(3):
            # Calculate cell position
            cell_x = x * (CELL_SIZE + CELL_PADDING)
            cell_y = y * (CELL_SIZE + CELL_PADDING)
            
            # Draw cell border
            pygame.draw.rect(screen, BLACK, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)
            
            # Calculate symbol position to center within cell
            symbol_x = cell_x + CELL_SIZE // 2
            symbol_y = cell_y + CELL_SIZE // 2
            
            if grid[y][x] == 'X':
                # Draw X symbol
                pygame.draw.line(screen, RED, (symbol_x - CELL_SIZE // 4, symbol_y - CELL_SIZE // 4),
                                (symbol_x + CELL_SIZE // 4, symbol_y + CELL_SIZE // 4), 5)
                pygame.draw.line(screen, RED, (symbol_x + CELL_SIZE // 4, symbol_y - CELL_SIZE // 4),
                                (symbol_x - CELL_SIZE // 4, symbol_y + CELL_SIZE // 4), 5)
            elif grid[y][x] == 'O':
                # Calculate circle radius based on cell size
                radius = min(CELL_SIZE // 3, CELL_SIZE // 3) // 2
                # Draw O symbol
                pygame.draw.circle(screen, RED, (symbol_x, symbol_y), radius, 5)


# Main loop
running = True
paused = False
while running:
    # Handle events
    if GPIO.input(QUIT_BUTTON) == GPIO.LOW:
        print('xdd')
        show_pause_popup()
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            # Get touch position from the event
            touch_x = event.x * screen.get_width()
            touch_y = event.y * screen.get_height()
            # Map touch position to game grid
            cell_x = int(touch_x) // (CELL_SIZE + CELL_PADDING)
            cell_y = int(touch_y) // (CELL_SIZE + CELL_PADDING)
            # Check if the cell is empty and it's the current player's turn
            if grid[cell_y][cell_x] == '' and (current_player == 'X' or current_player == 'O'):
                grid[cell_y][cell_x] = current_player
                winner = check_winner()
                if winner:
                    print(f"Player {winner} wins!")
                elif check_tie():
                    print("It's a tie!")
                else:
                    current_player = 'O' if current_player == 'X' else 'X'
        

    if not paused:
        screen.fill(WHITE)
        draw_grid()

        text = font.render("Turn: " + current_player, True, BLACK)
        screen.blit(text, (10, 300))
        pygame.display.flip()

    # # Clear the screen
    # screen.fill(WHITE)

    # Display current player
    # text = font.render("Turn: " + current_player, True, BLACK)
    # screen.blit(text, (10, 300))

    # # Update the display
    # pygame.display.flip()
    # print(grid)
# Quit Pygame
pygame.quit()
GPIO.cleanup()
