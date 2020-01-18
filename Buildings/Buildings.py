import pygame


class _ABuild(pygame.sprite.Sprite):
    def __init__(self, x, y, screen, radius, sprite, destroyable=False):
        pygame.sprite.Sprite.__init__(self)

        self.radius = radius
        self.image = pygame.image.load(sprite)
        self.destroyable = destroyable
        self.screen = screen

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self, x=0, y=0):
        if x:
            self.rect.x += x
        if y:
            self.rect.y += y

        self.screen.blit(self.image, self.rect)


class _AAttackTower(_ABuild):
    def __init__(self, x, y, screen, xp, damage, radius, sprite):
        super().__init__(x, y, screen, radius, sprite, True)
        self.xp = xp
        self.damage = damage


class RadiusTower(_AAttackTower):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, xp=100, damage=5, radius=1000, sprite='RadiusTower.png')

        self.period = 5000  # башня стреляет раз в 5 секунд (5000 миллисекунд)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)


class PointTower(_AAttackTower):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, xp=100, damage=5, radius=500, sprite='PointTower.png')


class ShopTower(_ABuild):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, radius=20, sprite='Shop.png')



# pygame.init()
# size = width, height = 800, 600
# screen = pygame.display.set_mode(size)
#
# sp = ShopTower(50, 50, screen)
#
# pygame.display.flip()
# # ожидание закрытия окна:
# running = True
# clock = pygame.time.Clock()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     pygame.time.delay(30)
#     screen.fill((0, 0, 0))
#     sp.update()
#     pygame.display.flip()
#     print(clock.tick() / 1000)
# quit()
