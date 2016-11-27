# -*- coding: utf-8 -*-

import time
import datetime
from Window import *
from Params import *
from Minder import *
from Tools import *


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define mainloop ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

def main():

    win = Window()
    win.create_map()

    show_screen = True
    has_changed = True
    general_offset = Params.map_current_offset
    arrow_move_speed = 20
    drag_flag = False

    while win:
        win.update()

        user_input = Minder.have_a_look()

        if user_input == 'QUIT':
            Window.destroy()
            win = None
            exit()

        elif user_input == 'SAVE':
            Window.save()

        elif user_input == 'LOAD':
            Window.load()
            win = Window()

        elif user_input == 'TOGGLE_ANTIALIASING':
            Params.buffer_antialiasing = not Params.buffer_antialiasing
            has_changed = True

        elif user_input == 'TOGGLE_FULLSCREEN':
            win.toggle_fullscreen()
            has_changed = True

        elif user_input == 'DRAW':
            show_screen = True
            has_changed = True

        elif user_input == 'CLEAR':
            win.clear_screen()
            show_screen = False

        elif user_input == 'RESET':
            win.reset_map()
            win.create_map()
            has_changed = True

        elif user_input[0:4] == 'ZOOM':
            old_tilesize = Params.map_tilesize
            Params.scale_tilesize(user_input)

            # check if zooming at min or max tilesize
            if not old_tilesize == Params.map_tilesize:
                general_offset = win.get_centered_zoom_offset(old_tilesize, Params.map_tilesize)
                has_changed = True

        elif user_input[0:4] == 'MOVE':
            general_offset = (general_offset[0] + arrow_move_speed if user_input == 'MOVE_LEFT' else general_offset[0],
                              general_offset[1] + arrow_move_speed if user_input == 'MOVE_UP' else general_offset[1])
            general_offset = (general_offset[0] - arrow_move_speed if user_input == 'MOVE_RIGHT' else general_offset[0],
                              general_offset[1] - arrow_move_speed if user_input == 'MOVE_DOWN' else general_offset[1])
            has_changed = True

        elif user_input == 'DRAGGING_OFF':
            drag_flag = False

        elif user_input == 'DRAGGING' or drag_flag:
            old_general_offset = general_offset
            if drag_flag:
                _movement = Minder.get_mouse_movement()
                general_offset = (general_offset[0] + round(_movement[0]),
                                  general_offset[1] + round(_movement[1]))
            else:
                drag_flag = True
            if not old_general_offset == general_offset:
                has_changed = True

        elif user_input == 'CAPTURE':
            date = str(datetime.datetime.now())
            filename = (date[2:4] + date[5:7] + date[8:10] + '_' +  # date yyMMdd
                        date[11:13] + date[14:16] + date[17:19] +   # time hhmmss
                        '.jpg')
            win.capture(filename)

        if show_screen and has_changed:
            _display_size = win.get_display_size()
            _display_half = (ceil(_display_size[0] / 2),
                             ceil(_display_size[1] / 2))

            _curr_map_size = (Params.map_size[0] * Params.map_tilesize,
                              Params.map_size[1] * Params.map_tilesize)

            min_offset = (_display_half[0] - _curr_map_size[0],
                          _display_half[1] - _curr_map_size[1])

            general_offset = (Tools.clip(general_offset[0], min_offset[0], _display_half[0]),
                              Tools.clip(general_offset[1], min_offset[1], _display_half[1]))

            Params.map_current_offset = general_offset

            win.clear_screen()
            win.render_screen()

            has_changed = False

    quit()


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ initialize ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

if __name__ == '__main__':
    main()
