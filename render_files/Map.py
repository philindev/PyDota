import pygame as pg

class Map:
    def __init__(self, width, height, mode=False):
        self.width = width
        self.height = height
        if mode:
            self.start_edit()

    def draw_cells(self, surface, cell_size):
        pass

    def start_edit(self):
        """
            Открывает меню разработки карты
        """

        def draw_cells(edge, left, top, size, surface):
            x, y = left, top
            for i in range((size[0] - 2 * left) // edge):
                for j in range((size[1] - 2 * top) // edge):
                    pg.draw.rect(surface, (255, 255, 255), (x, y, edge, edge), 1)
                    x += edge
                y += edge
                x = left

        pg.init()
        size = width, height = 1300, 1000
        screen = pg.display.set_mode(size)
        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            draw_cells(20, 50, 50, size, screen)
            pg.display.flip()

    def render(self):
        """
            Отрисовывает карту
        """
        pass


if __name__ == '__main__':
    Map(800, 800, mode=True)
