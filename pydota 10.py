from math import sqrt
import pygame

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

    def draw(self):
        pygame.draw.line(screen, (0, 255, 0), self.cords, (self.en_pos_list[0], self.en_pos_list[1]), 1)
        pygame.draw.circle(screen, self.p_green, self.en_pos_list, self.PRAD, 2)

        pygame.draw.circle(screen, self.red, self.cords, self.RAD)
        pygame.draw.rect(screen, self.h_green, (self.cords[0] - self.RAD,
                                                self.cords[1] - self.RAD - self.RAD / 5 - self.RAD / 4,
                                                (self.RAD * 2) * (self.health / self.full_health),
                                                self.RAD / 4), 0)
        pygame.draw.circle(screen, (255, 0, 0), self.cords, self.hit_range, 1)

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

        if abs(dx < 20) and dy > 20:
            self.y_add = 5
        elif abs(dx) < 20 and dy < -20:
            self.y_add = -5

        self.cords[0] += int(self.x_add * self.boost)
        self.cords[1] += int(self.y_add * self.boost)

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

    def heal(self, heal_location, heal):
        if int(sqrt((self.cords[0] - heal_location[0]) ** 2 + (self.cords[1] - heal_location[1]) ** 2)) < heal[1]:
            if self.health < self.full_health:
                self.health += heal[0]


class Creep:
    def __init__(self, col, pos):
        if col:
            self.team_color = (255, 0, 0)
            self.spawn_point = pos
            self.h_b = (0, 255, 0)
        else:
            self.team_color = (0, 0, 255)
            self.spawn_point = pos
            self.h_b = (255, 0, 0)

        self.RAD = 15


        self.view = 300
        self.hit_range = 85
        self.damage = 20

        self.cords = self.spawn_point.copy()
        self.full_health = 400
        self.health = 400

        self.x_add, self.y_add = 0, 0

    def draw(self):
        pygame.draw.circle(screen, self.team_color, self.cords, self.RAD)
        pygame.draw.circle(screen, (255, 255, 0), self.cords, self.view, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.cords, self.hit_range, 1)

        pygame.draw.rect(screen, (0, 255, 0), (self.cords[0] - self.RAD, self.cords[1] - self.RAD, self.RAD * 2, self.RAD * 2), 1)

    def move(self, en_tow_pos, en_pos_list):
        self.boost = 2
        self.dist, self.x_line, self.y_line = [], [], []
        self.in_view = []
        self.en_pos_list = en_pos_list
        self.en_tow_pos = en_tow_pos
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

        else:
            for j in range(len(self.en_tow_pos)):
                self.dist.append(
                    abs(self.cords[0] - self.en_tow_pos[j][0]) + abs(self.cords[1] - self.en_tow_pos[j][1]))

            mnind = self.dist.index(min(self.dist))

            dx = self.en_tow_pos[mnind][0] - self.cords[0]
            dy = self.en_tow_pos[mnind][1] - self.cords[1]
            if dx == 0:
                dx = -1
            k = (self.en_tow_pos[mnind][1] - self.cords[1]) / dx
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


    def attack(self):
        return [self.damage, self.hit_range]

    def health_bar(self):
        pygame.draw.rect(screen, self.h_b, (self.cords[0] - self.RAD,
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


class Heal:
    def __int__(self, pos):
        self.heal_ = 50
        self.heal_rad = 200
        self.cords = pos

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.cords[0], self.cords[1]), 30)
        pygame.draw.circle(screen, (255, 255, 255), self.cords, self.heal_rad, 1)

    def heal(self):
        return [self.heal_, self.heal_rad]



p = []
h = Heal()
h.__int__([500, 500])
clock = pygame.time.Clock()
fps = 100
creep_kd = 0

gr1 = Giant(True, [50, 250])
gr2 = Giant(True, [150, 250])
gr3 = Giant(True, [250, 250])
rgig_list = [gr1, gr2, gr3]

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

b = Boss([1200, 400])

gb1 = Giant(False, [1200, 400])
gb2 = Giant(False, [1100, 400])
gb3 = Giant(False, [1000, 400])
bgig_list = [gb1, gb2, gb3]

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


team_red = [crr1, crr2, crr3, crr4, crr5, crr6, crr7, crr8, crr9, crr10, crr11, crr12, crr13, crr14, crr15, crr16, gr1, gr2, gr3]
team_blue = [b, crb1, crb2, crb3, crb4, crb5, crb6, crb7, crb8, crb9, crb10, crb11, crb12, crb13, crb14, crb15, crb16, gb1, gb2, gb3]

rtower_pos = [[1200, 100]]
btower_pos = [[100, 600]]

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

    creep_kd += 1
    h.draw()
    for i in range(len(team_red)):
        if team_red[i] in rgig_list:
            team_red[i].draw()
            team_red[i].move_g(btower_pos)
        else:
            team_red[i].draw()
            team_red[i].move(btower_pos, blue_pos)

        team_red[i].health_bar()
        team_red[i].check_health()
        team_red[i].take_damage_f_creep(blue_pos, team_red[i].attack())

    for i in range(len(team_blue)):
        if team_blue[i] in bgig_list:
            team_blue[i].draw()
            team_blue[i].move_g(rtower_pos)
        elif team_blue[i] == b:
            if team_blue[i].hp() < 0.3:
                team_blue[i].draw()
                team_blue[i].retreat([h.cords])
            else:
                team_blue[i].draw()
                b.move(rtower_pos, blue_feed)

            team_blue[i].heal(h.cords, h.heal())
        else:
            team_blue[i].draw()
            team_blue[i].move(rtower_pos, blue_feed)

        team_blue[i].health_bar()
        team_blue[i].check_health()
        team_blue[i].take_damage_f_creep(red_pos, team_blue[i].attack())

        if creep_kd % 20 == 0 and team_blue[i] not in bgig_list:
            pl.take_damage_f_creep(team_blue[i].cords, team_blue[i].attack())

        if fill:
            if pl.chase(p, team_blue[i].cords, team_blue[i].RAD):
                team_blue[i].take_damage_f_pl(pl.cords, pl.attack())

    if fill:
        pl.move()
    pl.heal(h.cords, h.heal())
    pl.draw()
    pl.check_health()

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
