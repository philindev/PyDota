from random import randrange

import pygame as pg
from pygame.math import Vector2
import Buildings


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
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


def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))

    back = pg.sprite.Sprite()
    back.image = pg.transform.scale(pg.image.load('new.png'), (3350, 3350))
    rect = back.image.get_rect()

    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    camera = Vector2(400, 300)
    player = Player((400, 300), all_sprites)

    background_rects = [Buildings.ShopTower(randrange(0, 800), randrange(0, 800), screen), Buildings.PointTower(randrange(0, 800), randrange(0, 800), screen),
                        Buildings.RadiusTower(randrange(0, 800), randrange(0, 800), screen)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            player.handle_event(event)
        screen.blit(back.image, rect)
        all_sprites.update()
        # A vector that points from the camera to the player.
        heading = player.pos - camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        offset = -camera + Vector2(400, 300)  # + 400, 300 to center the player.

        screen.fill((30, 30, 30))
        topleft = rect.topleft + offset
        screen.blit(back.image, (topleft, rect.size))

        # Blit all objects and add the offset to their positions.
        for background_rect in background_rects:
            topleft = background_rect.rect.topleft + offset
            screen.blit(background_rect.image, (topleft, background_rect.rect.size))

        screen.blit(player.image, player.rect.topleft+offset)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()
