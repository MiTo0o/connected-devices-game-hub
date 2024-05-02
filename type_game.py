import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing Game")

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
green = (0, 255, 0)
red = (255, 0, 0)
light_gray = (230, 230, 230)

# Set fonts
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 40)

# Game variables
running = True
clock = pygame.time.Clock()
input_text = ''
start_time = 0
time_limit = 60
score = 0
active = False

# Sample sentences
sentences = [
    "Hello world this is a typing test",
    "Try to type this sentence as fast as you can",
    "The quick brown fox jumps over the lazy dog",
    "Pygame is fun for building small games",
    "Accuracy over speed is often better"
]
current_sentence = random.choice(sentences)

# Keyboard setup
keys = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM",
    "<SPACE><DEL>"
]
key_positions = {k: (i, j) for j, row in enumerate(keys) for i, k in enumerate(row)}
key_size = (screen_width // 10, 40)
key_margin = 5

def draw_key(screen, key, position, key_size):
    x, y = position
    w, h = key_size
    pygame.draw.rect(screen, gray, (x, y, w, h))
    text_obj = font.render(key, True, black)
    text_rect = text_obj.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_obj, text_rect)

def draw_keyboard(screen, keys, key_positions, key_size, key_margin):
    start_y = screen_height - (len(keys) * (key_size[1] + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (key_size[0] + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            actual_key = ' ' if key == '<SPACE>' else '←' if key == '<DEL>' else key
            draw_key(screen, actual_key, (start_x + i * (key_size[0] + key_margin), start_y + j * (key_size[1] + key_margin)), key_size)

def check_key_press(pos, key_positions, key_size, key_margin):
    start_y = screen_height - (len(keys) * (key_size[1] + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (key_size[0] + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            key_x, key_y = start_x + i * (key_size[0] + key_margin), start_y + j * (key_size[1] + key_margin)
            if key_x <= pos[0] < key_x + key_size[0] and key_y <= pos[1] < key_y + key_size[1]:
                return key
    return None

def render_text(screen, text, font, x, y, color):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Main game loop
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            key_pressed = check_key_press([event.x, event.y], key_positions, key_size, key_margin)
            print(key_pressed)
            if key_pressed:
                if key_pressed == '<DEL>':
                    input_text = input_text[:-1]
                elif key_pressed == '<SPACE>':
                    input_text += ' '
                else:
                    input_text += key_pressed.lower()
                start_time = start_time or time.time()

    # Time management
    time_elapsed = time.time() - start_time if start_time else 0
    if time_elapsed > time_limit:
        active = False
        score += sum(1 for word in input_text.split() if word in current_sentence.split())
        current_sentence = random.choice(sentences)
        input_text = ''
        start_time = 0

    # Render the current sentence with grayed out text for the part that's already typed
    typed_length = len(input_text)
    rendered_sentence = current_sentence[:typed_length] + current_sentence[typed_length:]
    render_text(screen, rendered_sentence[:typed_length], font, 10, 10, light_gray)
    render_text(screen, rendered_sentence[typed_length:], font, 10 + font.size(rendered_sentence[:typed_length])[0], 10, black)

    # Render the user input
    render_text(screen, input_text, font, 10, 40, green if current_sentence.startswith(input_text) else red)

    # Render the timer
    render_text(screen, f"Time left: {int(time_limit - time_elapsed)}", font, 10, 70, black)

    # Render the score
    render_text(screen, f"Score: {score}", large_font, 10, 100, black)

    # Draw the keyboard
    draw_keyboard(screen, keys, key_positions, key_size, key_margin)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

