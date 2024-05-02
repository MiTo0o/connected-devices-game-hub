import pygame
import random
import pigpio
import RPi.GPIO as GPIO

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

COLOR_NAMES = {
    RED: "RED",
    GREEN: "GREEN",
    BLUE: "BLUE",
    YELLOW: "YELLOW"
}
# Define color sequence
COLOR_SEQUENCE = [RED, GREEN, BLUE]

class SimonSays:
    def __init__(self,screen):
        self.screen = screen

        # Define cell size and padding
        self.CELL_SIZE = 80
        self.CELL_PADDING = 1

        self.running = True
        self.paused = False

        self.clock = pygame.time.Clock()
        self.sequence = []
        self.player_sequence = []
        self.round = 1
        self.playing = True

        self.pi1 = pigpio.pi()
        self.RED_PIN = 19
        self.BLUE_PIN = 13
        self.GREEN_PIN = 26
        
        self.pi1.set_mode(self.RED_PIN, pigpio.OUTPUT)
        self.pi1.set_mode(self.BLUE_PIN, pigpio.OUTPUT)
        self.pi1.set_mode(self.GREEN_PIN, pigpio.OUTPUT)

        GPIO.setmode(GPIO.BCM)
        self.QUIT_BUTTON = 17  # GPIO pin for the quit button
        GPIO.setup(self.QUIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.SCREEN_WIDTH = 240
        self.SCREEN_HEIGHT = 320
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
                        self.playing = False
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
        
    def generate_sequence(self):
        for _ in range(self.round):
            color = random.choice(COLOR_SEQUENCE)
            self.sequence.append(color)

    def display_sequence(self):
        color_names = [COLOR_NAMES[color] for color in self.sequence]
        print("Sequence Displayed:", color_names)
        for color in self.sequence:
            pin = self._color_to_pin(color)
            self.pi1.set_PWM_dutycycle(pin, 255)  
            pygame.time.wait(2000)  # Display each color for 2 secs
            self.pi1.set_PWM_dutycycle(pin, 1)  # Turn off LED
            pygame.time.wait(1000)  # Wait another 1 sec to ensure the lamp is completely off before showing the next color
           
    def check_player_input(self):
        if self.player_sequence == self.sequence:
            print("Correct!")
            font = pygame.font.SysFont(None, 30)
            result_text = "Correct!" if self.player_sequence == self.sequence else "Wrong!"
            result_render = font.render(result_text, True, BLACK)
            self.screen.blit(result_render, (10, 250))
            pygame.display.flip()
            self.round += 1
            self.player_sequence = []
            self.sequence = []
            self.generate_sequence()
            self.display_sequence()
        else:
            print("Wrong! Game Over")
            self.playing = False

    def _color_to_pin(self, color):
        if color == RED:
            print("red")
            return self.RED_PIN
        elif color == GREEN:
            print("green")
            return self.GREEN_PIN
        elif color == BLUE:
            print("blue")
            return self.BLUE_PIN
        else:
            return -1
    
    def run_game(self):
        self.generate_sequence()
        self.display_sequence()
        
        while self.playing:
            if GPIO.input(self.QUIT_BUTTON) == GPIO.LOW:
                self.show_pause_popup()
            else:
                player_input = False  # Flag to track if player has inputted something

                # Draw buttons on the screen
                self.screen.fill(WHITE)
                self.RED_BUTTON_RECT = pygame.draw.rect(self.screen, RED, (10, 10, 100, 100))
                self.GREEN_BUTTON_RECT = pygame.draw.rect(self.screen, GREEN, (130, 10, 100, 100))
                self.BLUE_BUTTON_RECT = pygame.draw.rect(self.screen, BLUE, (10, 130, 100, 100))
                self.YELLOW_BUTTON_RECT = pygame.draw.rect(self.screen, YELLOW, (130, 130, 100, 100))

                # Render round number
                font = pygame.font.SysFont(None, 30)
                round_text = "Round: " + str(self.round)
                round_render = font.render(round_text, True, BLACK)
                self.screen.blit(round_render, (10, 270))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                    elif event.type == pygame.FINGERDOWN:
                        x, y = event.x * 240, event.y * 320
                        if self.RED_BUTTON_RECT.collidepoint(x, y):
                            self.player_sequence.append(RED)
                            player_input = True  # Player has inputted something
                            print("Red button pressed")
                            self.pi1.set_PWM_dutycycle(self.RED_PIN, 255)
                            pygame.time.wait(250)
                            self.pi1.set_PWM_dutycycle(self.RED_PIN, 1)  
                        elif self.GREEN_BUTTON_RECT.collidepoint(x, y):
                            self.player_sequence.append(GREEN)
                            player_input = True  # Player has inputted something
                            print("Green button pressed")
                            self.pi1.set_PWM_dutycycle(self.GREEN_PIN, 255)
                            pygame.time.wait(250)
                            self.pi1.set_PWM_dutycycle(self.GREEN_PIN, 1) 
                        elif self.BLUE_BUTTON_RECT.collidepoint(x, y):
                            self.player_sequence.append(BLUE)
                            player_input = True  # Player has inputted something
                            print("Blue button pressed")
                            self.pi1.set_PWM_dutycycle(self.BLUE_PIN, 255)
                            pygame.time.wait(250)
                            self.pi1.set_PWM_dutycycle(self.BLUE_PIN, 1) 
                        elif self.YELLOW_BUTTON_RECT.collidepoint(x, y):
                            self.player_sequence.append(YELLOW)
                            player_input = True  # Player has inputted something
                            print("Yellow button pressed")

                if player_input:
                    if len(self.player_sequence) == len(self.sequence):
                        self.check_player_input()
                        pygame.time.wait(1000)
                self.clock.tick(60)

if __name__ == "__main__":
    game = SimonSays()
    game.run_game()