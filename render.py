# animator.py

import pygame
import sys
from simulation import GridSetup
from config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, SPRITE_PATH,H
import math

class Animate(GridSetup):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.top_margin = 30
        self.screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + self.top_margin))
        pygame.display.set_caption("Magnetic Dipoles")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('Arial', 20)


        try:
            image = pygame.image.load(SPRITE_PATH).convert_alpha()
            image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

            color = pygame.Color(0)
            color = (255, 0, 0) 

            sprite = pygame.Surface(image.get_size())
            sprite.fill(color)

            self.particle_sprite = image.copy()

            self.particle_sprite.blit(sprite , (0, 0), special_flags = pygame.BLEND_MULT)

        except pygame.error:
            print(f"Error: {SPRITE_PATH} not found.")
            sys.exit()

    def run(self):
        while self.running:
            self.handle_events()
            for _ in range(1000):
                self.move()
                self.rotate()
            self.draw()
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):

        # self.screen.fill((255, 255, 255))
        self.screen.fill((0, 0, 0))
        
        self._draw_grid()
        for x, y in self.pos:
            id = self.grid[x, y]
            angle = math.degrees(math.atan2(-self.dipole[id][0], self.dipole[id][1]))

            rotated_sprite = pygame.transform.rotozoom(self.particle_sprite, angle, 1.0)
            self.screen.blit(rotated_sprite, (x * CELL_SIZE - CELL_SIZE/4, 
                                (GRID_HEIGHT-y)%GRID_HEIGHT * CELL_SIZE - CELL_SIZE/4 + self.top_margin))

        energy_text = self.font.render(f"Energy: {self.total_energy:.2f}      Magnetic filed(H) = {H}", True, (200, 200, 200))
        self.screen.blit(energy_text, (10, 10))



    def _draw_grid(self):
        color = (30, 30, 30)
        
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, color, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, color, (0, y), (GRID_WIDTH * CELL_SIZE, y))
