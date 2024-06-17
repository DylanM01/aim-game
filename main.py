# Dylan Mesho
# 06/17/2024

import pygame, sys, random
from pygame.locals import QUIT, MOUSEBUTTONDOWN, SRCALPHA

pygame.init()

class Game:
    def __init__(self, window_width, window_height, window_name, fps):
        self.window_width, self.window_height = window_width, window_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(window_name)
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        
        self.targets_clicked = 0
        self.target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
    
    def is_clicked(self, obj, mouse_pos):
        x, y = mouse_pos[0] - obj.rect.x, mouse_pos[1] - obj.rect.y
        if 0 <= x < obj.rect.width and 0 <= y < obj.rect.height and obj.mask.get_at((x, y)):
            return True
    
    def draw_target(self):
        self.screen.blit(self.target.surface, self.target.rect)
    
    def select_new_coordinates(self):
        self.target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.font.SysFont('Arial', 30).render(str(self.targets_clicked), True, (20, 255, 20)), (10, 10))
        self.draw_target()
        
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if self.is_clicked(self.target, event.pos):
                    self.targets_clicked += 1
                    self.select_new_coordinates()

class Target: 
    def __init__(self, coordinateX, coordinateY, radius):
        self.target_coordinate = [coordinateX, coordinateY]
        self.radius = radius
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), SRCALPHA)
        pygame.draw.circle(self.surface, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.surface.get_rect(center=self.target_coordinate)
        self.mask = pygame.mask.from_surface(self.surface)

game = Game(700, 500, 'Aim Game', 30)

while True:
    game.check_events()
    game.render()