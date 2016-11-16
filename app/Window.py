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
        self.width = Params.window_width
        self.height = Params.window_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.toFullscreen = 0
        pygame.display.set_caption("PyGame Window")
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)

    def update(self):
        self.clk.tick(30)
        pygame.display.flip()

    def create_map(self):
        self.tileset = Tileset(Params.map_width, Params.map_height, Params.map_stepping)
        self.tileset.create_heightmap(Params.map_freq_multiplier, Params.map_octaves)
        self.tileset.create_tileset()

    def draw_tileset(self, _fov_x, _fov_y, _offset_x, _offset_y):
        for k in range(_fov_y):
            for i in range(_fov_x):
                try:
                    self.screen.fill(self.tileset.get_color_of(i + _offset_x, k + _offset_y),
                                     (i * Params.map_tilesize,
                                      k * Params.map_tilesize,
                                      Params.map_tilesize,
                                      Params.map_tilesize))
                except KeyError:
                    pass

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

        intended_size = (0,0) if self.toFullscreen else (Params.window_width, Params.window_height)

        self.screen = pygame.display.set_mode(intended_size, flags ^ pygame.FULLSCREEN, bitsize)

        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h

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
        return (self.width, self.height)


    @staticmethod
    def destroy():
        pygame.quit()
        Window.__instance = None