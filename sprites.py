import pygame as pg
from __init__ import load_image
from random import randint
from math import sqrt
import fix.cutter as cutter


class Soil(pg.sprite.Sprite):

    def __init__(self, pos, groups, **kwargs):
        super().__init__(groups)
        try:
            if "type" in kwargs.keys() and kwargs["type"] == 'solid':
                self.image = pg.Surface((280, 280))
                x, y = 0, 0
                for _ in range(4):
                    for __ in range(4):
                        a = randint(1, 5)
                        if a == 3 or a == 5:
                            self.image.blit(pg.transform.scale(pg.image.load(f'grass/{randint(4, 11)}.jpeg'), (70, 70)),
                                            (x, y, 70, 70))
                            x += 70
                            continue
                        self.image.blit(pg.transform.scale(pg.image.load(f'grass/{randint(1, 3)}.jpeg'), (70, 70)),
                                                                                                          (x, y, 70, 70))
                        x += 70
                    x = 0
                    y += 70
            elif "type" in kwargs.keys() and kwargs["type"] == 'edge':
                self.image = pg.Surface((280, 280))
                if kwargs["side"] == 'left':
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/left.png'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/left.png'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == 'bottom':
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/bottom.png'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/bottom.png'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == 'top':
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/top.png'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/top.png'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == 'right':
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/right.png'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/right.png'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "corner_right_bottom":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner_down1.png'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "corner_left_bottom":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner_down.png'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "angle_left_bottom":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/left.png'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner1.png'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/top.png'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "angle_left_top":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner_top.png'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "corner_right_top":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner_top1.png'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "angle_right_top":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner2.png'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/bottom.png'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/right.png'), (140, 140)),
                                    (0, 140, 140, 140))
                elif kwargs["side"] == "angle_right_bottom":
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/corner_down1.png'), (140, 140)),
                                    (0, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 0, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (140, 140, 140, 140))
                    self.image.blit(pg.transform.scale(pg.image.load(f'forest/water.jpeg'), (140, 140)),
                                    (0, 140, 140, 140))

        except pg.error:
            self.image = pg.Surface((280, 280))
            self.image.fill(pg.Color('brown'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Water(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups[0])
        try:
            self.image = pg.transform.scale(load_image('forest/water.jpeg'), (280, 280))
        except pg.error:
            self.image = pg.Surface((280, 280))
            self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Player:
    def __init__(self):
        super().__init__()
        self.RAD = 20
        self.PRAD = 10
        self.x_add, self.y_add = 0, 0
        self.boost = 4

        self.extra_x, self.extra_y = 0, 0

        self.spawn_point = [pg.display.Info().current_w // 2, pg.display.Info().current_h // 2]
        self.cords = self.spawn_point.copy()
        self.red, self.h_green, self.p_green = (200, 100, 0), (0, 255, 0), (0, 200, 0)
        self.full_health, self.health, self.damage, self.hit_range = 500, 500, 10, 100
        self.en_pos_list = (-10, -10)
        self.sprite = cutter.AnimatedSprite(pg.image.load('fix/GG.png'), scale_x=70, scale_y=70, pos=self.spawn_point)

    def draw(self):
        # pygame.draw.line(screen, (0, 255, 0), self.cords, (self.en_pos_list[0], self.en_pos_list[1]), 1)
        size = self.sprite.rect.size
        self.screen.blit(self.sprite.image, (self.cords[0] - size[0] // 2, self.cords[1] - size[1] // 2, *size))

        pg.draw.rect(self.screen, self.h_green, (self.cords[0] - self.RAD,
                                                self.cords[1] - self.RAD - self.RAD / 5 - self.RAD / 4,
                                                (self.RAD * 2) * (self.health / self.full_health),
                                                self.RAD / 4), 0)

    def set_point_position(self, pos):
        self.en_pos_list = pos

    def move(self, items, beings, mask):
        go = False
        for x, y in mask:
            if x <= self.en_pos_list[0] <= x + 280 and y <= self.en_pos_list[1] <= y + 280:
                go = True
                break

        if not go:
            return

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

        if abs(dx < 20) and dy > 20:
            self.y_add = 5
        elif abs(dx) < 20 and dy < -20:
            self.y_add = -5

        count = 0
        for _ in items:
            count += 1
            if count == 8 or count == 9:
                _.sprite.image.get_rect().x -= int(self.x_add * self.boost * 0.75)
                _.sprite.image.get_rect().y -= int(self.y_add * self.boost * 0.75)
                continue
            _.rect.x -= int(self.x_add * self.boost * 0.75)
            _.rect.y -= int(self.y_add * self.boost * 0.75)

        count = 0
        for creatures in beings:
            count += 1
            if count == 4:
                for cords in creatures:
                    cords[0] -= int(self.x_add * self.boost * 0.75)
                    cords[1] -= int(self.y_add * self.boost * 0.75)
            else:
                for _ in creatures:
                    _.cords[0] -= int(self.x_add * self.boost * 0.75)
                    _.cords[1] -= int(self.y_add * self.boost * 0.75)
                    _.spawn_point[0] -= int(self.x_add * self.boost * 0.75)
                    _.spawn_point[1] -= int(self.y_add * self.boost * 0.75)

        self.en_pos_list[0] -= int(self.x_add * self.boost * 0.75)
        self.en_pos_list[1] -= int(self.y_add * self.boost * 0.75)

        self.extra_x += int(self.x_add * self.boost * 0.75)
        self.extra_y += int(self.y_add * self.boost * 0.75)

        self.sprite.update(int(self.x_add * self.boost), int(self.y_add * self.boost))

    def take_damage_f_creep(self, en_location, danger):
        if int(sqrt((self.cords[0] - en_location[0]) ** 2 + (self.cords[1] - en_location[1]) ** 2)) < danger[1]:
            self.health -= danger[0]

    def check_health(self, draw_again):
        if self.health <= 0:
            self.health = self.full_health
            self.cords = self.spawn_point.copy()
            self.en_pos_list = self.spawn_point.copy()
            draw_again((self.extra_x, self.extra_y), self.boost)

    def attack(self):
        return [self.damage, self.hit_range]

    def chase(self, click_p, enemy_p, rad):
        if enemy_p[0] - rad < click_p[0] < enemy_p[0] + rad and enemy_p[1] - rad < click_p[1] < enemy_p[1] + rad:
            return True

    def add_screen(self, screen):
        self.screen = screen


class Creep:
    def __init__(self, col, pos):
        if col:
            self.team_color = (255, 0, 0)
            self.spawn_point = pos

            name = 'fix/Soldier/' + str(randint(1, 34)) + '.png'
        else:
            self.team_color = (0, 0, 255)
            self.spawn_point = pos

            name = 'fix/Enemy/' + str(randint(1, 36)) + '.png'

        self.RAD = 15

        self.green = (0, 255, 0)

        self.view = 300
        self.hit_range = 85
        self.damage = 20

        self.cords = self.spawn_point.copy()
        self.full_health = 400
        self.health = 400

        self.sprite = cutter.AnimatedSprite(pg.image.load(name))

        self.x_add, self.y_add = 0, 0

    def draw(self):
        size = self.sprite.rect.size
        self.screen.blit(self.sprite.image, (self.cords[0] - size[0] // 2, self.cords[1] - size[1] // 2, *size))

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
        pg.draw.rect(self.screen, self.green, (self.cords[0] - self.RAD,
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


    def move_g(self, en_pos_list):
        self.boost = 2
        self.dist, self.x_line, self.y_line = [], [], []
        self.in_view = []
        self.en_pos_list = en_pos_list
        self.en_pos_list = list(map(list, self.en_pos_list))
        self.x_add = 0
        self.y_add = 0

        for j in range(len(self.en_pos_list)):
            self.dist.append(
                abs(self.cords[0] - self.en_pos_list[j][0]) + abs(self.cords[1] - self.en_pos_list[j][1]))

        mnind = self.dist.index(min(self.dist))

        dx = self.en_pos_list[mnind][0] - self.cords[0]
        dy = self.en_pos_list[mnind][1] - self.cords[1]
        if dx == 0:
            dx = -1
        k = (self.en_pos_list[mnind][1] - self.cords[1]) / dx
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


class Boss(Creep):
    def __init__(self, pos):
        super(Boss, self).__init__(False, pos)
        self.team_color = (0, 0, 255)
        self.spawn_point = pos
        self.RAD = 40
        self.view = 500
        self.hit_range = 100
        self.full_health = 500
        self.health = 500
        self.damage = 30

    def hp(self):
        return self.health / self.full_health

    def heal(self, heal_location, heal):
        if int(sqrt((self.cords[0] - heal_location[0]) ** 2 + (self.cords[1] - heal_location[1]) ** 2)) < heal[1]:
            if self.health < self.full_health:
                self.health += heal[0]

    def retreat(self, en_pos_list):
        self.boost = 2
        self.dist, self.x_line, self.y_line = [], [], []
        self.in_view = []
        self.en_pos_list = en_pos_list
        self.en_pos_list = list(map(list, self.en_pos_list))
        self.x_add = 0
        self.y_add = 0

        for j in range(len(self.en_pos_list)):
            self.dist.append(
                abs(self.cords[0] - self.en_pos_list[j][0]) + abs(self.cords[1] - self.en_pos_list[j][1]))

        mnind = self.dist.index(min(self.dist))

        dx = self.en_pos_list[mnind][0] - self.cords[0]
        dy = self.en_pos_list[mnind][1] - self.cords[1]
        if dx == 0:
            dx = -1
        k = (self.en_pos_list[mnind][1] - self.cords[1]) / dx
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