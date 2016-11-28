# -*- coding: utf-8 -*-

import time
import datetime
from Window import *
from Params import *
from Minder import *
from Tools import *

# TODO: outsource the Params values into an *.ini
# TODO: make the main loop a ("Program") class with methods and attributes to store params from *.ini
# TODO: figure out how to store the map and its content efficiently
# TODO: outsource the renderer stuff into an extra class
# TODO: reorganize the Tools classes for better distinction


class Program:
    __instance = None
    __locked = False

    def __new__(cls, *args, **kwargs):
        if not Program.__instance:
            Program.__instance = object.__new__(cls)
        if not Program.__locked:
            Program.__locked = True
            return Program.__instance
        else:
            raise RuntimeError('Already initiated or running')

    def __init__(self):
        self.win = Window()
        self.win.create_map()

        self.user_input = ''
        self.show_screen = True
        self.has_changed = True
        self.general_offset = Params.map_current_offset
        self.arrow_move_speed = 20
        self.drag_flag = False

        self._task = {
            'QUIT': self._quit,
            'SAVE': self._save,
            'LOAD': self._load,
            'TOGGLE_AA': self._toggle_aa,
            'TOGGLE_FULL': self._toggle_full,
            'DRAW': self._draw,
            'CLEAR': self._clear,
            'RESET': self._reset,
            'ZOOM_IN': self._zoom,
            'ZOOM_OUT': self._zoom,
            'MOVE_LEFT': self._move,
            'MOVE_RIGHT': self._move,
            'MOVE_UP': self._move,
            'MOVE_DOWN': self._move,
            'DRAG_ON': self._drag,
            'DRAG_OFF': self._drag_off,
            'CAPTURE': self._capture,
            '': lambda: 'pass'
        }

#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define mainloop ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

    def main(self):
        while self.win:
            self.win.update()

            self.user_input = Minder.have_a_look()

            self._task[self.user_input]()

            if self.drag_flag:
                self._drag()

            if self.show_screen and self.has_changed:
                _display_size = self.win.get_display_size()
                _display_half = (ceil(_display_size[0] / 2),
                                 ceil(_display_size[1] / 2))

                _curr_map_size = (Params.map_size[0] * Params.map_tilesize,
                                  Params.map_size[1] * Params.map_tilesize)

                min_offset = (_display_half[0] - _curr_map_size[0],
                              _display_half[1] - _curr_map_size[1])

                self.general_offset = (Tools.clip(self.general_offset[0], min_offset[0], _display_half[0]),
                                       Tools.clip(self.general_offset[1], min_offset[1], _display_half[1]))

                Params.map_current_offset = self.general_offset

                self.win.clear_screen()
                self.win.render_screen()

                self.has_changed = False

        exit()

    #  _________________________________________________________ #
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define methods ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

    def _quit(self):
        Window.destroy()
        self.win = None
        exit()

    def _save(self):
        Window.save()

    def _load(self):
        Window.load()
        self.win = Window()

    def _toggle_aa(self):
        Params.buffer_antialiasing = not Params.buffer_antialiasing
        self.has_changed = True

    def _toggle_full(self):
        self.win.toggle_fullscreen()
        self.has_changed = True

    def _draw(self):
        self.show_screen = True
        self.has_changed = True

    def _clear(self):
        self.win.clear_screen()
        self.show_screen = False

    def _reset(self):
        self.win.reset_map()
        self.win.create_map()
        self.has_changed = True

    def _zoom(self):
        old_tilesize = Params.map_tilesize
        Params.scale_tilesize(self.user_input)

        # check if zooming at min or max tilesize
        if not old_tilesize == Params.map_tilesize:
            self.general_offset = self.win.get_centered_zoom_offset(old_tilesize, Params.map_tilesize)
            self.has_changed = True

    def _move(self):
        self.general_offset = (self.general_offset[0] + self.arrow_move_speed if self.user_input == 'MOVE_LEFT' else self.general_offset[0],
                               self.general_offset[1] + self.arrow_move_speed if self.user_input == 'MOVE_UP' else self.general_offset[1])
        self.general_offset = (self.general_offset[0] - self.arrow_move_speed if self.user_input == 'MOVE_RIGHT' else self.general_offset[0],
                               self.general_offset[1] - self.arrow_move_speed if self.user_input == 'MOVE_DOWN' else self.general_offset[1])
        self.has_changed = True

    def _drag(self):
        old_general_offset = self.general_offset
        if self.drag_flag:
            _movement = Minder.get_mouse_movement()
            self.general_offset = (self.general_offset[0] + round(_movement[0]),
                                   self.general_offset[1] + round(_movement[1]))
        else:
            self.drag_flag = True
        if not old_general_offset == self.general_offset:
            self.has_changed = True

    def _drag_off(self):
        self.drag_flag = False

    def _capture(self):
        date = str(datetime.datetime.now())
        filename = (date[2:4] + date[5:7] + date[8:10] + '_' +  # date yyMMdd
                    date[11:13] + date[14:16] + date[17:19] +   # time hhmmss
                    '.jpg')
        self.win.capture(filename)


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ initialize ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

if __name__ == '__main__':
    p = Program()
    p.main()
