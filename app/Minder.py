# -*- coding: utf-8 -*-

from abc import ABC
import pygame
from Window import *


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Minder(ABC):
    _mouse_pos = ()
    _mouse_move = ()

    @staticmethod
    def have_a_look():
        output = ''
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                output = 'QUIT'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_LEFT:
                    output = 'MOVE_LEFT'
                elif event.key == pygame.K_RIGHT:
                    output = 'MOVE_RIGHT'
                elif event.key == pygame.K_UP:
                    output = 'MOVE_UP'
                elif event.key == pygame.K_DOWN:
                    output = 'MOVE_DOWN'
                elif event.key == pygame.K_F2:
                    output = 'RESET'
                elif event.key == pygame.K_F3:
                    output = 'CLEAR'
                elif event.key == pygame.K_F5:
                    output = 'DRAW'
                elif event.key == pygame.K_F11:
                    output = 'TOGGLE_FULLSCREEN'
                elif event.key == pygame.K_F12:
                    output = 'CAPTURE'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mouse.set_cursor(*Window.get_cursor_data('lmb'))
                elif event.button == 3:
                    if not Minder._mouse_pos:
                        # reset possible movements since last mouse_reset after dragging
                        _ = pygame.mouse.get_rel()
                        Minder._mouse_move = (0, 0)

                        Minder._mouse_pos = pygame.mouse.get_pos()
                        pygame.mouse.set_visible(False)
                    output = 'DRAGGING'
                elif event.button == 4:
                    output = 'ZOOM_IN'
                elif event.button == 5:
                    output = 'ZOOM_OUT'
            elif event.type == pygame.MOUSEMOTION:
                Minder._mouse_move = pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(*Window.get_cursor_data('std'))
                if event.button == 3:
                    pygame.mouse.set_visible(True)
                    output = 'DRAGGING_OFF'
        return output

    @staticmethod
    def get_mouse_movement():
        '''
        returns a tuple for the last relative mouse movement
        :returns Tuple:
        '''
        _out = Minder._mouse_move
        Minder._mouse_move = (0, 0)
        return _out

    @staticmethod
    def reset_mouse_position():
        '''
        reset position of the mouse to the dragging start position
        :return:
        '''
        _pos = Minder._mouse_pos
        pygame.mouse.set_pos(*_pos)
        Minder._mouse_pos = ()
