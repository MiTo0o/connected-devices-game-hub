import pygame
import random
import time
import pigpio
import RPi.GPIO as GPIO

class Type_Racer:
    def __init__(self, screen):
        pygame.init()

        self.pi1 = pigpio.pi()
        self.RED_PIN = 19
        self.BLUE_PIN = 13
        self.GREEN_PIN = 26
        self.pi1.set_mode(self.RED_PIN, pigpio.OUTPUT)
        self.pi1.set_mode(self.BLUE_PIN, pigpio.OUTPUT)
        self.pi1.set_mode(self.GREEN_PIN, pigpio.OUTPUT)

        self.pi1.write(self.RED_PIN, 0)
        self.pi1.write(self.BLUE_PIN, 0)
        self.pi1.write(self.GREEN_PIN, 0)
        # Set up the display
        self.screen_width = 240
        self.screen_height = 320
        self.screen = screen

        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        self.QUIT_BUTTON = 17  # GPIO pin for the quit button
        GPIO.setup(self.QUIT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.QUIT_BUTTON = 17
        # Set colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gray = (200, 200, 200)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.light_gray = (230, 230, 230)

        # Set fonts
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 40)

        # Game variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.input_text = ''
        self.start_time = 0
        self.time_limit = 50
        self.score = 0
        self.active = False

        self.sentences = [
            "hello world this is a try to type this sentence",
            "try to type this sentence try to type this sentence",
        ]
        self.current_sentence = random.choice(self.sentences)
        
        self.keys = [
            "QWERTYUIO",  # Ensures 'P' is on the screen by limiting keys per row to 10
            "ASDFGHJKP",   # Same here, 9 keys
            "ZXCVBNML",
            " -",
        ]
        
        self.key_sizes = {
            'BKSPC': (self.screen_width // 5, 40),  # Backspace key size
            'SPACE': (3 * self.screen_width // 5, 40)  # Space key size, making it larger
        }
        self.key_margin = 5

    def show_pause_popup(self):
        # Create a font object
        font = pygame.font.Font(None, 36)
        # Render the pause message
        text = font.render("Game Paused", True, self.red)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))    
        # Render the quit button
        quit_button_text = font.render("Quit", True, self.red)
        quit_button_rect = quit_button_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50)) 
        # Main loop for the pop-up window
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    GPIO.cleanup()
                    return
                elif event.type == pygame.FINGERDOWN:
                    x, y = event.x * self.screen_width, event.y * self.screen_height
                    # print(x, y)
                    # print('quit', quit_button_rect)
                    if quit_button_rect.collidepoint(x, y):
                        self.running = False
                        GPIO.cleanup()
                        return
            if GPIO.input(self.QUIT_BUTTON) == GPIO.HIGH:
                self.paused = False
            # Fill the self.screen with black background
            self.screen.fill(self.black)        
            # Draw the pause message onto the self.screen
            self.screen.blit(text, text_rect)          
            # Draw the quit button
            self.screen.blit(quit_button_text, quit_button_rect)          
            # Update the display
            pygame.display.flip()

    def draw_key(self, screen, key, position, key_size):
        x, y = position
        w, h = key_size
        pygame.draw.rect(self.screen, self.gray, (x, y, w, h))
        label = '-' if key == '-' else ' ' if key == ' ' else key
        text_obj = self.font.render(label, True, self.black)
        text_rect = text_obj.get_rect(center=(x + w / 2, y + h / 2))
        screen.blit(text_obj, text_rect)

    def draw_keyboard(self, screen, keys, key_margin):
        key_height = 40
        start_y = self.screen_height - (len(self.keys) * (key_height + key_margin) - key_margin)
        for j, row in enumerate(keys):
            start_x = (self.screen_width - (len(row) * (self.screen_width // 10 + key_margin) - key_margin)) // 2
            for i, key in enumerate(row):
                self.key_size = (self.screen_width // 10, key_height) if key not in self.key_sizes else self.key_sizes[key]
                self.draw_key(self.screen, key, (start_x + i * (self.screen_width // 10 + key_margin), start_y + j * (key_height + key_margin)), self.key_size)

    def check_key_press(self, x, y, keys, key_margin):
        key_height = 40
        start_y = self.screen_height - (len(keys) * (key_height + key_margin) - key_margin)
        for j, row in enumerate(keys):
            start_x = (self.screen_width - (len(row) * (self.screen_width // 10 + key_margin) - key_margin)) // 2
            for i, key in enumerate(row):
                self.key_size = (self.screen_width // 10, key_height) if key not in self.key_sizes else key_sizes[key]
                key_x, key_y = start_x + i * (self.screen_width // 10 + key_margin), start_y + j * (key_height + key_margin)
                if key_x <= x < key_x + self.key_size[0] and key_y <= y < key_y + self.key_size[1]:
                    # print(key)
                    return key
        return None

    def render_text(self, screen, text, font, x, y, color):
        """Render text on the screen at specified position and color, adjusting for two lines if needed."""
        screen_width = self.screen.get_width()
        words = text.split()
        line1 = ''
        line2 = ''
        current_length = 0

        # Try to fit words into two lines
        for word in words:
            word_length = font.size(word + ' ')[0]
            if current_length + word_length < screen_width:
                line1 += word + ' '
                current_length += word_length
            else:
                line2 += word + ' '

        # Render the lines
        text_obj = self.font.render(line1.strip(), True, color)
        screen.blit(text_obj, (x, y))
        if line2:  # Only render the second line if there's text to display
            text_obj = self.font.render(line2.strip(), True, color)
            self.screen.blit(text_obj, (x, y + font.get_height()))
    def run(self):
        # Main game loop
        while self.running:
            if GPIO.input(self.QUIT_BUTTON) == GPIO.LOW:
                self.show_pause_popup()
            else:
                self.screen.fill(self.white)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.FINGERDOWN:
                        # Convert from normalized to absolute coordinates
                        abs_x, abs_y = int(event.x * self.screen_width), int(event.y * self.screen_height)
                        key_pressed = self.check_key_press(abs_x, abs_y, self.keys, self.key_margin)
                        if key_pressed:
                            if key_pressed == '-':
                                self.input_text = self.input_text[:-1]
                            elif key_pressed == ' ':
                                self.input_text += ' '
                            else:
                                self.input_text += key_pressed.lower()
                            self.start_time = self.start_time or time.time()

                # Time management
                self.time_elapsed = time.time() - self.start_time if self.start_time else 0
                if self.time_elapsed > self.time_limit:
                    self.active = False
                    self.score += sum(1 for word in self.input_text.split() if word in self.current_sentence.split())
                    self.current_sentence = random.choice(self.sentences)
                    self.input_text = ''
                    self.start_time = 0

                # Render the current sentence
                if len(self.current_sentence) * self.font.size(' ')[0] > self.screen_width:
                    # Scroll the sentence if it's too long to fit
                    start_index = max(0, len(self.input_text) - 10)
                    displayed_sentence = self.current_sentence[start_index:start_index + 20]
                else:
                    displayed_sentence = self.current_sentence

                self.render_text(self.screen, displayed_sentence, self.font, 10, 7, self.black)
                correct = self.current_sentence.startswith(self.input_text)
                # Render the user input
                self.render_text(self.screen, self.input_text, self.font, 10, 45, self.green if correct else self.red)
                if correct:
                    self.pi1.write(self.RED_PIN, 0)
                    self.pi1.write(self.GREEN_PIN, 1)
                else:
                    self.pi1.write(self.GREEN_PIN, 0)
                    self.pi1.write(self.RED_PIN, 1)

                # Render the timer
                self.render_text(self.screen, f"Time left: {int(self.time_limit - self.time_elapsed)}", self.font, 10, 85, self.black)

                # Render the score
                self.render_text(self.screen, f"Score: {self.score}", self.large_font, 10, 110, self.black)

                # Draw the keyboard
                self.draw_keyboard(self.screen, self.keys, self.key_margin)

                pygame.display.flip()
                self.clock.tick(30)

