# -*- coding: utf-8 -*-

from Window import *
from Params import *
from Minder import *
from Tools import *
import time
import datetime


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define mainloop ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #
# looooooooooooooooooooooooooooooooooooooooooooooooooooooool #
def main():

    win = Window()
    win.create_map()
    Params.calc_min_tilesize(win.get_display_size())

    show_screen = True
    has_changed = True
    mapped_tiles_x = 0
    mapped_tiles_y = 0
    map_offset_x = 0
    map_offset_y = 0
    arrow_move_speed = 10
    drag_flag = False

    last_time = 0
    frame_counter = 0

    while win:
        win.update()

        user_input = Minder.have_a_look()

        if user_input == 'QUIT':
            Window.destroy()
            win = None
            exit()

        if user_input == 'TOGGLE_FULLSCREEN':
            win.toggle_fullscreen()
            has_changed = True

        if user_input == 'DRAW':
            show_screen = True
            has_changed = True

        if user_input == 'CLEAR':
            win.clear_screen()
            show_screen = False

        if user_input == 'RESET':
            win.reset_map()
            win.create_map()
            has_changed = True

        if user_input[0:4] == 'ZOOM':
            old_tilesize = Params.map_tilesize
            if user_input == 'ZOOM_IN':
                Params.increase_tilesize()
            elif user_input == 'ZOOM_OUT':
                Params.decrease_tilesize()
            new_tilesize = Params.map_tilesize
            if not old_tilesize == new_tilesize:
                old_mapped_tiles_x = Params.map_width - win.get_display_size()[0] / old_tilesize
                old_mapped_tiles_y = Params.map_height - win.get_display_size()[1] / old_tilesize
                new_mapped_tiles_x = Params.map_width - win.get_display_size()[0] / new_tilesize
                new_mapped_tiles_y = Params.map_height - win.get_display_size()[1] / new_tilesize
                centered_offset_x = round((new_mapped_tiles_x - old_mapped_tiles_x) / 2)
                centered_offset_y = round((new_mapped_tiles_y - old_mapped_tiles_y) / 2)
                map_offset_x += centered_offset_x
                map_offset_y += centered_offset_y
            has_changed = True

        if user_input[0:4] == 'MOVE':
            map_offset_x -= arrow_move_speed if user_input == 'MOVE_LEFT' else 0
            map_offset_x += arrow_move_speed if user_input == 'MOVE_RIGHT' else 0
            map_offset_y -= arrow_move_speed if user_input == 'MOVE_UP' else 0
            map_offset_y += arrow_move_speed if user_input == 'MOVE_DOWN' else 0
            win.clear_screen()
            has_changed = True

        if user_input == 'DRAGGING' or drag_flag:
            if drag_flag:
                _movement = Minder.get_mouse_movement()
                map_offset_x -= round(_movement[0] / 3)
                map_offset_y -= round(_movement[1] / 3)
            else:
                drag_flag = True
            has_changed = True

        if user_input == 'DRAGGING_OFF':
            drag_flag = False

        if show_screen and has_changed:
            fov_x = ceil(win.get_display_size()[0] / Params.map_tilesize)
            fov_y = ceil(win.get_display_size()[1] / Params.map_tilesize)

            mapped_tiles_x = Params.map_width - fov_x
            mapped_tiles_y = Params.map_height - fov_y

            map_offset_x = Tools.clip(map_offset_x, 0, mapped_tiles_x)
            map_offset_y = Tools.clip(map_offset_y, 0, mapped_tiles_y)

            win.draw_tileset(fov_x, fov_y, map_offset_x, map_offset_y)

            has_changed = False

        if user_input == 'CAPTURE':
            date = str(datetime.datetime.now())
            filename = (date[2:10] + '_' +
                        date[11:13] + '-' +
                        date[14:16] + '-' +
                        date[17:19] + '_img.jpg')
            win.capture(filename)

        if time.clock() - last_time > 1:
            last_time = time.clock()
            # print(frame_counter)
            frame_counter = 0
        else:
            frame_counter += 1

    quit()


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ initialize ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

if __name__ == '__main__':
    main()
