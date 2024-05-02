import pygame
import json
import pigpio
import RPi.GPIO as GPIO
import random
import paho.mqtt.client as mqtt
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

GAME_STATE_TOPIC = "game/state"
GAME_WINNER_TOPIC = "game/winner"

# Initialize MQTT client
client = mqtt.Client()
client.connect("localhost", 1883) #change the broker address to the ip address of the server device
client.subscribe(GAME_STATE_TOPIC)
client.subscribe(GAME_WINNER_TOPIC)


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
        self.winner = None
        self.clock = pygame.time.Clock()
        # Variable to track current player
        self.current_player = 'O'
        self.confetti_particles = []
        self.button_rects = []
        self.disabled = True
        self.player = "O"
        client.on_message = self.on_message
        client.loop_start()

        self.pi1 = pigpio.pi()
        self.RED_PIN = 19
        self.BLUE_PIN = 13
        self.pi1.set_mode(self.RED_PIN, pigpio.OUTPUT)
        self.pi1.set_mode(self.BLUE_PIN, pigpio.OUTPUT)


    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        print(payload)
        if topic == GAME_STATE_TOPIC:
            new_info = json.loads(payload)
            self.grid = new_info["grid"] 
            if new_info["player"] == self.player:
               self.disabled = True
            else:
               self.disabled = False
        elif topic == GAME_WINNER_TOPIC:
            # Display the winner
            print("Winner:", payload)

    def switch_light_color(self):
        if self.current_player == 'X':
            self.pi1.write(self.RED_PIN, 0)
            self.pi1.write(self.BLUE_PIN, 1)
        else:
            self.pi1.write(self.RED_PIN, 1)
            self.pi1.write(self.BLUE_PIN, 0)

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

    def create_confetti_particle(self):
        x = random.randint(0, self.SCREEN_WIDTH)
        y = -10
        size = random.randint(5, 10)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return {'x': x, 'y': y, 'size': size, 'color': color}

    def end_pop_up(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        font = pygame.font.SysFont(None, 30)
        text = font.render("Turn: " + self.current_player, True, BLACK)
        self.screen.blit(text, (10, 300))
        
        # Calculate the size and position of the rectangle
        rect_width = 200
        rect_height = 100
        rect_x = (self.SCREEN_WIDTH - rect_width) // 2
        rect_y = (self.SCREEN_HEIGHT - rect_height) // 2
        
        # Draw the rectangle
        pygame.draw.rect(self.screen, (50, 50, 50), (rect_x, rect_y, rect_width, rect_height))
        
        # Render the text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.winner, True, (255, 255, 255))  # White text color
        text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Button to return to main menu
        button_text = font.render("Main Menu", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.SCREEN_WIDTH // 2, rect_y + rect_height + 30))
        pygame.draw.rect(self.screen, (50, 50, 50), button_rect)
        self.screen.blit(button_text, button_rect)
        if button_rect not in self.button_rects:
            self.button_rects.append(button_rect)

        # Button to start another game
        button_text = font.render("Start New Game", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.SCREEN_WIDTH // 2, rect_y + rect_height + 70))
        pygame.draw.rect(self.screen, (50, 50, 50), button_rect)
        self.screen.blit(button_text, button_rect)
        if button_rect not in self.button_rects:
            self.button_rects.append(button_rect)
            
        # Update the display
        self.update_confetti()  
        pygame.display.flip()

    def update_confetti(self):
        if random.randint(0, 100) < 3:
            self.confetti_particles.append(self.create_confetti_particle())

        for particle in self.confetti_particles:
            pygame.draw.circle(self.screen, particle['color'], (particle['x'], particle['y']), particle['size'])
            particle['y'] += 2  # Move particle downwards
            if particle['y'] > self.SCREEN_HEIGHT:  # Remove particles that fall off the screen
                self.confetti_particles.remove(particle)


    def end_screen(self):
        local_running = True
        while local_running:
            self.end_pop_up()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    local_running = False
                elif event.type == pygame.FINGERDOWN:
                    for button_rect in self.button_rects:
                        if button_rect.collidepoint(event.x * 240, event.y* 320):
                            if button_rect == self.button_rects[0]:
                                print("Return to main menu button pressed")
                                self.running = False
                                GPIO.cleanup()
                                return
                            elif button_rect == self.button_rects[1]:
                                print("Start new game button pressed")

                                self.confetti_particles = []
                                self.button_rects = []
                                self.grid = [['' for _ in range(3)] for _ in range(3)]
                                self.winner = None
                                return
            self.clock.tick(60)
               
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
                        if self.disabled == False:
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
                                        self.winner = f"Player {winner} wins!"
                                        client.publish(GAME_WINNER_TOPIC, self.winner)
                                    elif self.check_tie():
                                        print("It's a tie!")
                                        self.winner = "It's a tie!"
                                    else:
                                        info = {
                                            "grid": self.grid,
                                            "player": self.player
                                        }
                                        client.publish(GAME_STATE_TOPIC, json.dumps(info))
                                        self.switch_light_color()

                if self.winner:
                    self.end_screen()        
                if not self.paused:
                    self.screen.fill(WHITE)
                    self.draw_grid()

                    # Font for displaying current player
                    font = pygame.font.SysFont(None, 30)
                    text = font.render("Turn: " + self.current_player, True, BLACK)
                    self.screen.blit(text, (10, 300))
                    pygame.display.flip()

    
                

                
