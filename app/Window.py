# -*- coding: utf-8 -*-

from math import fabs
from math import floor
from random import randint
import pickle
import pygame
from map.Tileset import *
from Params import *
from Creature import *


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
        self.fps = 0
        self.size = Params.window_size
        self.screen = pygame.display.set_mode(self.size)
        self.caption = "Pygame Window"
        self.toFullscreen = 0
        self.tileset = None
        self.map_surface = None
        self.curr_map_surface = None
        self.curr_creature = Creature()
        pygame.display.set_caption(self.caption)
        self.map_surface = pygame.Surface(Params.map_size)
        self.curr_map_surface = pygame.Surface(Params.map_size)
        self.buffer_surface = pygame.Surface((1, 1))
        self.buffer_surface.set_colorkey(Params.buffer_color_key)
        self.buffer_aa_surface = self.buffer_surface.copy()
        pygame.display.set_caption("PyGame Window")
        pygame.mouse.set_cursor(*Window.get_cursor_data('std'))
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(200, 10)

    @staticmethod
    def save():
        _win = Window.__instance
        # clocks don't wanna be saved
        _clk = _win.clk
        _win.clk = None
        with open("savegame", "wb") as file:
            pickle.dump(_win, file)
        _win.clk = _clk

    @staticmethod
    def load():
        # FIXME: execution fails after loading, try to save only relevant things (eg heightmap)
        with open("savegame", "rb") as file:
            Window.__instance = pickle.load(file)
            Window.__instance.clk = pygame.time.Clock()

    def update(self):
        self.clk.tick(60)
        pygame.display.flip()
        # update FPS ticker in window caption
        _fps = int(self.clk.get_fps())
        if not self.fps == _fps:
            self.fps = _fps
            _fps_string = ' - ' + str(self.fps) + ' FPS'
            pygame.display.set_caption(self.caption + _fps_string)

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
        self.render_screen()  # draw map on screen

    def render_screen(self):
        self.render_curr_map_surface()
        self.render_creatures()
        curr_offset = (Params.map_current_offset[0] + Params.map_add_surface_offset[0],
                       Params.map_current_offset[1] + Params.map_add_surface_offset[1])
        self.screen.blit(self.curr_map_surface, curr_offset)  # display current map on screen

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

        # center initial map surface offset position
        Params.map_current_offset = (screen_center[0] - (surf_width / 2),
                                     screen_center[1] - (surf_height / 2))

        # fill each pixel of map surface with tile color
        for x in range(Params.map_size[0]):
            for y in range(Params.map_size[1]):
                tile_color = self.tileset.get_color_of(x, y)
                self.map_surface.set_at((x, y), tile_color)

    def get_centered_zoom_offset(self, _old_tile_size, _new_tile_size):
        screen_center = (ceil(self.size[0] / 2), ceil(self.size[1] / 2))
        _curr_offset = Params.map_current_offset

        # get pixel position of screen center relative to offset/map position
        center_map_surface = (abs(_curr_offset[0] - screen_center[0]),
                              abs(_curr_offset[1] - screen_center[1]))

        # calculate new offset to keep the current screen center
        new_offset = (round(screen_center[0] - (center_map_surface[0] * (_new_tile_size / _old_tile_size))),
                      round(screen_center[1] - (center_map_surface[1] * (_new_tile_size / _old_tile_size))))

        # print('New offset: ',new_offset)
        return new_offset

    @staticmethod
    def get_tile_by_map_position(_position):
        curr_tile = (ceil(_position[0] / Params.map_tilesize),
                     ceil(_position[1] / Params.map_tilesize))
        return curr_tile

    def get_displayed_tile(self, _which_one):
        # get (first displayed pixel of map) - render margin
        if _which_one == 'FIRST':
            curr_x = (Params.map_current_offset[0] * (-1)) - Params.win_render_margin
            curr_y = (Params.map_current_offset[1] * (-1)) - Params.win_render_margin

        # get (last displayed pixel of map) + render margin
        elif _which_one == 'LAST':
            curr_x = (Params.map_current_offset[0] * (-1)) + self.size[0] + Params.win_render_margin
            curr_y = (Params.map_current_offset[1] * (-1)) + self.size[1] + Params.win_render_margin

        else:
            try:
                raise NotImplementedError('!!! Check usage of FIRST and LAST parameters in Window.get_displayed_tile()')
            except NotImplementedError as e:
                print(e)

        # find last x-position
        _x = Window.get_tile_by_map_position((curr_x, 0))
        x = Tools.clip(_x[0], 0, Params.map_size[0])

        # find last y-position
        _y = Window.get_tile_by_map_position((0, curr_y))
        y = Tools.clip(_y[1], 0, Params.map_size[1])

        return x, y

    def rect_is_on_curr_map(self, _rect):  # returns if the input position is on curr_map_surface
        # _rect is a rectangle positioned on the map at tilesize = max_tilesize

        _corner = {0: _rect.topleft,
                   1: _rect.topright,
                   2: _rect.bottomleft,
                   3: _rect.bottomright}

        for i in _corner:  # repeat for all 4 corners of _rect

            curr_pos = _corner[i]

            # get _map_position for current scaling
            curr_x = round((curr_pos[0] / Params.map_max_tilesize) * Params.map_tilesize)
            curr_y = round((curr_pos[1] / Params.map_max_tilesize) * Params.map_tilesize)

            # get first and last rendered pixels relative to map_curr_offset
            first_pixel = self.get_displayed_tile('FIRST')
            first_pixel = (first_pixel[0] * Params.map_tilesize, first_pixel[1] * Params.map_tilesize)
            last_pixel = self.get_displayed_tile('LAST')
            last_pixel = (last_pixel[0] * Params.map_tilesize, last_pixel[1] * Params.map_tilesize)

            # check if position is on curr_map_surface
            if (first_pixel[0] < curr_x <= last_pixel[0] and
                    first_pixel[1] < curr_y <= last_pixel[1]):
                return True

        return False

    def render_curr_map_surface(self):
        # get first displayed tile
        first_tile = self.get_displayed_tile('FIRST')
        # get last displayed tile
        last_tile = self.get_displayed_tile('LAST')

        size = (last_tile[0] - first_tile[0],
                last_tile[1] - first_tile[1])

        # scale curr_map to the viewn section and insert map section
        # self.curr_map_surface = pygame.transform.scale(self.curr_map_surface, (width, height))
        # self.curr_map_surface.blit(self.map_surface, (0, 0), (first_tile, last_tile))

        # alternative: define curr_map_surface as subsurface of map_surface
        curr_rect = pygame.Rect(first_tile, size)
        self.curr_map_surface = self.map_surface.subsurface(curr_rect)

        # scale curr_map to the tile size
        size = (size[0] * Params.map_tilesize,
                size[1] * Params.map_tilesize)
        self.curr_map_surface = pygame.transform.scale(self.curr_map_surface, size)

        # update additional surface offset
        Params.map_add_surface_offset = (first_tile[0] * Params.map_tilesize,
                                         first_tile[1] * Params.map_tilesize)

    def render_buffer_to_curr_map(self, _map_position, _max_size):  # scales + renders buffer_surface to a map position
        # _map_position is the centered position of where to draw buffer_surface to the map (at tilesize = max_tilesize)
        # _max_size is the target size of buffer_surface (at tilesize = max_tilesize)
        orig_size = self.buffer_surface.get_size()
        if not all(orig_size):  # check if buffer has length|width == 0
            return

        rect = pygame.Rect(_map_position, _max_size)
        if not self.rect_is_on_curr_map(rect):  # check if buffer would be on curr. rendered map surface
            return

        # get first rendered pixel relative to map_curr_offset
        first_pixel = self.get_displayed_tile('FIRST')
        first_pixel = (first_pixel[0] * Params.map_tilesize, first_pixel[1] * Params.map_tilesize)

        # get position (top-left pixel) relative to map_current_offset
        scaled_pos = (round(((_map_position[0] - (_max_size[0] / 2)) / Params.map_max_tilesize) * Params.map_tilesize),
                      round(((_map_position[1] - (_max_size[1] / 2)) / Params.map_max_tilesize) * Params.map_tilesize))

        # get position relative to curr. displayed map surface (curr_map_surface)
        render_pos = (scaled_pos[0] - first_pixel[0], scaled_pos[1] - first_pixel[1])

        # scale the original size (max_tilesize) to the current zoom (tilesize)
        render_size = (round((_max_size[0] / Params.map_max_tilesize) * Params.map_tilesize),
                       round((_max_size[1] / Params.map_max_tilesize) * Params.map_tilesize))

        if Params.buffer_antialiasing:
            # create rect, whose inside is the area of the curr_map where the buffer will be rendered
            aa_rect = pygame.Rect(render_pos, render_size)
            curr_map_rect = pygame.Rect((0, 0), self.curr_map_surface.get_size())
            aa_rect = curr_map_rect.clip(aa_rect)  # gets the intersection
            self.buffer_aa_surface = self.curr_map_surface.subsurface(aa_rect)
            self.buffer_aa_surface = pygame.transform.scale(self.buffer_aa_surface, orig_size)
            self.buffer_aa_surface.blit(self.buffer_surface, (0, 0))
            # self.buffer_aa_surface = pygame.transform.smoothscale(self.buffer_aa_surface,  # has no affect
            #                                                           (orig_size[0] * 2, orig_size[1] * 2))
            self.buffer_aa_surface = pygame.transform.smoothscale(self.buffer_aa_surface, render_size)

            # draw the antialiased buffer_surface to the curr_map_surface
            self.curr_map_surface.blit(self.buffer_aa_surface, render_pos)
        else:
            self.buffer_surface = pygame.transform.scale(self.buffer_surface, render_size)

            # draw the buffer_surface to the curr_map_surface
            self.curr_map_surface.blit(self.buffer_surface, render_pos)

    def render_creatures(self):  # calls render_creature for every visible creature

        # iterable and mutable list for all needed-to-draw creatures
        _toDraw = {
            self.create_dummy_creature,
            self.render_curr_creature
        }

        for creature in _toDraw:
            creature()

        # previously:
        # for i in range(1):
        #     self.create_dummy_creature()
        #     self.render_curr_creature()

    def render_curr_creature(self):  # renders creature on curr_map_surface
        # specify parameters
        if Params.buffer_antialiasing:
            radius = self.curr_creature.size     # double circle radius for better antialiasing
        else:
            radius = round(self.curr_creature.size / 2)
        size = (radius * 2 + 1, radius * 2 + 1)  # 1 tolerance pixel to avoid later rounding issues (position- and
        pos = (radius, radius)                   # radius-precision are not affected
        border_width = 0

        # check if creature is on curr. rendered map surface
        rect = pygame.Rect(self.curr_creature.x, self.curr_creature.y,
                           size[0], size[1])
        if not self.rect_is_on_curr_map(rect):
            return
        # get first and last rendered pixels relative to map_curr_offset
        first_pixel = self.get_displayed_tile('FIRST')
        first_pixel = (first_pixel[0] * Params.map_tilesize, first_pixel[1] * Params.map_tilesize)
        last_pixel = self.get_displayed_tile('LAST')
        last_pixel = (last_pixel[0] * Params.map_tilesize, last_pixel[1] * Params.map_tilesize)
        # FIXME eventually: not used values 'first_pixel' and 'last_pixel'

        # adjust buffer_surface
        # fill buffer with transparent color key:
        self.buffer_surface.fill(Params.buffer_color_key)
        # scale buffer to creature size:
        self.buffer_surface = pygame.transform.scale(self.buffer_surface, size)
        # draw circle at buffer
        pygame.draw.circle(self.buffer_surface, self.curr_creature.color, pos, radius, border_width)

        # render buffer_surface on curr_map_surface
        self.render_buffer_to_curr_map((self.curr_creature.x, self.curr_creature.y),
                                       (self.curr_creature.size, self.curr_creature.size))

    def create_dummy_creature(self):  # created dummy creature in the center of the map
        self.curr_creature.x = (Params.map_size[0] / 2) * Params.map_max_tilesize + 10
        self.curr_creature.y = (Params.map_size[1] / 2) * Params.map_max_tilesize + 10
        self.curr_creature.color = pygame.Color(255, 255, 0)
        self.curr_creature.size = round(Params.map_max_tilesize / 1.5)

        # random creatures (for performance testing):
        # self.curr_creature.x = randint(0, Params.map_size[0] * Params.map_max_tilesize)
        # self.curr_creature.y = randint(0, Params.map_size[1] * Params.map_max_tilesize)
        # self.curr_creature.color = pygame.Color(randint(0, 255), randint(0, 255), randint(0, 255))
        # self.curr_creature.size = randint(round(Params.map_max_tilesize / 3), Params.map_max_tilesize * 2)

    @staticmethod
    def get_tile_by_map_position(_position):
        curr_tile = (ceil(_position[0] / Params.map_tilesize),
                     ceil(_position[1] / Params.map_tilesize))
        return curr_tile

    @staticmethod
    def get_cursor_data(_this_one):
        cursors = {
            'std': (  # sized 16x16
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
                "     XXXXX XX   "),

            'lmb': (  # sized 16x16
                "   XX           ",
                "  X..X          ",
                "  X..X          ",
                "  X..X          ",
                "   X..X XXXX    ",
                "   X..XX..X.XX  ",
                "   XX..X..X.X.X ",
                "  X.X..X..X.X.X ",
                " X..X.........X ",
                " X............X ",
                "  X....X.X.X..X ",
                "  X....X.X.X..X ",
                "   X...X.X.X.X  ",
                "    X........X  ",
                "     X....X.X   ",
                "     XXXXX XX   "),

            'rmb': (  # sized 16x16
                "   XX  XX       ",
                "  X..XX..X      ",
                "  X..XX..X      ",
                "  X..XX..X      ",
                "   X..X..XXX    ",
                "   X..XX..X.XX  ",
                "   XX..X..X.X.X ",
                "  X.X..X..X.X.X ",
                " X..X.........X ",
                " X............X ",
                "  X....X.X.X..X ",
                "  X....X.X.X..X ",
                "   X...X.X.X.X  ",
                "    X........X  ",
                "     X....X.X   ",
                "     XXXXX XX   "),

            'drg': (  # sized 16x16
                "   XX  XX       ",
                "  X..XX..X      ",
                "  X..XX..X      ",
                "  X..XX..X      ",
                "  X..XX..XXX    ",
                "   X..XX..X.XX  ",
                "   XX..X..X.X.X ",
                "  X.X..X..X.X.X ",
                " X..X.........X ",
                " X............X ",
                "  X....X.X.X..X ",
                "  X....X.X.X..X ",
                "   X...X.X.X.X  ",
                "    X........X  ",
                "     X....X.X   ",
                "     XXXXX XX   "),

            'drg2': (  # sized 16x16
                "       XX       ",
                "      X..X      ",
                "     X....X     ",
                "    X..XX..X    ",
                "   XXXX..XXXX   ",
                "  X.X X..X X.X  ",
                " X..XX.XX.XX..X ",
                "X..X..X  X..X..X",
                "X..X..X  X..X..X",
                " X..XX.XX.XX..X ",
                "  X.X X..X X.X  ",
                "   XXXX..XXXX   ",
                "    X..XX..X    ",
                "     X....X     ",
                "      X..X      ",
                "       XX       ")
        }

        _cur_file, _cur_mask = pygame.cursors.compile(cursors[_this_one], 'X', '.')
        return (16, 16), (3, 1), _cur_file, _cur_mask

    @staticmethod
    def destroy():
        pygame.quit()
        Window.__instance = None
