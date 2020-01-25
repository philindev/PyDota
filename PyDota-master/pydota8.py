from math import sqrt
import pygame
import time

pygame.init()
height, width = 1300, 700
size = height, width
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


class Player:
    def __init__(self):
        self.RAD = 20
        self.PRAD = 10

        self.spawn_point = [600, 600]
        self.cords = self.spawn_point.copy()
        self.red, self.h_green, self.p_green = (200, 100, 0), (0, 255, 0), (0, 200, 0)
        self.full_health, self.health, self.damage, self.hit_range = 500, 500, 10, 100
        self.en_pos_list = (-10, -10)

    def draw(self):
        pygame.draw.circle(screen, self.red, self.cords, self.RAD)
        pygame.draw.circle(screen, self.p_green, self.en_pos_list, self.PRAD, 2)
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
        self.boost = 3
        if dx == 0:
            dx = -1
        k = dy / dx
        # print(k, "     k")
        b = self.cords[1] - k * self.cords[0]
        # print(b, "     b")

        xslide = dx / 70
        # print(xslide)

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

        x_add = int(self.x_line[1] - self.x_line[0])
        y_add = int(self.y_line[1] - self.y_line[0])

        if dy > 50:
            y_add = 5
        elif dy < -50:
            y_add = -5

        self.cords[0] += x_add * self.boost
        self.cords[1] += y_add * self.boost

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
        if enemy_p[0] - rad < click_p[0] < enemy_p[0] + rad and  enemy_p[1] - rad < click_p[1] < enemy_p[1] + rad:
            return True


class Creep:
    def __init__(self, col):
        if col:
            self.team_color = (255, 0, 0)
            self.spawn_point = [100, 100]
        else:
            self.team_color = (0, 0, 255)
            self.spawn_point = [700, 600]

        self.RAD = 15

        self.green = (0, 255, 0)

        self.view = 300
        self.hit_range = 70
        self.damage = 20

        self.cords = self.spawn_point.copy()
        self.full_health = 400
        self.health = 400

        self.x_add, self.y_add = 0, 0



    def draw(self):
        pygame.draw.circle(screen, self.team_color, self.cords, self.RAD)
        pygame.draw.circle(screen, (255, 255, 0), self.cords, self.view, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.cords, self.hit_range, 1)

    def move(self, en_pos_list, fr_pos_list, r, ind):

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
                sqrt((self.cords[0] - self.in_view[j][0]) ** 2 + (self.cords[1] - self.in_view[j][1]) ** 2))


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
                    x = int(d * xslide)
                    self.x_line.append(x)
                    y = int(k * x + b)
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

        for i in range(len(fr_pos_list)):
            if i != ind:
                if sqrt((self.cords[0] - fr_pos_list[i][0]) ** 2 + (self.cords[1] - fr_pos_list[i][1]) ** 2) <= r[i] + self.RAD:
                    self.x_add = 0
                    self.y_add = 0

        self.cords[0] += self.x_add * self.boost
        self.cords[1] += self.y_add * self.boost

    def attack(self):
        return [self.damage, self.hit_range]

    def chase(self):
        pass

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

#
# class Giant(Creep):
#     def __init__(self, col):
#         super(Giant, self).__init__(col)
#         self.cords = [1000, 200]
#         self.RAD = 60
#
#     def move(self, en_pos_list, fr_pos_list, r, ind):
#         print("enposlist:", en_pos_list)
#         self.boost = 2
#         self.dist, self.x_line, self.y_line = [], [], []
#         self.in_view = []
#         self.en_pos_list = en_pos_list
#         self.en_pos_list = list(map(list, self.en_pos_list))
#         self.x_add = 0
#         self.y_add = 0
#
#         for v in self.en_pos_list:
#             if sqrt((self.cords[0] - v[0]) ** 2 + (self.cords[1] - v[1]) ** 2) <= self.view:
#                 self.in_view.append(v)
#
#         for j in range(len(self.in_view)):
#             self.dist.append(
#                 sqrt((self.cords[0] - self.in_view[j][0]) ** 2 + (self.cords[1] - self.in_view[j][1]) ** 2))
#
#         print("in view:", self.in_view)
#
#         if len(self.in_view) > 0:
#             mnind = self.dist.index(min(self.dist))
#             dx = self.in_view[mnind][0] - self.cords[0]
#             dy = self.in_view[mnind][1] - self.cords[1]
#             if dx == 0:
#                 dx = -1
#             k = (self.in_view[mnind][1] - self.cords[1]) / dx
#             b = self.cords[1] - k * self.cords[0]
#
#             xslide = dx / 100
#
#             if abs(dx) > 40:
#                 for d in range(1, 3):
#                     x = int(d * xslide)
#                     self.x_line.append(x)
#                     y = int(k * x + b)
#                     self.y_line.append(y)
#             else:
#                 self.x_line.append(1)
#                 self.y_line.append(1)
#                 self.x_line.append(1)
#                 self.y_line.append(1)
#
#             self.x_add = self.x_line[1] - self.x_line[0]
#             self.y_add = self.y_line[1] - self.y_line[0]
#
#             if dy > 50:
#                 self.y_add = 5
#             elif dy < -50:
#                 self.y_add = -5
#
#         for i in range(len(fr_pos_list)):
#             if i != ind:
#                 if sqrt((self.cords[0] - fr_pos_list[i][0]) ** 2 + (self.cords[1] - fr_pos_list[i][1]) ** 2) <= r[i] + self.RAD:
#                     self.x_add = 0
#                     self.y_add = 0
#
#         self.cords[0] += self.x_add * self.boost
#         self.cords[1] += self.y_add * self.boost
#
#
# class Tower:
#     def __init__(self):
#         self.cords = [1000, 200]
#         self.RAD = 60
#         self.color = (255, 255, 255)
#
#     def draw(self):
#         pygame.draw.circle(screen, (200, 200, 200), self.cords, self.RAD)
p =[]

# t = Tower()
# g = Giant(True)

clock = pygame.time.Clock()
fps = 100
creep_kd = 0
crr1 = Creep(True)


crb1 = Creep(False)


team_red = [crr1]
team_blue = [crb1]


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


    print('time:', pygame.time.get_ticks())

    blue_pos = [i.cords for i in team_blue]
    blue_collide = [i.collision() for i in team_blue]

    red_pos = [i.cords for i in team_red]
    red_collide = [i.collision() for i in team_red]

    blue_feed = red_pos.copy()
    blue_feed.append(pl.cords)

    creep_s_kd += 1
    creep_kd += 1
    print(creep_s_kd)
    for i in range(len(team_red)):
        team_red[i].draw()
        team_red[i].move(blue_pos, red_pos, red_collide, i)
        team_red[i].health_bar()
        team_red[i].check_health()
        team_red[i].take_damage_f_creep(blue_pos, team_red[i].attack())

    for i in range(len(team_blue)):
        team_blue[i].draw()
        team_blue[i].move(blue_feed, blue_pos, blue_collide, i)
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

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
