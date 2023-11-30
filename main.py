import pygame
import random
import sys
import math
from enum import Enum
import neat


width = 1280
height = 720
bg = (255, 255, 255, 255)

score = 0
score_speedup = 100
game_speed = 5.0

skins = ['default','aqua','black','bloody','cobalt','gold','insta','lime','magenta','magma','navy','neon','orange','purple','pinky','rgb','silver','subaru','sunny','toxic']

names = ['Dino_1','Dino_2','Dino_3','Dino_4','Dino_5','Dino_6','Dino_7','Dino_8','Dino_9','Dino_10','Dino_11','Dino_12','Dino_13','Dino_14','Dino_15','Dino_16','Dino_17','Dino_18','Dino_19','Dino_20']

generation = 0

class DinoState(Enum):
    RUN = 1
    JUMP = 2


class Dino():
    name = "Dino"
    jump_power = 10
    cur_jump_power = jump_power
    color = 'default'
    sprites = {
        "run": [],
        "jump": []
    }
    image = None
    run_animation_index = [0, 5]
    hitbox = None
    state = DinoState.RUN

    def __init__(self, x, y, color="default", name="None"):
        self.color = color
        self.load_sprites()
        self.hitbox = pygame.Rect(
            x, y, self.sprites["run"][0].get_width(), self.sprites["run"][0].get_height())
        self.image = self.sprites["run"][0]

        if name is not None:
            self.name = name

    def load_sprites(self):
        self.sprites["run"].append(pygame.image.load(
            f"sprites/dino/{self.color}_run1.png"))
        self.sprites["run"].append(pygame.image.load(
            f"sprites/dino/{self.color}_run2.png"))
        self.sprites["jump"].append(pygame.image.load(
            f"sprites/dino/{self.color}_jump.png"))

    def draw(self, src, fnt=None):
        src.blit(self.image, (self.hitbox.x, self.hitbox.y))

        if fnt is not None:
            c_label = fnt.render(self.name.capitalize(), True, (100, 100, 100))
            c_label_rect = c_label.get_rect()
            c_label_rect.center = (self.hitbox.x + 45, self.hitbox.y - 30)
            src.blit(c_label, c_label_rect)

    def run(self):
        self.sprites["run"].append(pygame.image.load(
            f"sprites/dino/{self.color}_run1.png"))
        self.sprites["run"].append(pygame.image.load(
            f"sprites/dino/{self.color}_run2.png"))
        self.image = self.sprites["run"][self.run_animation_index[0] //
                                         self.run_animation_index[1]]

        self.run_animation_index[0] += 1
        if self.run_animation_index[0] > self.run_animation_index[1]:
            self.run_animation_index[0] = 0

    def jump(self):
        if self.state == DinoState.JUMP:
            self.hitbox.y -= self.cur_jump_power * (2 * (game_speed / 8))
            self.cur_jump_power -= 0.5 * (game_speed/8)

            # if self.cur_jump_power <= -self.jump_power:
            #     self.hitbox.y -= self.cur_jump_power * (2 * (game_speed / 8))
            #     self.state = DinoState.RUN
            #     self.cur_jump_power = self.jump_power
            if self.hitbox.y >= height - 170:
                self.hitbox.y = height -170
                self.state = DinoState.RUN
                self.cur_jump_power = self.jump_power
        else:
            self.state = DinoState.JUMP
            self.image = pygame.image.load(
                f"sprites/dino/{self.color}_jump.png")

    def update(self):
        if self.state == DinoState.RUN:
            self.run()
        elif self.state == DinoState.JUMP:
            self.jump()


class Cactus:
    available_types = ['1', '2', '3', '4', '5', '6']
    cactus_type = None
    image = None
    hitbox = None
    is_active = True

    def __init__(self, x, y, forced_type=None):
        if forced_type is not None:
            self.cactus_type = forced_type

        self.load_image()
        self.hitbox.x = x
        self.hitbox.y = y - self.hitbox.height

    def load_image(self):
        if self.cactus_type is None:
            self.randomize_cactus()

        self.image = pygame.image.load(
            f'sprites/cactus/{self.cactus_type}.png')
        self.hitbox = self.image.get_rect()

    def randomize_cactus(self):
        self.cactus_type = random.choice(self.available_types)

    def update(self):
        self.hitbox.x -= game_speed
        if self.hitbox.x < -self.hitbox.width:
            self.is_active = False

    def draw(self, src):
        src.blit(self.image, self.hitbox)

def calc_dist(a,b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx ** 2 + dy ** 2)

