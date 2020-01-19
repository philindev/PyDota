import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname,).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def btn(x: int, y: int, screen: pygame.Surface, icon_path: str, shadow: str, text: str,
        mode=False, on_focus=False,
        font_path=r"game\fonts\iFlash 705.ttf",
        size=24, btn_size=None):

    btn_size = btn_size
    if btn_size is None:
        btn_size = 280, 80
    width, height = btn_size
    button = pygame.transform.scale(pygame.image.load(icon_path), (width, height))
    color = (255, 255, 255)
    if mode:
        button = pygame.transform.scale(pygame.image.load(shadow), (width, height))
    if mode or on_focus:
        color = (84, 84, 84)
    font = pygame.font.Font(font_path, size)
    font = font.render(text, 1, color)
    font_rect = font.get_rect()[2:]
    center_x, center_y = width // 2, height // 2
    text_x, text_y = center_x - font_rect[0] // 2, center_y - font_rect[1] // 2
    button.blit(font, (text_x, text_y))
    screen.blit(button, (x, y))


class Menu:
    def __init__(self, width, height):
        self.size = width, height
        self.image = pygame.transform.scale(load_image("game\menu_icons\menu_image1.png"), (width, height))
        self.favicon_image = load_image("game\menu_icons\main_icon.png")
        self.mode = [False, False, False]
        self.on_focus = [False, False, False]
        self.center = width * 5 // 6

    def render(self, screen):
        screen.blit(self.image, self.image.get_rect())
        self.interface(screen)

    def favicon(self):
        return self.favicon_image

    def interface(self, screen):
        width, height = self.size
        y, center = height // 3, self.center
        screen.blit(self.favicon(), (center - 40, y))
        x = center - 140
        y += 110
        texts = ["Start", "Settings", "Exit"]
        for i in range(len(texts)):
            btn(x, y, screen,
                "game\menu_icons\TextBlock1.png",
                "game\menu_icons\ShadowTextBlock1.png",
                texts[i],
                mode=self.mode[i],
                on_focus=self.on_focus[i])
            y += 100

    def events(self, event, **kwargs):
        start_x, start_y = self.center - 140, self.size[1] // 3 + 110
        if event.type == pygame.MOUSEMOTION \
                or event.type == pygame.MOUSEBUTTONDOWN \
                or event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if start_x <= x <= start_x + 280:
                if start_y <= y <= start_y + 80:
                    self.on_focus[0] = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mode[0] = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mode[0] = False
                        if 'start' in kwargs.keys():
                            var = kwargs['start']
                            # => event
                            pygame.event.post(var)
                else:
                    self.on_focus[0] = False
                if start_y + 110 <= y <= start_y + 110 + 80:
                    self.on_focus[1] = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mode[1] = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mode[1] = False
                else:
                    self.on_focus[1] = False
                if start_y + 110 * 2 <= y <= start_y + 110 * 2 + 80:
                    self.on_focus[2] = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mode[2] = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mode[2] = False
                        print('Good buy, gamer!')
                        sys.exit(0)
                else:
                    self.on_focus[2] = False


def main():
    pygame.init()
    pygame.display.set_caption("PyDoka")
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((0, 0, 0))
    # Ставим фавикон и обои на меню
    action = Menu(pygame.display.Info().current_w, pygame.display.Info().current_h)
    pygame.display.set_icon(action.favicon())
    CHANGE = pygame.USEREVENT + 1
    start = pygame.event.Event(CHANGE)

    playing = True
    while playing:
        # Обновление экрана и получение событий
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F11:
                    sys.exit()
            action.events(event, start=start)
            if event.type == CHANGE:
                print('Start')
                return
        # action - главная переменная хранящая класс в котором происходит отрисовка на экране
        action.render(screen)


if __name__ == '__main__':
    main()
    import PG
