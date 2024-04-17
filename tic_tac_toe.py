import pygame
import os
import RPi.GPIO as GPIO

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

class TicTacToe:
    def __init__(self, screen):
        self.screen = screen
        # Define Tic Tac Toe self.grid
        self.grid = [['' for _ in range(3)] for _ in range(3)]
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        self.QUIT_BUTTON = 17  # GPIO pin for the quit button
        GPIO.setup(self.QUIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.SCREEN_WIDTH = 240
        self.SCREEN_HEIGHT = 320
        # Define cell size and padding
        self.CELL_SIZE = 80
        self.CELL_PADDING = 1

        self.running = True
        self.paused = False

        # Variable to track current player
        self.current_player = 'X'

    def show_pause_popup(self):
        # Create a font object
        font = pygame.font.Font(None, 36)
        
        # Render the pause message
        text = font.render("Game Paused", True, RED)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        
        # Render the quit button
        quit_button_text = font.render("Quit", True, RED)
        quit_button_rect = quit_button_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        
        # Main loop for the pop-up window
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    GPIO.cleanup()
                    return
                elif event.type == pygame.FINGERDOWN:
                    x, y = event.x * self.SCREEN_WIDTH, event.y * self.SCREEN_HEIGHT
                    # print(x, y)
                    # print('quit', quit_button_rect)
                    if quit_button_rect.collidepoint(x, y):
                        self.running = False
                        GPIO.cleanup()
                        return
            if GPIO.input(self.QUIT_BUTTON) == GPIO.HIGH:
                self.paused = False
            # Fill the self.screen with black background
            self.screen.fill(BLACK)
            
            # Draw the pause message onto the self.screen
            self.screen.blit(text, text_rect)
            
            # Draw the quit button
            self.screen.blit(quit_button_text, quit_button_rect)
            
            # Update the display
            pygame.display.flip()

    # Function to check for a winner
    def check_winner(self):
        for row in self.grid:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] != '':
                return self.grid[0][col]
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != '':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != '':
            return self.grid[0][2]
        return None

    # Function to check for a tie
    def check_tie(self):
        for row in self.grid:
            for cell in row:
                if cell == '':
                    return False
        return True

    def draw_grid(self):
        # Draw Tic Tac Toe self.grid and symbols
        for y in range(3):
            for x in range(3):
                # Calculate cell position
                cell_x = x * (self.CELL_SIZE + self.CELL_PADDING)
                cell_y = y * (self.CELL_SIZE + self.CELL_PADDING)
                
                # Draw cell border
                pygame.draw.rect(self.screen, BLACK, (cell_x, cell_y, self.CELL_SIZE, self.CELL_SIZE), 3)
                
                # Calculate symbol position to center within cell
                symbol_x = cell_x + self.CELL_SIZE // 2
                symbol_y = cell_y + self.CELL_SIZE // 2
                
                if self.grid[y][x] == 'X':
                    # Draw X symbol
                    pygame.draw.line(self.screen, RED, (symbol_x - self.CELL_SIZE // 4, symbol_y - self.CELL_SIZE // 4),
                                    (symbol_x + self.CELL_SIZE // 4, symbol_y + self.CELL_SIZE // 4), 5)
                    pygame.draw.line(self.screen, RED, (symbol_x + self.CELL_SIZE // 4, symbol_y - self.CELL_SIZE // 4),
                                    (symbol_x - self.CELL_SIZE // 4, symbol_y + self.CELL_SIZE // 4), 5)
                elif self.grid[y][x] == 'O':
                    # Calculate circle radius based on cell size
                    radius = min(self.CELL_SIZE // 3, self.CELL_SIZE // 3) // 2
                    # Draw O symbol
                    pygame.draw.circle(self.screen, BLUE, (symbol_x, symbol_y), radius, 5)

    def run(self):
        while self.running:
            # Handle events
            if GPIO.input(self.QUIT_BUTTON) == GPIO.LOW:
                print('xdd')
                self.show_pause_popup()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.FINGERDOWN:
                        # Get touch position from the event
                        touch_x = event.x * self.screen.get_width()
                        touch_y = event.y * self.screen.get_height()
                        # Map touch position to game self.grid
                        cell_x = int(touch_x) // (self.CELL_SIZE + self.CELL_PADDING)
                        cell_y = int(touch_y) // (self.CELL_SIZE + self.CELL_PADDING)
                        # Check if the cell is empty and it's the current player's turn
                        if 0 <= cell_x < 3 and 0 <= cell_y < 3:
                            if self.grid[cell_y][cell_x] == '' and (self.current_player == 'X' or self.current_player == 'O'):
                                self.grid[cell_y][cell_x] = self.current_player
                                winner = self.check_winner()
                                if winner:
                                    print(f"Player {winner} wins!")
                                elif self.check_tie():
                                    print("It's a tie!")
                                else:
                                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                        
                if not self.paused:
                    self.screen.fill(WHITE)
                    self.draw_grid()

                    # Font for displaying current player
                    font = pygame.font.SysFont(None, 30)
                    text = font.render("Turn: " + self.current_player, True, BLACK)
                    self.screen.blit(text, (10, 300))
                    pygame.display.flip()
                
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchself.screen')
