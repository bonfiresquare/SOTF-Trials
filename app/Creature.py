# -*- coding: utf-8 -*-

import pygame


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #


class Creature:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.color = pygame.Color(0, 0, 0)
        self.energy = 100
        self.injury = 0

