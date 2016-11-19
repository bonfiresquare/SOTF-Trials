# -*- coding: utf-8 -*-

from noise import snoise2
from random import random
from map.Tools import *
from Tile import *


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Tileset:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Tileset.__instance:
            Tileset.__instance = object.__new__(cls)
        return Tileset.__instance

    def __init__(self, size_x, size_y, _stepping):
        self.size_x = size_x
        self.size_y = size_y
        self.stepping = _stepping
        self.height = {}
        # self.tiles = {}        # TODO: making the tiles being useful
        self.colormap = {}
        self.counter = {}

    def create_heightmap(self, _freq_multiplier, _octaves):
        freq = self.size_x * _freq_multiplier
        offset = round((random() + random()) * 100000)
        # _min, _max = 1000, 0
        for k in range(self.size_y):
            for i in range(self.size_x):
                self.height[i, k] = round((1 + snoise2((i + offset) / freq,
                                                       (k + offset) / freq,
                                                       octaves=_octaves)) * (self.stepping / 2))
                self.colormap[i, k] = Tools.get_color(self.height[i, k], self.stepping)
                # _min = self.height[i, k] if self.height[i, k] < _min else _min
                # _max = self.height[i, k] if self.height[i, k] > _max else _max
                try:
                    self.counter[self.height[i, k]] += 1
                except KeyError:
                    self.counter[self.height[i, k]] = 1
        print('Proportional distribution of heights:')
        for i in self.counter:
            print(i, ':', self.counter[i], '\t->', round((self.counter[i] * 100) / (self.size_x * self.size_y), 2), '%')

    def create_tileset(self):
        # for k in range(self.size_y):
        #     for i in range(self.size_x):
        #         self.tiles[i, k] = Tile(self.height[i, k])
        pass

    def get_color_of(self, _x, _y):
        return self.colormap[int(_x), int(_y)]

    @staticmethod
    def reset_tileset():
        Tileset.__instance = None