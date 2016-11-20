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
    map_size = (250, 250)   # default = (250, 250)
    map_tilesize = 1          # default = 10
    map_stepping = 10         # default = 10
    map_freq_multiplier = 0.8 # default = 0.8
    map_octaves = 64          # default = 64

    map_min_tilesize = 1      # default = 2
    map_max_tilesize = 40     # default = 40

    # hight < map_waterlevel = water
    # hight < map_grasslevel && > map_waterlevel = grass
    # hight > map_grasslevel = mountain
    map_waterlevel = ceil(map_stepping * 0.5)  # default = ceil(map_stepping * 0.5)
    map_grasslevel = ceil(map_stepping * 0.72)   # default = ceil(map_stepping * 0.75)

    map_current_offset = (0, 0)
    map_add_surface_offset = (0, 0)  # additional surface offset (relative to current offset)
    map_current_surface_margin = 5   # margin (no. of tiles) around the visible map - needed to avoid missing tiles

    @staticmethod
    def calc_min_tilesize(_size):
        # Params.map_min_tilesize = Tools.clip(max(ceil((_size[0] / Params.map_size[0]) / 2) * 2,
        #                                          ceil((_size[1] / Params.map_size[1]) / 2) * 2), 4, 40)
        if Params.map_tilesize < Params.map_min_tilesize:
            Params.map_tilesize = Params.map_min_tilesize

    @staticmethod
    def increase_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize + 1, Params.map_min_tilesize, Params.map_max_tilesize)

    @staticmethod
    def decrease_tilesize():
            Params.map_tilesize = Tools.clip(Params.map_tilesize - 1, Params.map_min_tilesize, Params.map_max_tilesize)

    #@staticmethod
    #def create_map_surface():
    #    screen_center = (ceil(Params.window_size[0] / 2), ceil(Params.window_size[1] / 2))
    #    surf_width = Params.map_size[0]
    #    surf_height = Params.map_size[1]

    #    # center map surface offset position
    #    Params.map_current_offset = (screen_center[0] - (surf_width / 2),
    #                                 screen_center[1] - (surf_height / 2))

    #    # create surface and fill every pixels with tile colors
    #    Params.map_surface = pygame.Surface((surf_width, surf_height))
    #    _tileset = Tileset.get_instance()
    #    for x in range(surf_width):
    #        for y in range(surf_height):
    #            tile_color = _tileset.get_color_of(x, y)
    #            Params.map_surface.set_at((x, y), tile_color)

    #@staticmethod
    #def zoom_map_surface():
    #    new_width = ceil(Params.map_tilesize * Params.map_size[0])
    #    new_height = ceil(Params.map_tilesize * Params.map_size[1])
    #    Params.curr_map_surface = pygame.transform.scale(Params.map_surface, (new_width, new_height))
    #    return Params.curr_map_surface
