# Dylan Mesho
# 06/17/2024

import pygame, sys, random, time
from pygame.locals import QUIT, SRCALPHA, USEREVENT, MOUSEBUTTONDOWN, KEYDOWN

pygame.init()

class Game:
    def __init__(self, window_width, window_height, window_name, fps):
        self.window_width, self.window_height = window_width, window_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(window_name)
        
        self.stopwatch = Stopwatch()
        self.fps = fps
        self.clock = pygame.time.Clock()
        
        self.targets_clicked = 0
        self.target_amount = 3
        self.targets = []
        for _ in range(self.target_amount):
            self.target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
            self.targets.append(self.target)
    
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
        self.stopwatch.start()
        if self.stopwatch.seconds >= 15:
            for target in self.targets:
                self.targets.remove(target)
            self.stopwatch.stop()
        time_text = self.stopwatch.get_time()
        self.screen.blit(pygame.font.SysFont('Arial', 30).render(time_text, True, (255, 0, 0)), (10, 40))
        
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def check_events(self):
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for target in self.targets:
                    if self.stopwatch.running:
                        if self.is_clicked(target, mouse_position):
                            self.targets_clicked += 1
                            self.targets.remove(target)
                            new_target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), target.radius)
                            self.targets.append(new_target)    
                   
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.stopwatch.running:
                        self.stopwatch.reset()
                        self.targets_clicked = 0
                        self.stopwatch.start()
                        for _ in range(self.target_amount):
                            target = Target(random.randrange(50, self.window_width - 50), random.randrange(50, self.window_height - 50), 50)
                            self.targets.append(target)
                    
class Target: 
    def __init__(self, coordinateX, coordinateY, radius):
        self.target_coordinate = [coordinateX, coordinateY]
        self.radius = radius
        self.surface = pygame.transform.scale(pygame.image.load('assets/target.png'), (self.radius * 2, self.radius * 2))
        self.rect = self.surface.get_rect(center=self.target_coordinate)
        self.mask = pygame.mask.from_surface(self.surface)

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False
        self.seconds = 0.0

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self._run()

    def _run(self):
        if self.running and self.elapsed_time < 15:
            self.elapsed_time = time.time() - self.start_time
            if self.elapsed_time >= 15:
                self.stop()
            time.sleep(0.01)

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False

    def get_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(self.elapsed_time, 60)
        milliseconds = (self.elapsed_time - int(self.elapsed_time)) * 1000
        self.seconds = seconds
        return f"{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"

game = Game(700, 500, 'Aim Game', 30)

while True:
    game.check_events()
    game.render()