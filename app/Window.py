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
        pygame.mouse.set_cursor(*Window.get_cursor_data())
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

        self.create_map_surface()
        Params.map_current_offset = self.get_centered_zoom_offset(1, Params.map_tilesize)  # center map zoom
        self.draw_tileset()  # draw map on screen

    def draw_tileset(self):
        self.render_curr_map_surface()
        curr_offset = (Params.win_render_margin * (-1), Params.win_render_margin * (-1))
        if Params.map_current_offset[0] > 0:
            curr_offset = (curr_offset[0] + Params.map_current_offset[0], curr_offset[1])
        if Params.map_current_offset[1] > 0:
            curr_offset = (curr_offset[0], curr_offset[1] + Params.map_current_offset[1])
        self.screen.blit(self.curr_map_surface,curr_offset)  # display current map on screen

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

    def create_map_surface(self):
        screen_center = (ceil(self.size[0] / 2), ceil(self.size[1] / 2))
        surf_width = Params.map_size[0]
        surf_height = Params.map_size[1]

        # center map surface offset position
        Params.map_current_offset = (screen_center[0] - (surf_width / 2),
                                     screen_center[1] - (surf_height / 2))

        # create surface and fill every pixels with tile colors
        self.map_surface = pygame.Surface((surf_width,surf_height))
        for x in range(surf_width):
            for y in range(surf_height):
                tile_color = self.tileset.get_color_of(x, y)
                self.map_surface.set_at((x, y), tile_color)

        # initialize current map section
        self.curr_map_surface = self.map_surface.copy();

    def get_centered_zoom_offset(self, _old_tile_size, _new_tile_size):
        screen_center = (ceil(self.size[0] / 2), ceil(self.size[1] / 2))
        curr_offset = Params.map_current_offset

        # get pixel position of screen center relative to offset/map position
        center_map_surface = (abs(curr_offset[0] - screen_center[0]),
                              abs(curr_offset[1] - screen_center[1]))

        # calculate new offset to keep the current screen center
        new_offset = (round(screen_center[0] - (center_map_surface[0] * (_new_tile_size / _old_tile_size))),
                      round(screen_center[1] - (center_map_surface[1] * (_new_tile_size / _old_tile_size))))

        print('New offset: ',new_offset)
        return new_offset

    def get_tile_by_map_position(self, _position):
        curr_tile = (ceil(_position[0] / Params.map_tilesize),
                     ceil(_position[1] / Params.map_tilesize))
        return curr_tile

    def get_first_displayed_tile(self):
        # get (first displayed pixel of map) - render margin
        curr_x = (Params.map_current_offset[0] * (-1)) - Params.win_render_margin
        curr_y = (Params.map_current_offset[1] * (-1)) - Params.win_render_margin

        # find first x-position tile:
        first_x = self.get_tile_by_map_position((curr_x, 0))
        x = Tools.clip(first_x[0], 0, Params.map_size[0])

        # find first y-position:
        first_y = self.get_tile_by_map_position((0, curr_y))
        y = Tools.clip(first_y[1], 0, Params.map_size[1])

        first_tile = (x,y)
        return first_tile

    def get_last_displayed_tile(self):
        # get (last displayed pixel of map) + render margin
        curr_x = (Params.map_current_offset[0] * (-1)) + self.size[0] + Params.win_render_margin
        curr_y = (Params.map_current_offset[1] * (-1)) + self.size[1] +  Params.win_render_margin

        # find last x-position
        last_x = self.get_tile_by_map_position((curr_x, 0))
        x = Tools.clip(last_x[0], 0, Params.map_size[0])

        # find last y-position
        last_y = self.get_tile_by_map_position((0, curr_y))
        y = Tools.clip(last_y[1], 0, Params.map_size[1])

        last_tile = (x, y)
        return last_tile

    def render_curr_map_surface(self):
        # get first displayed tile
        first_tile = self.get_first_displayed_tile()
        # get last displayed tile
        last_tile = self.get_last_displayed_tile()

        new_width = (last_tile[0] - first_tile[0])
        new_height = (last_tile[1] - first_tile[1])

        # scale curr_map to the viewn section and insert map section
        self.curr_map_surface = pygame.transform.scale(self.curr_map_surface,(new_width,new_height))
        self.curr_map_surface.blit(self.map_surface, (0, 0), (first_tile, last_tile))

        # scale curr_map to the tile size
        new_width *= Params.map_tilesize
        new_height *= Params.map_tilesize
        self.curr_map_surface = pygame.transform.scale(self.curr_map_surface, (new_width, new_height))

        # update additional surface offset
        Params.map_add_surface_offset = first_tile * Params.map_tilesize

    @staticmethod
    def get_cursor_data():
        cursor_strings = (  # sized 16x16
            "   XX           ",
            "  X..X          ",
            "  X..X          ",
            "   X..X         ",
            "   X..X XXXX    ",
            "    X..X..X.XX  ",
            "   XX..X..X.X.X ",
            "  X.X..X..X.X.X ",
            " X..X.........X ",
            " X............X ",
            "  X....X.X.X..X ",
            "  X....X.X.X..X ",
            "   X...X.X.X.X  ",
            "    X........X  ",
            "     X....X.X   ",
            "     XXXXX XX   ")
        _cur_file, _cur_mask = pygame.cursors.compile(cursor_strings, '.', 'X')
        return ((16, 16), (3, 1), _cur_file, _cur_mask)

    @staticmethod
    def destroy():
        pygame.quit()
        Window.__instance = None