# -*- coding: utf-8 -*-

from abc import ABC
import pygame

#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #


class Tools(ABC):

    @staticmethod
    def clip(val, min_, max_):
        return min_ if val < min_ else max_ if val > max_ else val

    @staticmethod
    def dict_size_2d(_dict) -> tuple:
        x, y = 0, 0
        while not y:
            try:
                __ = _dict[x, y]
                x += 1
            except KeyError:
                y = int(len(_dict) / x)
        return x, y
