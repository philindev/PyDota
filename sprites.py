import pygame as pg
from pygame.math import Vector2
from __init__ import load_image


class Soil(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups[0])
        try:
            self.image = pg.transform.scale(load_image('game/texuters/Soil.jpg'), (280, 280))
        except pg.error:
            self.image = pg.Surface((280, 280))
            self.image.fill(pg.Color('brown'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.add(groups[0])
        self.player = groups[1]
        self.pos = Vector2(pos)

    def update(self):
        self.pos -= self.player.vel
        self.rect.x, self.rect.y = self.pos


class Water(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(groups[0])
        try:
            self.image = pg.transform.scale(load_image('game/texuters/Water.jpg'), (280, 280))
        except pg.error:
            self.image = pg.Surface((280, 280))
            self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.add(groups[0])
        self.player = groups[1]
        self.pos = Vector2(pos)

    def update(self):
        self.pos -= self.player.vel
        self.rect.x, self.rect.y = self.pos
