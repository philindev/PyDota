import pygame
from math import sqrt


class _ABuild(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, radius, sprite, destroyable=False):
        pygame.sprite.Sprite.__init__(self)

        self.radius = radius
        self.image = pygame.image.load(sprite)
        self.destroyable = destroyable
        self.screen = screen

        self.rect = self.image.get_rect()
        self.count = 0

        self.rect.x = x
        self.rect.y = y


class _AAttackTower(_ABuild):
    def __init__(self, x, y, screen, xp, damage, radius, sprite):
        super().__init__(x, y, screen, radius, sprite, True)
        self.xp = xp
        self.damage = damage
        self.dead = False

    def damaged(self, pos, danger):
        if int(sqrt((self.rect.x + self.rect.center[0] - pos[0]) ** 2 + (self.rect.y + self.rect.center[1] - pos[1]) ** 2)) < 700:
            self.xp -= danger[0]
            print(danger)
        if self.xp <= 0:
            self.dead = True
        print(self.rect)
        print(int(sqrt((self.rect[0] + self.rect.center[0] - pos[0]) ** 2 + (self.rect[1] + self.rect.center[1] - pos[1]) ** 2)), danger[1])
