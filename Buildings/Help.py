import pygame
from math import sqrt


class Heal:
    def __init__(self, x, y, screen):
        self.radius = 150
        self.sprite = AnimatedSprite(pygame.image.load("Buildings/HealSprite.png"), 8, 8)  # норм выглядит при time.delay(30)
        self.destroyable = False
        self.screen = screen
        self.heal = 10  # +5 здоровья в сек

        self.sprite.rect.x = x
        self.sprite.rect.y = y
        self.count = 0

    def update(self, x=0, y=0):
        self.sprite.update()

        if x:
            self.sprite.rect.x += x
        if y:
            self.sprite.rect.y += y

        print(self.sprite.rect)

        self.screen.blit(self.sprite.image, self.sprite.rect)

    def help(self, pers):
        self.count += 1
        if int(sqrt((self.sprite.rect.center[0] - pers[0]) ** 2 + (self.sprite.rect.center[1] - pers[1]) ** 2)) < self.radius:
            if self.count % 5 == 0:
                return self.heal
        return 0


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []

        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(columns):
            for i in range(rows):
                if j == columns - 1 and i == rows - 3:
                    return
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (200, 200)))  # Здесь менять scale

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]



# Пример использования

# pygame.init()
# size = width, height = 800, 600
# screen = pygame.display.set_mode(size)
#
# sp = Heal(50, 300, screen)
#
# pygame.display.flip()
# # ожидание закрытия окна:
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((0, 0, 0))
#     sp.update()
#     pygame.display.flip()
# quit()
