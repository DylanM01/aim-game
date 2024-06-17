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
        
        self.sliders = [
            Slider((640, 480), (100, 20), 0.5, 0, 100)
        ]
    
    def is_clicked(self, object, mouse_position):
        x, y = mouse_position[0] - object.rect.x, mouse_position[1] - object.rect.y
        if 0 <= x < object.rect.width and 0 <= y < object.rect.height and object.mask.get_at((x, y)):
            return True
    
    def draw_target(self):
        self.screen.blit(self.target.surface, self.target.rect)
    
    def select_new_coordinates(self):
        self.target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
    
    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.font.SysFont('Arial', 30).render(str(self.targets_clicked), True, (0, 255, 0)), (10, 10))
        self.draw_target()
        
        for slider in self.sliders:
            pygame.draw.rect(self.screen, (0, 255, 0), slider.container_rect)
            pygame.draw.rect(self.screen, (0, 0, 255), slider.button_rect)
        
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def check_events(self):
        mouse_position = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if self.is_clicked(self.target, mouse_position) and mouse[0]:
                self.targets_clicked += 1
                self.select_new_coordinates()
                
            for slider in self.sliders:
                if slider.container_rect.collidepoint(mouse_position) and mouse[0]:
                    slider.move_slider(mouse_position)

class Target: 
    def __init__(self, coordinateX, coordinateY, radius):
        self.target_coordinate = [coordinateX, coordinateY]
        self.radius = radius
        
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), SRCALPHA)
        pygame.draw.circle(self.surface, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.surface.get_rect(center=self.target_coordinate)
        self.mask = pygame.mask.from_surface(self.surface)

class Slider:
    def __init__(self, position, size, initial_value, mininum_value, maximum_value):
        self.position = position
        self.size = size
        
        self.slider_left_position = self.position[0] - (size[0] / 2)
        self.slider_right_position = self.position[0] + (size[0] / 2)
        self.slider_top_position = self.position[1] - (size[1] / 2)
        
        self.minimum_value = mininum_value
        self.maximum_value = maximum_value
        self.initial_value = (self.slider_right_position - self.slider_left_position) * initial_value # percentage
        
        self.container_rect = pygame.Rect(self.slider_left_position, self.slider_top_position, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_position + self.initial_value - 5, self.slider_top_position, 10, self.size[1])
    
    def move_slider(self, mouse_position):
        self.button_rect.centerx = mouse_position[0]
    
    def get_value(self):
        value_range = self.slider_right_position - self.slider_left_position - 1
        button_value = self.button_rect.center - self.slider_left_position
        
        return (button_value / value_range) * (self.maximum_value - self.minimum_value) + self.minimum_value
        

game = Game(700, 500, 'Aim Game', 30)

while True:
    game.check_events()
    game.render()