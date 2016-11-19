# -*- coding: utf-8 -*-

from abc import ABC
from pygame import Color
import colorsys
from math import ceil


#  _________________________________________________________ #
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ define file class ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ #

class Tools(ABC):

    @staticmethod
    def clip(val, min_, max_):
        return min_ if val < min_ else max_ if val > max_ else val

    @staticmethod
    def get_color(_elevation, _stepping, _waterlvl, _grasslvl):
        s = 60
        if _elevation < _waterlvl:
            h = 220
            v = 20 + (_elevation * (80 / _waterlvl))
        else:
            if _elevation < _grasslvl:
                h = 120
                v = 40 + (_elevation - _waterlvl) * (60 / (_grasslvl - _waterlvl))
            else:
                h = 60
                v = 60 - (_elevation - _grasslvl) * (50 / (_stepping - _grasslvl))
        rgb = Tools.hsv_to_rgb(h, s, v)
        return Color(rgb[0], rgb[1], rgb[2])

    @staticmethod
    def hsv_to_rgb(h, s, v):
        v = Tools.clip(v, 0, 100)
        rgb = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
