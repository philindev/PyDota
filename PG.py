from random import randrange

import sys


import pygame as pg
from pygame.math import Vector2
from sprites import Soil, Water
from map import Map


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)

    def handle_event(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_F11:
                sys.exit()
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

    def add_screen(self, screen):
        self.screen = screen


class Camera:
    def __init__(self, focused_player):
        self.player = focused_player
        self.screen_size = pg.display.Info().current_w, pg.display.Info().current_h
        x, y = self.screen_size
        self.camera = Vector2(self.screen_size)

    def count_camera_pos(self):
        x, y = self.screen_size
        heading = self.player.pos - self.camera
        self.camera += heading * 0.05
        offset = -self.camera + Vector2(x // 2, y // 2) # центрирует камеру на игроке
        self.player.screen.fill((30, 30, 30))
        # for background_rect in self.background_rects:
        #     topleft = background_rect.topleft + offset
        #     pg.draw.rect(self.player.screen, (200, 50, 70), (topleft, background_rect.size))

        self.player.screen.blit(self.player.image, self.player.rect.topleft + offset)

    def add_rects(self, rects):
        self.background_rects = rects


def create_map(width, height, all_sprites, land):
    # render_map = pg.Surface((3360, 3360))
    x, y = 0, 0
    for row in land:
        for element in row:
            if element == "В":
                all_sprites.add(Water((x, y)))
            elif element == 'З':
                all_sprites.add(Soil((x, y)))
            x += width
        y += height


def main():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((60, 3300), all_sprites)
    player.add_screen(screen)
    camera = Camera(player)

    # background_rects = [pg.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 20, 20)
    #                     for _ in range(500)]
    # camera.add_rects(background_rects)
    create_map(280, 280, all_sprites, Map.land)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            player.handle_event(event)

        all_sprites.draw(screen)
        all_sprites.update()
        # heading = player.pos - camera
        # camera += heading * 0.05
        # offset = -camera + Vector2(400, 300)  # + 400, 300 to center the player.
        camera.count_camera_pos()

        pg.display.flip()
        clock.tick(60)


main()

pg.quit()
