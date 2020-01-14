import pygame as pg
from pygame.math import Vector2


class Map:
    land = ["ВВВВВВВВЗЗЗЗ",
            "ВВВВВВВЗЗЗЗВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВВЗЗЗВВВ",
            "ВВВВВЗЗЗВВВВ",
            "ВВВВЗЗЗВВВВВ",
            "ВВВЗЗЗЗВВВВВ",
            "ВВЗЗЗЗВВВВВВ",
            "ВЗЗЗЗВВВВВВВ"]

    def __init__(self, screen):
        self.screen = screen

    @staticmethod
    def double_map(land):
        output = [''] * 9
        for _ in range(9):
            for __ in land[_]:
                print(__)
                output[_] += __ * 2
        print(output)
        return output





