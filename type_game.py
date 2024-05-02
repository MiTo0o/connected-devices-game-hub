import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

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
    "__SPACE____DEL__"
]
key_positions = {k: (i, j) for j, row in enumerate(keys) for i, k in enumerate(row)}
key_size = (screen_width // 10, 40)
key_margin = 5

def draw_key(screen, key, position, key_size, is_special=False):
    x, y = position
    w, h = key_size
    pygame.draw.rect(screen, gray, (x, y, w, h))
    label = ' ' if key == '__SPACE__' else 'DEL' if key == '__DEL__' else key
    text_obj = font.render(label, True, black)
    text_rect = text_obj.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_obj, text_rect)

def draw_keyboard(screen, keys, key_positions, key_size, key_margin):
    start_y = screen_height - (len(keys) * (key_size[1] + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (key_size[0] + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            if key in ['__SPACE__', '__DEL__']:
                special_key_size = (key_size[0] * 5 if key == '__SPACE__' else key_size[0] * 2, key_size[1])
                draw_key(screen, key, (start_x + i * (key_size[0] + key_margin), start_y + j * (key_size[1] + key_margin)), special_key_size, is_special=True)
                if key == '__SPACE__':
                    i += 4  # Increment index for the large space key
                elif key == '__DEL__':
                    i += 1  # Increment index for the delete key
            else:
                draw_key(screen, key, (start_x + i * (key_size[0] + key_margin), start_y + j * (key_size[1] + key_margin)), key_size)

def check_key_press(x, y, key_positions, key_size, key_margin):
    start_y = screen_height - (len(keys) * (key_size[1] + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (key_size[0] + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            key_x, key_y = start_x + i * (key_size[0] + key_margin), start_y + j * (key_size[1] + key_margin)
            if key in ['__SPACE__', '__DEL__']:
                special_key_size = (key_size[0] * 5 if key == '__SPACE__' else key_size[0] * 2, key_size[1])
                if key_x <= x < key_x + special_key_size[0] and key_y <= y < key_y + special_key_size[1]:
                    return key
                if key == '__SPACE__':
                    i += 4  # Increment index for the large space key
                elif key == '__DEL__':
                    i += 1  # Increment index for the delete key
            elif key_x <= x < key_x + key_size[0] and key_y <= y < key_y + key_size[1]:
                return key
    return None

def render_text(screen, text, font, x, y, color):
    """Render text on the screen at specified position and color."""
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

# Main game loop
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            # Convert from normalized to absolute coordinates
            abs_x, abs_y = int(event.x * screen_width), int(event.y * screen_height)
            key_pressed = check_key_press(abs_x, abs_y, key_positions, key_size, key_margin)
            if key_pressed:
                if key_pressed == '__DEL__':
                    input_text = input_text[:-1]
                elif key_pressed == '__SPACE__':
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
