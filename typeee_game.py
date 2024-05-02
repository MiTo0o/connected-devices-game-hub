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
time_limit = 80
score = 0
active = False

# Sample sentences
sentences = [
    "hello world this is a try to type this sentence",
    "try to type this sentence try to type this sentence",
    "the quick brown fox jumps try to type this sentence",
    "pygame is fun for building try to type this sentence",
    "accuracy over speed is often try to type this sentence"
]
current_sentence = random.choice(sentences)

# Keyboard setup
keys = [
    "QWERTYUIO",  # Ensures 'P' is on the screen by limiting keys per row to 10
    "ASDFGHJKP",   # Same here, 9 keys
    "ZXCVBNML",
    " -",

]
key_sizes = {
    'BKSPC': (screen_width // 5, 40),  # Backspace key size
    'SPACE': (3 * screen_width // 5, 40)  # Space key size, making it larger
}
key_margin = 5

def draw_key(screen, key, position, key_size):
    x, y = position
    w, h = key_size
    pygame.draw.rect(screen, gray, (x, y, w, h))
    label = '-' if key == '-' else ' ' if key == ' ' else key
    text_obj = font.render(label, True, black)
    text_rect = text_obj.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_obj, text_rect)

def draw_keyboard(screen, keys, key_margin):
    key_height = 40
    start_y = screen_height - (len(keys) * (key_height + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (screen_width // 10 + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            key_size = (screen_width // 10, key_height) if key not in key_sizes else key_sizes[key]
            draw_key(screen, key, (start_x + i * (screen_width // 10 + key_margin), start_y + j * (key_height + key_margin)), key_size)

def check_key_press(x, y, keys, key_margin):
    key_height = 40
    start_y = screen_height - (len(keys) * (key_height + key_margin) - key_margin)
    for j, row in enumerate(keys):
        start_x = (screen_width - (len(row) * (screen_width // 10 + key_margin) - key_margin)) // 2
        for i, key in enumerate(row):
            key_size = (screen_width // 10, key_height) if key not in key_sizes else key_sizes[key]
            key_x, key_y = start_x + i * (screen_width // 10 + key_margin), start_y + j * (key_height + key_margin)
            if key_x <= x < key_x + key_size[0] and key_y <= y < key_y + key_size[1]:
                # print(key)
                return key
    return None

def render_text(screen, text, font, x, y, color):
    """Render text on the screen at specified position and color, adjusting for two lines if needed."""
    screen_width = screen.get_width()
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
    text_obj = font.render(line1.strip(), True, color)
    screen.blit(text_obj, (x, y))
    if line2:  # Only render the second line if there's text to display
        text_obj = font.render(line2.strip(), True, color)
        screen.blit(text_obj, (x, y + font.get_height()))
# def render_text(screen, text, font, x, y, color):
#     """Render text on the screen at specified position and color."""
#     text_obj = font.render(text, True, color)
#     screen.blit(text_obj, (x, y))

# Main game loop
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.FINGERDOWN:
            # Convert from normalized to absolute coordinates
            abs_x, abs_y = int(event.x * screen_width), int(event.y * screen_height)
            key_pressed = check_key_press(abs_x, abs_y, keys, key_margin)
            if key_pressed:
                if key_pressed == '-':
                    input_text = input_text[:-1]
                elif key_pressed == ' ':
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

    # Render the current sentence
    if len(current_sentence) * font.size(' ')[0] > screen_width:
        # Scroll the sentence if it's too long to fit
        start_index = max(0, len(input_text) - 10)
        displayed_sentence = current_sentence[start_index:start_index + 20]
    else:
        displayed_sentence = current_sentence

    render_text(screen, displayed_sentence, font, 10, 10, black)

    # Render the user input
    render_text(screen, input_text, font, 10, 45, green if current_sentence.startswith(input_text) else red)

    # Render the timer
    render_text(screen, f"Time left: {int(time_limit - time_elapsed)}", font, 10, 75, black)

    # Render the score
    render_text(screen, f"Score: {score}", large_font, 10, 100, black)

    # Draw the keyboard
    draw_keyboard(screen, keys, key_margin)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
