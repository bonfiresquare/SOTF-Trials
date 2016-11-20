# -*- coding: utf-8 -*-

import pygame
from map.Tileset import *
from Params import *
from math import fabs


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Window:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Window.__instance:
            Window.__instance = object.__new__(cls)
        return Window.__instance

    def __init__(self):
        pygame.init()
        self.clk = pygame.time.Clock()
        self.size = Params.window_size
        self.screen = pygame.display.set_mode(self.size)
        self.toFullscreen = 0
        self.tileset = None
        pygame.display.set_caption("PyGame Window")
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(200, 50)

    def update(self):
        self.clk.tick(30)
        pygame.display.flip()

    def create_map(self):
        self.tileset = Tileset(Params.map_size[0],
                               Params.map_size[1],
                               Params.map_stepping,
                               Params.map_waterlevel,
                               Params.map_grasslevel)
        self.tileset.create_heightmap(Params.map_freq_multiplier,
                                      Params.map_octaves)
        self.tileset.create_tileset()

    def draw_tileset(self, _fov, _base_offset, _map_offset):
        _tilesize = Params.map_tilesize
        for k in range(_fov[1]):
            for i in range(_fov[0]):
                try:
                    tile_color = self.tileset.get_color_of(_map_offset[0] + i, _map_offset[1] + k)
                except KeyError:
                    tile_color = pygame.Color(0, 0, 0)
                self.screen.fill(tile_color,
                                 ((_base_offset[0] + i) * _tilesize,
                                  (_base_offset[1] + k) * _tilesize,
                                  _tilesize,
                                  _tilesize))

    def capture(self, _filename):
        pygame.image.save(self.screen, _filename)

    def toggle_fullscreen(self):
        self.toFullscreen = int(fabs(self.toFullscreen - 1))
        flags = self.screen.get_flags()
        bitsize = self.screen.get_bitsize()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()

        pygame.display.quit()
        pygame.display.init()

        intended_size = (0, 0) if self.toFullscreen else Params.window_size

        self.screen = pygame.display.set_mode(intended_size,
                                              flags ^ pygame.FULLSCREEN,
                                              bitsize)

        self.size = (pygame.display.Info().current_w,
                     pygame.display.Info().current_h)

        Params.calc_min_tilesize(self.get_display_size())

        pygame.display.set_caption(*caption)
        pygame.key.set_mods(0)
        pygame.mouse.set_cursor(*cursor)

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def reset_map(self):
        Tileset.reset_tileset()
        self.tileset = {}

    def get_display_size(self):
        return self.size

    def scroll_map(self, _mouse_movement):
        pass

    @staticmethod
    def destroy():
        pygame.quit()
        Window.__instance = None