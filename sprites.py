import pygame as pg


class Soil(pg.sprite.Group):
    def __init__(self, pos, *groups):
        super(Soil, self).__init__(*groups)
        self.image = pg.Surface((280, 280))
        self.image.fill(pg.Color('brown'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        print('Drew Water')


class Water(pg.sprite.Group):
    def __init__(self, pos, *groups):
        super(Water, self).__init__(*groups)
        self.image = pg.Surface((280, 280))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        print('Drew Soil')
