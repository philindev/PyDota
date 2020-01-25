import pygame
from math import sqrt
from Buildings.Abstract_Build import _ABuild, _AAttackTower


class RadiusTower(_AAttackTower):
    """
    Чтобы это работало правильно нужно перед циклом инициализировать и вызвать update:
        heal = Buildings.RadiusTower(550, 0, screen)
        damage = heal.update()

    В главном цикле 1 раз вызывать attack и update:
        heal.attack(team_blue, team_blue[0].sprite.rect.center)
        damage = heal.update()

    И для каждого объект который может быть задамажен (например, крип) прописать подобное:
        if not damage:
            damage = heal.update()
            if damage:
                team_blue[i].take_damage_f_pl(damage[0], damage[1])
        else:
            team_blue[i].take_damage_f_pl(damage[0], damage[1])
    """
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, xp=100, damage=100, radius=500, sprite='Buildings/RadiusTower.png')

        self.bomb = None

    def attack(self, coor, center):
        if not self.dead:
            for pers in coor:
                self.count += 1

                if int(sqrt((self.rect.center[0] - pers.cords[0]) ** 2 + (
                        self.rect.center[1] - pers.cords[1]) ** 2)) < self.radius:
                    if self.count % 300 == 0:
                        self.bomb = Bomb(pers.cords[0] + center[0], pers.cords[1] + center[1], self.screen)

    def update(self):
        if not self.dead:
            self.screen.blit(self.image, self.rect)
            if self.bomb != None:
                if self.bomb.update():
                    result = self.bomb.rect
                    self.bomb = None
                    return result, (75, self.damage)
            return False


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.surface = AnimatedSprite(pygame.image.load('Buildings/boom.png'), 8, 1)
        self.screen = screen
        self.rect = self.surface.image.get_rect()
        self.rect.x = x - 75
        self.rect.y = y - 75

        self.count = 0

    def update(self):
        self.count += 1
        if self.count % 20 == 0:
            result = self.surface.update()
            self.screen.blit(self.surface.image, self.rect)
            return result


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []

        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(columns):
            for i in range(rows):
                frame_location = (self.rect.w * j, self.rect.h * i)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (150, 150)))  # Здесь менять scale

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        return self.cur_frame == len(self.frames) - 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start, destination, screen):
        pygame.sprite.Sprite.__init__(self)

        self.surface = pygame.Surface((6, 6), pygame.SRCALPHA)
        self.screen = screen
        self.rect = self.surface.get_rect()
        self.rect.x = start[0] + 90
        self.rect.y = start[1] + 100
        self.dest = destination
        self.done = False

        self.count = 0
        pygame.draw.circle(self.surface, (255, 255, 255), (3, 3), 3)

        screen.blit(self.surface, self.rect)

    def update(self):
        self.dist, self.x_line, self.y_line = [], [], []

        dx = self.dest[0] - self.rect.x
        dy = self.dest[1] - self.rect.y

        if dx <= 50 and dy <= 50:

            return True

        if dx == 0:
            dx = 1

        xslide = 2
        if dx < 0:
            xslide *= -1

        if abs(dx) + abs(dy) > 10:
            for d in range(1, 3):
                x = d * xslide
                self.x_line.append(x)
                y = (x - self.rect[0]) * dy / dx + self.rect[1]
                self.y_line.append(y)
        else:
            self.x_line.append(1)
            self.y_line.append(1)
            self.x_line.append(1)
            self.y_line.append(1)

        self.x_add = self.x_line[1] - self.x_line[0]
        self.y_add = self.y_line[1] - self.y_line[0]

        if abs(dx < 10) and dy > 20:
            self.y_add = 5
        elif abs(dx) < 10 and dy < -20:
            self.y_add = -5

        self.rect[0] += int(self.x_add * 4)
        self.rect[1] += int(self.y_add * 4)

        self.screen.blit(self.surface, self.rect)


class PointTower(_AAttackTower):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, xp=400, damage=100, radius=500, sprite='Buildings/PointTower.png')
        self.bullet = None

    def attack(self, coor):
        if not self.dead:
            for pers in coor:
                self.count += 1

                if int(sqrt((self.rect.center[0] - pers.cords[0]) ** 2 + (
                        self.rect.center[1] - pers.cords[1]) ** 2)) < self.radius:
                    if self.count % 100 == 0:
                        self.bullet = Bullet(self.rect.topleft, pers.cords, self.screen)
                        pers.health -= self.damage
                        return

    def update(self, x=0, y=0):
        if not self.dead:
            self.screen.blit(self.image, self.rect)
            if self.bullet != None:
                if self.bullet.update():
                    self.bullet = None


class MainTower(_AAttackTower):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, radius=20, sprite='Buildings/Shop.png', xp=1000, damage=0)

    def check_win(self):
        return self.dead
