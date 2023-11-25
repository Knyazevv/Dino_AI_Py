import pygame
import random
import math
from enum import Enum


width = 1280
height = 720
bg = (255, 255, 255, 255)

score = 0
score_speed = 100
game_speed = 5.0


class DinoState(Enum):
    RUN = 1
    JUMP = 2


class Dino():
    name = 'Dino'
    jump_power = 10
    cur_jump_power = jump_power
    color = 'default'
    sprites = {
        'run': [],
        'jump': [],
    }
    image = None
    run_animation_index = [0, 5]
    hitbox = None
    state = DinoState.RUN

    def __init__(self, x, y, color='default', name='Dino',):
        self.name = name
        self.load_sprites()
        self.hitbox = pygame.Rect(
            x, y, self.sprites['run'][0].get_width(), self.sprites['run'][0].get_height())
        self.image = self.sprites['run'][0]

        if name is None:
            self.name = name

    def load_sprites(self):
        self.sprites['run'].append(pygame.image.load(
            f'sprites/dino/{self.color}_run1.png'))
        self.sprites['run'].append(pygame.image.load(
            f'sprites//dino/{self.color}_run2.png'))
        self.sprites['jump'].append(pygame.image.load(
            f'sprites/dino/{self.color}_jump.png'))

    def draw(self, src, fnt=None):
        src.blit(self.image, (self.hitbox.x, self.hitbox.y))

        if fnt is not None:
            c_lable = fnt.render(self.name.capitalize(), True, (100, 100, 100))
            c_lable_rect = c_lable.get_rect()
            c_lable_rect.center = (self.hitbox.x + 45, self.hitbox.y - 30)
            src.blit(c_lable, c_lable_rect)

    def run(self):
        self.sprites['run'].append(pygame.image.load(
            f'sprites/dino/{self.color}_run1.png'))
        self.sprites['run'].append(pygame.image.load(
            f'sprites//dino/{self.color}_run2.png'))
        self.image = self.sprites['run'][self.run_animation_index[0] //
                                         self.run_animation_index[1]]

        self.run_animation_index[0] += 1
        if self.run_animation_index[0] > self.run_animation_index[1]:
            self.run_animation_index[0] = 0

    def jump(self):
        if self.state == DinoState.JUMP:
            self.hitbox.y -= self.cur_jump_power * (2 * (game_speed / 8))
            self.cur_jump_power -= 0.5 * (game_speed / 8)

            if self.cur_jump_power <= -self.jump_power:
                self.hitbox.y -= self.cur_jump_power * (2 * (game_speed / 8))
                self.state = DinoState.RUN
                self.cur_jump_power = self.jump_power
        else:
            self.state = DinoState.JUMP
            self.image = pygame.image.load(
                f'sprites/dino/{self.color}_jump.png')

    def update(self):
        if self.state == DinoState.RUN:
            self.run()
        elif self.state == DinoState.JUMP:
            self.jump()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    road_chunks = [
        [pygame.image.load('sprites/road.png'),[0,height -100]],
        [pygame.image.load('sprites/road.png'),[2404,height -100]]
    ]
    font = pygame.font.SysFont('Roboto', 30)
    
    
    

    dino = Dino(30, height - 170, 'default', 'Dino')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(bg)

        # screen.blit(road, (0, height - 100))
        for road_chunk in road_chunks:
            if road_chunk[1][0] <= -2400:
                road_chunk[1][0] = road_chunks[len(road_chunks)-1][1][0] + 2400
                road_chunks[0], road_chunks[1] = road_chunks[1], road_chunks[0]
                break
            road_chunk[1][0] -= game_speed
            screen.blit(road_chunk[0],(road_chunk[1][0], road_chunk[1][1]))
                
        dino.update()

        dino.draw(screen, font)
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            if not dino.state == DinoState.JUMP:
                dino.jump()

        pygame.display.flip()
        clock.tick(0)


run_game()
