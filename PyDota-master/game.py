import sys
import os

import pygame
import map
# import choose_hero.Menu as Menu
# import map.Bar as Bar


class Game:
    def __init__(self, screen):
        super(Game, self).__init__()
        self.playing = True
        self.all_sprites = pygame.sprite.Group()
        self.Map = map.Map(screen)
        self.Map.create_map(self.all_sprites)
        self.player = map.Player((400, 300))
        self.camera = map.Camera(self.player)

    def render(self, screen):
        if self.playing:
            self.camera.count_new_position()
            self.all_sprites.update()
            self.player.update()

    def events(self, event, **kwargs):
        if self.playing:
            self.player.handle_event(event)

