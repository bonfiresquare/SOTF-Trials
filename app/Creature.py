# -*- coding: utf-8 -*-

import pygame


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #


class Creature:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

        # moving speed
        self.maxspeed = 100
        self.currspeed = self.maxspeed

        # energy / healthpoints (conumed by time and moving speed)
        self.maxenergy = 100
        self.currenergy = self.maxenergy

        # consumed food (transforms to energy over time)
        self.maxfood = 100
        self.currfood = self.maxfood

        # range of adjacenting tiles that can be detected
        self.viewrange = 1

        self.color = pygame.Color(0, 0, 0)
        self.size = 1

        # self.injury = 0

