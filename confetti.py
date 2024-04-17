import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the Pygame window
screen_width = 240
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)

# Function to generate a confetti particle
def create_confetti_particle():
    x = random.randint(0, screen_width)
    y = -10
    size = random.randint(5, 10)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return {'x': x, 'y': y, 'size': size, 'color': color}
popup_displayed = False
# List to hold confetti particles
confetti_particles = []
def show_popup(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True,(0,0,0))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add a new confetti particle at random intervals
    if random.randint(0, 100) < 3:
        confetti_particles.append(create_confetti_particle())

    # Move and draw confetti particles
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text_surface = font.render('HALO', True,(0,0,0))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle['color'], (particle['x'], particle['y']), particle['size'])
        particle['y'] += 2  # Move particle downwards
        if particle['y'] > screen_height:  # Remove particles that fall off the screen
            confetti_particles.remove(particle)

    # if not popup_displayed:
    #     # show_popup('HALO')
    #     font = pygame.font.Font(None, 36)
    #     text_surface = font.render('HALO', True,(0,0,0))
    #     text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    #     screen.blit(text_surface, text_rect)
    #     popup_displayed = True

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
