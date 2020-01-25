from math import sqrt
import pygame
import fix.cutter as cutter
from random import randint
import Buildings.Help as Help

pygame.init()
height, width = 1300, 700
size = height, width
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


class Player:
    def __init__(self):
        super().__init__()
        self.RAD = 20
        self.PRAD = 10
        self.x_add, self.y_add = 0, 0
        self.boost = 4
        self.spawn_point = [600, 600]
        self.cords = self.spawn_point.copy()
        self.red, self.h_green, self.p_green = (200, 100, 0), (0, 255, 0), (0, 200, 0)
        self.full_health, self.health, self.damage, self.hit_range = 500, 500, 10, 100
        self.en_pos_list = (-10, -10)

        self.sprite = cutter.AnimatedSprite(pygame.image.load('GG.png'), scale_x=70, scale_y=70)

    def draw(self):
        # pygame.draw.line(screen, (0, 255, 0), self.cords, (self.en_pos_list[0], self.en_pos_list[1]), 1)
        size = self.sprite.rect.size
        screen.blit(self.sprite.image, (self.cords[0] - size[0] // 2, self.cords[1] - size[1] // 2, *size))

        pygame.draw.rect(screen, self.h_green, (self.cords[0] - self.RAD,
                                                self.cords[1] - self.RAD - self.RAD / 5 - self.RAD / 4,
                                                (self.RAD * 2) * (self.health / self.full_health),
                                                self.RAD / 4), 0)

    def set_point_position(self, pos):
        self.en_pos_list = pos

    def move(self):
        self.dist, self.x_line, self.y_line = [], [], []

        dx = self.en_pos_list[0] - self.cords[0]
        dy = self.en_pos_list[1] - self.cords[1]

        if dx == 0:
            dx = 1

        xslide = 2
        if dx < 0:
            xslide *= -1

        if abs(dx) + abs(dy) > 20:
            for d in range(1, 3):
                x = d * xslide
                self.x_line.append(x)
                y = (x - self.cords[0]) * dy / dx + self.cords[1]
                self.y_line.append(y)
        else:
            self.x_line.append(1)
            self.y_line.append(1)
            self.x_line.append(1)
            self.y_line.append(1)

        self.x_add = self.x_line[1] - self.x_line[0]
        self.y_add = self.y_line[1] - self.y_line[0]

        self.cords[0] += int(self.x_add * self.boost)
        self.cords[1] += int(self.y_add * self.boost)

        self.sprite.update(int(self.x_add * self.boost), int(self.y_add * self.boost))

    def take_damage_f_creep(self, en_location, danger):
        if int(sqrt((self.cords[0] - en_location[0]) ** 2 + (self.cords[1] - en_location[1]) ** 2)) < danger[1]:
            self.health -= danger[0]

    def check_health(self):
        if self.health <= 0:
            self.health = self.full_health
            self.cords = self.spawn_point.copy()
            self.en_pos_list = self.spawn_point.copy()

    def attack(self):
        return [self.damage, self.hit_range]

    def chase(self, click_p, enemy_p, rad):
        if enemy_p[0] - rad < click_p[0] < enemy_p[0] + rad and enemy_p[1] - rad < click_p[1] < enemy_p[1] + rad:
            return True


class Creep:
    def __init__(self, col, pos):
        if col:
            self.team_color = (255, 0, 0)
            self.spawn_point = pos

            name = 'Soldier\\' + str(randint(1, 34)) + '.png'
        else:
            self.team_color = (0, 0, 255)
            self.spawn_point = pos

            name = 'Enemy\\' + str(randint(1, 36)) + '.png'

        self.RAD = 15

        self.green = (0, 255, 0)

        self.view = 300
        self.hit_range = 85
        self.damage = 20

        self.cords = self.spawn_point.copy()
        self.full_health = 400
        self.health = 400

        self.sprite = cutter.AnimatedSprite(pygame.image.load(name))

        self.x_add, self.y_add = 0, 0

    def draw(self):
        size = self.sprite.rect.size
        screen.blit(self.sprite.image, (self.cords[0] - size[0] // 2, self.cords[1] - size[1] // 2, *size))

    def move(self, en_pos_list):
        self.boost = 2
        self.dist, self.x_line, self.y_line = [], [], []
        self.in_view = []
        self.en_pos_list = en_pos_list
        self.en_pos_list = list(map(list, self.en_pos_list))
        self.x_add = 0
        self.y_add = 0

        for v in self.en_pos_list:
            if sqrt((self.cords[0] - v[0]) ** 2 + (self.cords[1] - v[1]) ** 2) <= self.view:
                self.in_view.append(v)

        for j in range(len(self.in_view)):
            self.dist.append(
                abs(self.cords[0] - self.in_view[j][0]) + abs(self.cords[1] - self.in_view[j][1]))


        if len(self.in_view) > 0:
            mnind = self.dist.index(min(self.dist))

            dx = self.in_view[mnind][0] - self.cords[0]
            dy = self.in_view[mnind][1] - self.cords[1]
            if dx == 0:
                dx = -1
            k = (self.in_view[mnind][1] - self.cords[1]) / dx
            b = self.cords[1] - k * self.cords[0]

            xslide = dx / 100

            if abs(dx) > 40:
                for d in range(1, 3):
                    x = d * xslide
                    self.x_line.append(x)
                    y = k * x + b
                    self.y_line.append(y)
            else:
                self.x_line.append(1)
                self.y_line.append(1)
                self.x_line.append(1)
                self.y_line.append(1)

            self.x_add = self.x_line[1] - self.x_line[0]
            self.y_add = self.y_line[1] - self.y_line[0]

            if dy > 50:
                self.y_add = 5
            elif dy < -50:
                self.y_add = -5

        self.cords[0] += int(self.x_add * self.boost)
        self.cords[1] += int(self.y_add * self.boost)

        self.sprite.update(int(self.x_add * self.boost), int(self.y_add * self.boost))

    def attack(self):
        return [self.damage, self.hit_range]

    def health_bar(self):
        pygame.draw.rect(screen, self.green, (self.cords[0] - self.RAD,
                                              self.cords[1] - self.RAD - self.RAD / 5 - self.RAD / 4,
                                              (self.RAD * 2) * (self.health / self.full_health),
                                              self.RAD / 4),
                         0)

    def check_health(self):
        if self.health <= 0:
            self.health = self.full_health
            self.cords = self.spawn_point.copy()

    def take_damage_f_pl(self, en_location, danger):
        if int(sqrt((self.cords[0] - en_location[0]) ** 2 + (self.cords[1] - en_location[1]) ** 2)) < danger[1]:
            self.health -= danger[0]

    def take_damage_f_creep(self, en_location, danger):
        for i in en_location:
            if int(sqrt((self.cords[0] - i[0]) ** 2 + (self.cords[1] - i[1]) ** 2)) < danger[1]:
                self.health -= danger[0]

    def collision(self):
        return self.RAD

    def add_screen(self, screen):
        self.screen = screen


class Giant(Creep):
    def __init__(self, col, pos):
        super(Giant, self).__init__(col, pos)
        self.RAD = 30

        name = 'giant\\' + str(randint(1, 4)) + '.png'
        self.sprite = cutter.AnimatedSprite(pygame.image.load(name))


class Boss(Creep):
    def __init__(self, pos):
        super(Boss, self).__init__(False, pos)
        self.team_color = (0, 0, 255)
        self.spawn_point = pos
        self.RAD = 40

        self.sprite = cutter.AnimatedSprite(pygame.image.load('boss\\walk.png'), 4, 4, 100, 100)

    p = []


clock = pygame.time.Clock()
fps = 100
creep_kd = 0

crr1 = Creep(True, [50, 50])
crr2 = Creep(True, [100, 100])
crr3 = Creep(True, [150, 150])
crr4 = Creep(True, [50, 100])
crr5 = Creep(True, [50, 150])
crr6 = Creep(True, [100, 50])
crr7 = Creep(True, [100, 150])
crr8 = Creep(True, [150, 50])
crr9 = Creep(True, [150, 100])
crr10 = Creep(True, [50, 200])
crr11 = Creep(True, [100, 200])
crr12 = Creep(True, [150, 200])
crr13 = Creep(True, [200, 200])
crr14 = Creep(True, [200, 50])
crr15 = Creep(True, [200, 100])
crr16 = Creep(True, [200, 150])

crb1 = Creep(False, [1200, 600])
crb2 = Creep(False, [1200, 550])
crb3 = Creep(False, [1200, 500])
crb4 = Creep(False, [1150, 600])
crb5 = Creep(False, [1150, 550])
crb6 = Creep(False, [1150, 500])
crb7 = Creep(False, [1100, 600])
crb8 = Creep(False, [1100, 550])
crb9 = Creep(False, [1100, 500])
crb10 = Creep(False, [1050, 500])
crb11 = Creep(False, [1050, 550])
crb12 = Creep(False, [1050, 600])
crb13 = Creep(False, [1050, 650])
crb14 = Creep(False, [1100, 650])
crb15 = Creep(False, [1150, 650])
crb16 = Creep(False, [1200, 650])

team_red = [crr1, crr2, crr3, crr4, crr5, crr6, crr7, crr8, crr9, crr10, crr11, crr12, crr13, crr14, crr15, crr16]
team_blue = [crb1, crb2, crb3, crb4, crb5, crb6, crb7, crb8, crb9, crb10, crb11, crb12, crb13, crb14, crb15, crb16]
# heal = Help.Heal(1050, 0, screen)

pl = Player()
run = True
fill = False
creep_s_kd = 0
while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                p = list(event.pos)
                pl.set_point_position(p)
                fill = True

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    blue_pos = [i.cords for i in team_blue]
    blue_collide = [i.collision() for i in team_blue]

    red_pos = [i.cords for i in team_red]
    red_collide = [i.collision() for i in team_red]

    blue_feed = red_pos.copy()
    blue_feed.append(pl.cords)

    creep_s_kd += 1
    creep_kd += 1

    for i in range(len(team_red)):
        team_red[i].draw()
        team_red[i].move(blue_pos)
        team_red[i].health_bar()
        team_red[i].check_health()
        team_red[i].take_damage_f_creep(blue_pos, team_red[i].attack())

    for i in range(len(team_blue)):
        team_blue[i].draw()
        team_blue[i].move(blue_feed)
        team_blue[i].health_bar()
        team_blue[i].check_health()
        team_blue[i].take_damage_f_creep(red_pos, team_blue[i].attack())

        if creep_kd % 40 == 0:
            pl.take_damage_f_creep(team_blue[i].cords, team_blue[i].attack())

        if fill:
            if pl.chase(p, team_blue[i].cords, team_blue[i].RAD):
                team_blue[i].take_damage_f_pl(pl.cords, pl.attack())

    if fill:
        pl.move()

    pl.draw()
    pl.check_health()


    clock.tick(30)
    # if pl.health < pl.full_health:
    #     pl.health += heal.help(pl.cords)
    #
    # heal.update()
    pygame.display.flip()

pygame.quit()
