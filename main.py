# Dylan Mesho
# 06/17/2024

import pygame, sys, random, time
from pygame.locals import QUIT, SRCALPHA, USEREVENT

pygame.init()

class Game:
    def __init__(self, window_width, window_height, window_name, fps):
        self.window_width, self.window_height = window_width, window_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(window_name)
        
        self.time_remaining = 30
        self.remaining_time = 0.0
        self.start_time = time.time()
        self.fps = fps
        self.clock = pygame.time.Clock()
        
        self.targets_clicked = 0
        self.target_amount = 3
        self.targets = []
        for _ in range(self.target_amount):
            self.target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
            self.targets.append(self.target)
    
    def stopwatch(self):
        remaining_time = max(0, self.time_remaining - (time.time() - self.start_time))
        self.remaining_time = remaining_time
        minutes, seconds = divmod(remaining_time, 60)
        milliseconds = int((remaining_time - int(remaining_time)) * 1000)
        time_str = "{:02}:{:02}:{:03}".format(int(minutes), int(seconds), milliseconds)
        self.screen.blit(pygame.font.SysFont('Arial', 30).render(time_str, True, (255, 0, 0)), (10, 50))
    
    def is_clicked(self, object, mouse_position):
        x, y = mouse_position[0] - object.rect.x, mouse_position[1] - object.rect.y
        if 0 <= x < object.rect.width and 0 <= y < object.rect.height and object.mask.get_at((x, y)):
            return True
    
    def draw_target(self):
        for target in self.targets:
            self.screen.blit(target.surface, target.rect)
        
    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.font.SysFont('Arial', 30).render(str(self.targets_clicked), True, (0, 255, 0)), (10, 10))
        self.draw_target()
        
        self.stopwatch()
        
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def check_events(self):
        mouse_position = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            for target in self.targets:       
                if self.is_clicked(target, mouse_position) and mouse[0] and self.remaining_time != 0:
                    self.targets_clicked += 1
                    self.targets.remove(target)
                    target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), target.radius)
                    self.targets.append(target)
                    
class Target: 
    def __init__(self, coordinateX, coordinateY, radius):
        self.target_coordinate = [coordinateX, coordinateY]
        self.radius = radius
        self.surface = pygame.transform.scale(pygame.image.load('assets/target.png'), (self.radius * 2, self.radius * 2))
        self.rect = self.surface.get_rect(center=self.target_coordinate)
        self.mask = pygame.mask.from_surface(self.surface)

game = Game(700, 500, 'Aim Game', 30)

while True:
    game.check_events()
    game.render()