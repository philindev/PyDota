import pygame as pg
from sprites import Water, Soil
from pprint import pprint


class Map:

    land = ["                 ",
            "                 ",
            "        ХВВВВМ   ",
            "        ЛЗЗЗЗП   ",
            "       ХЭЗЗЗЗП   ",
            "      ХЭЗЗЗЗИС   ",
            "     ХЭЗЗЗЗИС    ",
            "    ХЭЗЗЗЗИС     ",
            "   ХЭЗЗЗЗИС      ",
            "   ЛЗЗЗЗИС       ",
            "   ЛЗЗЗЗП        ",
            "   РННННД        ",
            "                 ",
            "                 "]

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
        print("Preview-map:\n")
        pprint(land)

        x, y = 0, 0
        mask = list()
        render_map = pg.Surface((len(land[0]) * 280, len(land) * 280))

        for row in land:
            for element in row:
                if element == " ":
                    w = Water((x, y), all_sprites, focused_player)
                    render_map.blit(w.image, w.rect)
                elif element == 'З':
                    s = Soil((x, y), all_sprites, type="solid")
                    render_map.blit(s.image, s.rect)
                    # x1, x2, y1, y2
                    mask.append([x - 720, y - 2200])
                elif element == "Д":
                    s = Soil((x, y), all_sprites, type="edge", side="corner_right_bottom")
                    render_map.blit(s.image, s.rect)
                elif element == "Н":
                    s = Soil((x, y), all_sprites, type="edge", side="bottom")
                    render_map.blit(s.image, s.rect)
                elif element == "Р":
                    s = Soil((x, y), all_sprites, type="edge", side="corner_left_bottom")
                    render_map.blit(s.image, s.rect)
                elif element == "Э":
                    s = Soil((x, y), all_sprites, type="edge", side="angle_left_bottom")
                    render_map.blit(s.image, s.rect)
                elif element == "Х":
                    s = Soil((x, y), all_sprites, type="edge", side='angle_left_top')
                    render_map.blit(s.image, s.rect)
                elif element == "П":
                    s = Soil((x, y), all_sprites, type="edge", side="right")
                    render_map.blit(s.image, s.rect)
                elif element == "М":
                    s = Soil((x, y), all_sprites, type="edge", side="corner_right_top")
                    render_map.blit(s.image, s.rect)
                elif element == "В":
                    s = Soil((x, y), all_sprites, type="edge", side="top")
                    render_map.blit(s.image, s.rect)
                elif element == "Л":
                    s = Soil((x, y), all_sprites, type="edge", side="left")
                    render_map.blit(s.image, s.rect)
                elif element == "И":
                    s = Soil((x, y), all_sprites, type="edge", side="angle_right_top")
                    render_map.blit(s.image, s.rect)
                elif element == "С":
                    s = Soil((x, y), all_sprites, type="edge", side="angle_right_bottom")
                    render_map.blit(s.image, s.rect)
                x += self.block_size
            x = 0
            y += self.block_size
        self.image = render_map

        pos = -720, -2200
        self.rect = render_map.get_rect()
        self.rect.x, self.rect.y = pos
        return mask

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

    def print_pos(self):
        print(self.rect.x, self.rect.y)
