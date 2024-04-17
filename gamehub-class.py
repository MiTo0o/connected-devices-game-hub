import pygame
import sys
from tic_tac_toe import TicTacToe

class GameHub:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((240, 320))
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.games = {
            "Tic Tac Toe": TicTacToe(self.screen),
            # Add more games here
        }
        self.selected_game = None
        self.game_icons = {
            "Tic Tac Toe": pygame.image.load("ttt_logo.png"),
            # Load icons for other games here
        }
        self.game_icon_size = (60, 60)
        self.game_icon_spacing = 20
        self.icon_x = 20
        self.icon_y = 20

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.screen.fill((255, 255, 255))
            self.draw_game_icons()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def draw_game_icons(self):
        x, y = self.icon_x, self.icon_y
        for game_name, icon in self.game_icons.items():
            self.screen.blit(pygame.transform.scale(icon, self.game_icon_size), (x, y))
            y += self.game_icon_size[1] + self.game_icon_spacing

    def handle_click(self, pos):
        x, y = pos
        for game_name, icon in self.game_icons.items():
            icon_rect = pygame.Rect(self.icon_x, self.icon_y, *self.game_icon_size)
            if icon_rect.collidepoint(x, y):
                self.selected_game = self.games[game_name]
                self.selected_game.run()
                self.selected_game = None
                break

if __name__ == "__main__":
    game_hub = GameHub()
    game_hub.run()
