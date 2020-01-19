from random import randrange

import sys
import math
import copy


import pygame as pg
from pygame.math import Vector2
from map import Map
from sprites import Player


def to_convenient_cords(x, y):
    absolute_h, absolute_w = pg.display.Info().current_h // 2, pg.display.Info().current_w // 2
    cords_x = x - absolute_w
    cords_y = y - absolute_h
    return cords_x, cords_y


class Camera:

    def __init__(self, focused_player, *args):
        self.player = focused_player
        self.screen_size = pg.display.Info().current_w, pg.display.Info().current_h
        x, y = self.screen_size
        self.camera = Vector2(self.screen_size)
        if len(args):
            self.world = args[0]

    def count_camera_pos(self, all_sprites):
        x, y = self.screen_size
        heading = self.player.pos - self.camera
        self.camera += heading * 0.05
        offset = -self.camera + Vector2(x // 2, y // 2)  # центрирует камеру на игроке

        self.player.screen.blit(self.player.image, self.player.rect.topleft + offset)

    def add_rects(self, rects):
        self.background_rects = rects


def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    sprite_objects = list()

    player = Player()
    player.add_screen(screen)

    world = Map()
    world.add_screen(screen)
    world.create_map(all_sprites, player)

    sprite_objects.append(world)
    fill = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    p = list(event.pos)
                    player.set_point_position(p)
                    fill = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    return

        screen.fill((30, 30, 30))

        if fill:
            player.move(sprite_objects)

        for _ in sprite_objects:
            screen.blit(_.image, _.rect)
        player.draw()
        player.check_health()

        pg.display.flip()
        clock.tick(60)


main()
pg.quit()
