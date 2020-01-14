import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('darkred'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = 5
            elif event.key == pg.K_a:
                self.vel.x = -5
            elif event.key == pg.K_w:
                self.vel.y = -5
            elif event.key == pg.K_s:
                self.vel.y = 5
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w:
                self.vel.y = 0
            elif event.key == pg.K_s:
                self.vel.y = 0

    def update(self):
        # Move the player.
        self.pos += self.vel
        self.rect.center = self.pos


class Water(pg.sprite.Group):
    def __init__(self, pos, *groups):
        super(Water, self).__init__(*groups)
        self.image = pg.Surface((280, 280))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Soil(pg.sprite.Group):
    def __init__(self, pos, *groups):
        super(Soil, self).__init__(*groups)
        self.image = pg.Surface((280, 280))
        self.image.fill(pg.Color('brown'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Camera:
    def __init__(self, focused_player):
        super(Camera, self).__init__()
        self.camera = Vector2(0, 0)
        self.pos = pg.display.Info().current_w, pg.display.Info().current_h
        self.player = focused_player

    def count_new_position(self):
        heading = self.player.pos - self.camera
        self.camera += heading * 0.05
        offset = -self.camera + Vector2(400, 300)

    def screen_size(self):
        return self.pos


class Map:
    land = ["ВВВВВВВВЗЗЗЗ",
            "ВВВВВВВЗЗЗЗВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВЗЗЗВВВВ",
            "ВВВВЗЗЗВВВВВ",
            "ВВВЗЗЗЗВВВВВ",
            "ВВЗЗЗЗВВВВВВ",
            "ВЗЗЗЗВВВВВВВ"]

    def __init__(self, screen):
        self.screen = screen

    @staticmethod
    def double_map(land):
        output = [''] * 9
        for _ in range(9):
            for __ in land[_]:
                print(__)
                output[_] += __ * 2
        print(output)
        return output

    def create_map(self, all_sprites):
        """
            Отрисовывает карту
        """
        # render_map = pg.Surface((3360, 3360))
        x, y = 0, 0
        for row in self.land:
            for element in row:
                if element == "В":
                    all_sprites.add(Water((x, y)))
                elif element == 'З':
                    all_sprites.add(Soil((x, y)))
                x += 280
            y += 280




