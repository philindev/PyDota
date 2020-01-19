import pygame as pg
from sprites import Water, Soil
import pprint


class Map:

    land = ["ВВВВВВВВЗЗЗЗ ",
            "ВВВВВВВВЗЗЗЗ",
            "ВВВВВВВЗЗЗЗВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВЗЗЗВВВВ",
            "ВВВВЗЗЗВВВВВ",
            "ВВВЗЗЗЗВВВВВ",
            "ВВЗЗЗЗВВВВВВ",
            "ВЗЗЗЗВВВВВВВ",
            "ВЗЗЗЗВВВВВВВ"]

    def __init__(self):
        self.block_size = 280
        self.land = Map.land
        self.image = pg.Surface((3360, 3360))
        self.rect = self.image.get_rect()


    @staticmethod
    def double_map(land):
        output = [''] * 9
        for _ in range(9):
            for __ in land[_]:
                print(__)
                output[_] += __ * 2
        print(output)
        return output

    def create_map(self, all_sprites, focused_player):
        land = self.land
        x, y = 0, 0
        render_map = pg.Surface((3360, 3360))
        for row in land:
            for element in row:
                if element == "В":
                    w = Water((x, y), all_sprites, focused_player)
                    render_map.blit(w.image, w.rect)
                elif element == 'З':
                    s = Soil((x, y), all_sprites, focused_player)
                    render_map.blit(s.image, s.rect)
                x += self.block_size
            x = 0
            y += self.block_size
        self.image = render_map
        self.rect = render_map.get_rect()

    def throught_the_errors(self, land):

        lost_x, lost_y = pg.display.Info().current_w // self.block_size // 2 + 2, \
                         pg.display.Info().current_h // self.block_size // 2 + 2

        top_edge = ["В" * (pg.display.Info().current_w // self.block_size)] * lost_y
        bottom_edge = top_edge.copy()
        left_edge = ["В" * lost_x] * len(land)
        right_edge = left_edge.copy()
        final = list(top_edge)
        for _ in range(len(land)):
            final.append(left_edge[_] + land[_] + right_edge[_])
        final += bottom_edge
        self.land = final

    def add_screen(self, screen):
        self.screen = screen
