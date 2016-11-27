# -*- coding: utf-8 -*-

from Tools import *
from math import ceil
from abc import ABC

from map.Tileset import *
import pygame

#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Params(ABC):

    window_size = (1200, 800)
    map_size = (500, 500)       # default = (250, 250)
    map_tilesize = 2            # default = 10
    map_stepping = 16           # default = 10
    map_freq_multiplier = 0.7   # default = 0.8
    map_octaves = 64            # default = 64

    map_min_tilesize = 1        # default = 2
    map_max_tilesize = 20       # default = 40

    # height < map_waterlevel = water
    # height < map_grasslevel && > map_waterlevel = grass
    # height > map_grasslevel = mountain
    map_waterlevel = ceil(map_stepping * 0.45)  # default = ceil(map_stepping * 0.5)
    map_grasslevel = ceil(map_stepping * 0.65)   # default = ceil(map_stepping * 0.75)

    map_current_offset = (0, 0)
    map_add_surface_offset = (0, 0)  # additional surface offset (relative to current offset)
    win_render_margin = 40           # rendered margin around the visible map - needed to avoid missing tiles

    @staticmethod
    def scale_tilesize(_whereto):
        _delta = 1 if _whereto == 'ZOOM_IN' else -1  # if _whereto == 'ZOOM_OUT'
        Params.map_tilesize = Tools.clip(Params.map_tilesize + _delta, Params.map_min_tilesize, Params.map_max_tilesize)
