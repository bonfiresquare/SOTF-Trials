# -*- coding: utf-8 -*-

from Window import *
from Tools import *
from math import ceil
from abc import ABC

#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #


class Params(ABC):

    window_width = 1200
    window_height = 800

    map_width = 300
    map_height = 300
    map_tilesize = 10
    map_stepping = 8
    map_freq_multiplier = 0.8
    map_octaves = 64

    map_min_tilesize = 0

    @staticmethod
    def calc_min_tilesize(_size):
        # screen = Window()
        # res = screen.get_display_size()
        Params.map_min_tilesize = ceil((max(_size[0],
                                            _size[1]) / min(Params.map_width,
                                                           Params.map_height)) / 2) * 2
        Params.map_min_tilesize = Tools.clip(Params.map_min_tilesize, 4, 40)
        Params.map_tilesize = Params.map_min_tilesize if Params.map_tilesize < Params.map_min_tilesize else Params.map_tilesize

    @staticmethod
    def increase_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize + 2, Params.map_min_tilesize, 40)

    @staticmethod
    def decrease_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize - 2, Params.map_min_tilesize, 40)