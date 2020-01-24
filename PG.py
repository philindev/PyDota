import pygame as pg
from pygame.math import Vector2

from map import Map
import Buildings
import fix.cutter as cutter
from sprites import Player
from sprites import Creep


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

    team_blue = list()
    team_red = list()
    towers = list()

    creep_s_kd = 0
    creep_kd = 0


    spawn_red_points = [[i, j] for i in range(0, 200, 50) for j in range(0, 200, 50)]
    spawn_blue_points = [[i, j] for i in range(0, 200, 50) for j in range(0, 200, 50)]

    for _ in spawn_red_points:
        extra_x, extra_y = pg.display.Info().current_w + 280 * 2, pg.display.Info().current_h - 280 * 3
        unit = Creep(True, [_[0] + extra_x // 2, _[1] + extra_y // 2])
        unit.add_screen(screen)
        team_red.append(unit)

    for _ in spawn_blue_points:
        extra_x, extra_y = pg.display.Info().current_w + 280 * 2, pg.display.Info().current_h // 2
        unit = Creep(False, [_[0] + extra_x, _[1] + extra_y])
        unit.add_screen(screen)
        team_blue.append(unit)

    beings = [team_blue, team_red, towers]
    sprite_objects.append(world)

    def draw_again_after_death(cords, boost):
        x, y = cords
        print(x, y)
        world.rect.x += x
        world.rect.y += y
        for obj in beings:
            for unit in obj:
                unit.cords[0] += x
                unit.cords[1] += y
                unit.spawn_point[0] += x
                unit.spawn_point[1] += y

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

        blue_pos = [i.cords for i in team_blue]
        blue_collide = [i.collision() for i in team_blue]

        red_pos = [i.cords for i in team_red]
        red_collide = [i.collision() for i in team_red]

        blue_feed = red_pos.copy()
        blue_feed.append(player.cords)

        creep_s_kd += 1
        creep_kd += 1

        if fill:
            player.move(sprite_objects, beings)

        for _ in sprite_objects:
            screen.blit(_.image, _.rect)

        for unit in team_red:
            unit.draw()
            unit.move(blue_pos)
            unit.health_bar()
            unit.check_health()
            unit.take_damage_f_creep(blue_pos, unit.attack())

        for unit in team_blue:
            unit.draw()
            unit.move(blue_feed)
            unit.health_bar()
            unit.check_health()
            unit.take_damage_f_creep(red_pos, unit.attack())

            if creep_kd % 40 == 0:
                player.take_damage_f_creep(unit.cords, unit.attack())

        player.draw()
        player.check_health(draw_again_after_death)

        pg.display.flip()
        clock.tick(60)


main()
pg.quit()
