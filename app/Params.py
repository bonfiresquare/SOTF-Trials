# -*- coding: utf-8 -*-

from Tools import *
from math import ceil
from abc import ABC


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Params(ABC):

    window_size = (1200, 800)
    map_size = (500, 500)
    map_tilesize = 10
    map_stepping = 8
    map_freq_multiplier = 1
    map_octaves = 64

    map_min_tilesize = 2

    @staticmethod
    def calc_min_tilesize(_size):
        # Params.map_min_tilesize = Tools.clip(max(ceil((_size[0] / Params.map_size[0]) / 2) * 2,
        #                                          ceil((_size[1] / Params.map_size[1]) / 2) * 2), 4, 40)
        if Params.map_tilesize < Params.map_min_tilesize:
            Params.map_tilesize = Params.map_min_tilesize

    @staticmethod
    def increase_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize + 2, Params.map_min_tilesize, 40)

    @staticmethod
    def decrease_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize - 2, Params.map_min_tilesize, 40)