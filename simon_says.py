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
        self.screen = pygame.display.set_mode((240, 320))

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
            self.pi1.set_PWM_dutycycle(pin, 0)  # Turn off LED
            pygame.time.wait(500)  # Wait another 1 sec to ensure the lamp is completely off before showing the next color
           

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
                    elif self.GREEN_BUTTON_RECT.collidepoint(x, y):
                        self.player_sequence.append(GREEN)
                        player_input = True  # Player has inputted something
                        print("Green button pressed")
                    elif self.BLUE_BUTTON_RECT.collidepoint(x, y):
                        self.player_sequence.append(BLUE)
                        player_input = True  # Player has inputted something
                        print("Blue button pressed")
                    elif self.YELLOW_BUTTON_RECT.collidepoint(x, y):
                        self.player_sequence.append(YELLOW)
                        player_input = True  # Player has inputted something
                        print("Yellow button pressed")

            if player_input:
                if len(self.player_sequence) == len(self.sequence):
                    self.check_player_input()

            self.clock.tick(60)

if __name__ == "__main__":
    game = SimonSays()
    game.run_game()