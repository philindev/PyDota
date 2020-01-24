import pygame as pg
from pygame.math import Vector2

from map import Map
from sprites import Player
from sprites import Creep, Giant
from Buildings.Buildings import RadiusTower


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
    print(str(pg.display.Info().current_w) + ' x ' + str(pg.display.Info().current_h) + " разрешение экарана")

    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    sprite_objects = list()

    player = Player()
    player.add_screen(screen)

    world = Map()
    world.add_screen(screen)
    allowed = world.create_map(all_sprites, player)

    team_blue = list()
    team_red = list()
    towers = list()

    heal1 = RadiusTower(1920 - 280 * 4, 1080 - 280 * 4, screen)
    damage1 = heal1.update()
    heal2 = RadiusTower(1920, 1080 - 280 * 5, screen)
    damage2 = heal2.update()

    dire1 = RadiusTower(1920 - 280 - 70, 1080 - 280 * 7 - 70, screen)
    ddamage1 = dire1.update()
    dire2 = RadiusTower(1920 + 280 * 2, 1080 - 280 * 8, screen)
    ddamage2 = dire2.update()

    creep_s_kd = 0
    creep_kd = 0

    spawn_red_points = [[i, j] for i in range(0, 200, 50) for j in range(0, 200, 50)]
    spawn_blue_points = [[i, j] for i in range(0, 200, 50) for j in range(0, 200, 50)]

    rgig_list = list()
    bgig_list = list()

    for i in range(3):
        a = Giant(True, [1920 + 280 * 2, 1080 - 280 * 3])
        b = Giant(False, [2200, - 1000])
        rgig_list.append(a)
        bgig_list.append(b)

    for _ in spawn_red_points:
        extra_x, extra_y = 1920 + 280 * 2, 1080 - 280 * 3
        unit = Creep(True, [_[0] + extra_x // 2, _[1] + extra_y // 2])
        unit.add_screen(screen)
        team_red.append(unit)

    for _ in spawn_blue_points:
        extra_x, extra_y = 2200, - 1000
        unit = Creep(False, [_[0] + extra_x, _[1] + extra_y])
        unit.add_screen(screen)
        team_blue.append(unit)

    beings = [team_blue, team_red, towers, allowed]
    sprite_objects.append(world)
    sprite_objects.append(heal1)
    sprite_objects.append(heal2)
    sprite_objects.append(dire1)
    sprite_objects.append(dire2)

    def draw_again_after_death(cords, boost):
        x, y = cords
        for _ in sprite_objects:
            _.rect.y += y
            _.rect.x += x
        count = 0
        for obj in beings:
            count += 1
            if count == 4:
                for i in obj:
                    i[0] += x
                    i[1] += y
                continue
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
                if event.key == pg.K_F10:
                    world.print_pos()

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
            player.move(sprite_objects, beings, allowed)

        for _ in sprite_objects:
            screen.blit(_.image, _.rect)

        dire1.attack(team_red, team_red[0].sprite.rect.center)
        ddamage1 = dire1.update()
        dire2.attack(team_red, team_red[0].sprite.rect.center)
        ddamage2 = dire2.update()

        for unit in team_red:
            unit.draw()
            unit.move(blue_pos)
            unit.health_bar()
            unit.check_health()
            unit.take_damage_f_creep(blue_pos, unit.attack())
            if not ddamage1:
                ddamage1 = dire1.update()
                if ddamage1:
                    unit.take_damage_f_pl(ddamage1[0], ddamage1[1])
            else:
                unit.take_damage_f_pl(ddamage1[0], ddamage1[1])
            if not ddamage2:
                ddamage2 = dire2.update()
                if ddamage2:
                    unit.take_damage_f_pl(ddamage2[0], ddamage2[1])
            else:
                unit.take_damage_f_pl(damage2[0], damage2[1])

        heal1.attack(team_blue, team_blue[0].sprite.rect.center)
        damage1 = heal1.update()
        heal2.attack(team_blue, team_blue[0].sprite.rect.center)
        damage2 = heal2.update()

        for unit in team_blue:
            unit.draw()
            unit.move(blue_feed)
            unit.health_bar()
            unit.check_health()
            unit.take_damage_f_creep(red_pos, unit.attack())
            if not damage1:
                damage1 = heal1.update()
                if damage1:
                    unit.take_damage_f_pl(damage1[0], damage1[1])
            else:
                unit.take_damage_f_pl(damage1[0], damage1[1])
            if not damage2:
                damage2 = heal2.update()
                if damage2:
                    unit.take_damage_f_pl(damage2[0], damage2[1])
            else:
                unit.take_damage_f_pl(damage2[0], damage2[1])

            if creep_kd % 40 == 0:
                player.take_damage_f_creep(unit.cords, unit.attack())

            if fill:
                if player.chase(p, unit.cords, unit.RAD):
                    unit.take_damage_f_pl(player.cords, player.attack())

        player.draw()
        player.check_health(draw_again_after_death)

        pg.display.flip()
        clock.tick(60)


main()
pg.quit()
