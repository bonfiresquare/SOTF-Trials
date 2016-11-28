# -*- coding: utf-8 -*-

from abc import ABC
import pygame
from Window import *


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Minder(ABC):
    _mouse_move = ()
    _keymap = {pygame.K_ESCAPE: 'QUIT',
               pygame.K_LEFT:   'MOVE_LEFT',
               pygame.K_RIGHT:  'MOVE_RIGHT',
               pygame.K_UP:     'MOVE_UP',
               pygame.K_DOWN:   'MOVE_DOWN',
               pygame.K_F2:     'DRAW',
               pygame.K_F3:     'CLEAR',
               pygame.K_F5:     'RESET',
               pygame.K_F8:     'SAVE',
               pygame.K_F9:     'LOAD',
               pygame.K_F10:    'TOGGLE_AA',
               pygame.K_F11:    'TOGGLE_FULL',
               pygame.K_F12:    'CAPTURE'}
    @staticmethod
    def have_a_look():
        output = ''
        for e in pygame.event.get():
            # print(event)
            if e.type == pygame.QUIT:
                output = 'QUIT'
            elif e.type == pygame.KEYDOWN:
                output = Minder._keymap[e.key]
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pygame.mouse.set_cursor(*Window.get_cursor_data('lmb'))
                elif e.button == 3:
                    pygame.mouse.set_cursor(*Window.get_cursor_data('rmb'))
                elif e.button == 4:
                    output = 'ZOOM_IN'
                elif e.button == 5:
                    output = 'ZOOM_OUT'
            elif e.type == pygame.MOUSEMOTION:
                Minder._mouse_move = pygame.mouse.get_rel()
                if pygame.mouse.get_pressed()[2]:
                    pygame.mouse.set_cursor(*Window.get_cursor_data('drg'))
                    output = 'DRAG_ON'
            elif e.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(*Window.get_cursor_data('std'))
                if e.button == 3:
                    output = 'DRAG_OFF'
        return output

    @staticmethod
    def get_mouse_movement():
        _out = Minder._mouse_move
        Minder._mouse_move = (0, 0)
        return _out