def run_game(genomes,config):

    global game_speed,score, enemies,dinosaurs,generation,score_speedup 
    generation+=1

    game_speed = 5.0
    score = 0
    score_speedup = 100

    dinosaurs = []
    nets = []
    skins_copy = skins[:]
    names_copy = names[:]

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        g.fitness = 0 

        skin = 'default'
        if len(skins_copy):
            skin = skins_copy.pop()

        name = "Dino"
        if len(names_copy):
            name = names_copy.pop()
        
        dinosaurs.append(Dino(30,height-170,skin,name))


    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    road_chunks = [
        [pygame.image.load('sprites/road.png'), [0, height - 100]],
        [pygame.image.load('sprites/road.png'), [2404, height - 100]]
    ]
    enemies = [
        Cactus(width + 300 / random.uniform(0.8, 3), height - 85),
        Cactus(width * 2 + 200 / random.uniform(0.8, 3), height - 85),
        Cactus(width * 3 + 400 / random.uniform(0.8, 3), height - 85),
    ]
    font = pygame.font.SysFont("Roboto", 30)
    score_font = pygame.font.SysFont("Roboto",40)
    dname_font = pygame.font.SysFont("Roboto",30)
    heading_font = pygame.font.SysFont("Roboto",70)
    # dino = Dino(30, height - 170, 'default', "Dino")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(bg)
        # screen.blit(road,(0,height - 100))

        for road_chunk in road_chunks:
            if road_chunk[1][0] <= -2400:
                road_chunk[1][0] = road_chunks[len(
                    road_chunks) - 1][1][0] + 2400
                road_chunks[0], road_chunks[1] = road_chunks[1], road_chunks[0]
                break
            road_chunk[1][0] -= game_speed
            screen.blit(road_chunk[0], (road_chunk[1][0], road_chunk[1][1]))

        # dino.update()
        # dino.draw(screen, font)
        for dino in dinosaurs:
            dino.update()
            dino.draw(screen,font)

        if len(dinosaurs) == 0:
            break

        if len(enemies) < 3:
            enemies.append(Cactus(
                enemies[len(enemies) - 1].hitbox.x + width / random.uniform(0.8, 3), height - 85))
        
        rem_list = []
        for i, enemy in enumerate(enemies):
            enemy.update()
            enemy.draw(screen)

            if not enemy.is_active:
                rem_list.append(i)
                continue
            for j,dinosaur in enumerate(dinosaurs):
                if dinosaur.hitbox.colliderect(enemy.hitbox):
                    genomes[j][1].fitness -= 10
                    dinosaurs.pop(j)

                    genomes.pop(j)
                    nets.pop(j)

        for i in rem_list:
            enemies.pop(i)

            for j, dinosaur in enumerate(dinosaurs):
                genomes[j][1].fitness += 5

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate(
                (dinosaur.hitbox.y ,calc_dist((dinosaur.hitbox.x, dinosaur.hitbox.y), enemies[0].hitbox.midtop),
                enemies[0].hitbox.width,
                game_speed 
                ))
            if output[0] > 0.5 and dinosaur.state is not DinoState.JUMP:
                dinosaur.jump()
                genomes[i][1].fitness -= 1
        

        score += 0.5 * (game_speed / 4)
        if score > score_speedup:
            score_speedup += 100 * (game_speed / 2)
            game_speed+=1
            print(f"Game speed increased - {game_speed}")

        # user_input = pygame.key.get_pressed()
        # if user_input[pygame.K_SPACE]:
        #     if not dino.state == DinoState.JUMP:
        #         dino.jump()

        score_label = score_font.render("Point : " + str(math.floor(score)),True,(50,50,50))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (width - 100, 50)
        screen.blit(score_label, score_label_rect)


        for i, dinosaur in enumerate(dinosaurs):
            dname_label = dname_font.render(dinosaur.name, True, (170,240,190))
            dname_label_rect = dname_label.get_rect()
            dname_label_rect.center = (width - 100, 100 + (i * 25))
            screen.blit(dname_label,dname_label_rect)

        lable = heading_font.render("Generation : " + str(generation), True, (0,70,190))
        lable_rect = lable.get_rect()
        lable_rect.center = (width / 2, 150)
        screen.blit(lable, lable_rect)

        score_label = score_font.render("Speed : " + str(game_speed / 8) + "x", True,(50,50,50))
        score_label_rect = score_label.get_rect()
        score_label_rect.center = (150,50)
        screen.blit(score_label,score_label_rect)

        pygame.display.flip()
        clock.tick(60)


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,neat.DefaultStagnation, "config-feedforward.txt")

p = neat.Population(config)

p.run(run_game,1000)
