import numpy as np
from cv2 import cv2 as cv
from p_stack import *

"""Colors:
18 - white
19 - black
20 - gray"""

def read_img(img):
    return cv.imread(img, 1)

def rgb_to_value(rgb, palette):
    for i in range(len(palette[0])):
        if (palette[0][i] == rgb).all():
            return i
    return 18

def get_x(coord):
    "return x coord"
    return coord[0]
def get_y(coord):
    return coord[1]

def is_coord_on_screen(coord, img):
    x = get_x(coord)
    y = get_y(coord)
    if x < 0 or y < 0 or x >= img.shape[1] or y >= img.shape[0]: return False
    else: return True

def coord_to_color_value(coord, img, palette):
    x = get_x(coord) 
    y = get_y(coord)
    rgb = img[y, x]
    return rgb_to_value(rgb, palette)


def coord_neighbors(coord, max_height, max_width):
    neightbors = []
    x = get_x(coord)
    y = get_y(coord)
    if x > 0:
        neightbors.append([x-1, y])
    if y > 0:
        neightbors.append([x, y-1])
    if x < max_width-1:
        neightbors.append([x+1, y])
    if y < max_height-1:
        neightbors.append([x, y+1])
    return neightbors

def get_adjacent_codels(coord, img, palette):
    codels = []
    codels.append(coord)
    color = coord_to_color_value(coord, img, palette)
    height = img.shape[0]
    width = img.shape[1]
    def find_adjacent(coord):
        nonlocal codels
        neightbors = coord_neighbors(coord, height, width)
        for neightbor in neightbors:
            is_same_color = coord_to_color_value(neightbor, img, palette) == color
            if neightbor not in codels and is_same_color:
                codels.append(neightbor)
                find_adjacent(neightbor)
        return None
    find_adjacent(coord)
    return codels


def find_adjacent_block_coord(codels, img, pointer):
    def find_extrema(codels, func, axis):
        return axis(func(codels, key = (lambda coord: axis(coord))))
    def find_all_edge_codels(value, axis):
        """Finds all codels whose [axis] is of [value] and returns them in a list"""
        return [codel for codel in codels if axis(codel) == value]
    pd = pointer.direction
    cd = pointer.chooser
    if pd == 0:
        x = find_extrema(codels, max, get_x)
        y = 0
        edge_codels = find_all_edge_codels(x, get_x)
        if cd: 
            y = find_extrema(edge_codels, min, get_y)
        else:
            y = find_extrema(edge_codels, max, get_y)
        return [x + 1, y]

    elif pd == 1:
        y = find_extrema(codels, max, get_y)
        x = 0
        edge_codels = find_all_edge_codels(y, get_y)
        if cd: 
            x = find_extrema(edge_codels, max, get_x)
        else:
            x = find_extrema(edge_codels, min, get_x)
        return [x, y + 1]

    elif pd == 2:
        x = find_extrema(codels, min, get_x)
        y = 0
        edge_codels = find_all_edge_codels(x, get_x)
        if cd: 
            y = find_extrema(edge_codels, max, get_y)
        else:
            y = find_extrema(edge_codels, min, get_y)
        return [x - 1, y]     
    
    else:
        y = find_extrema(codels, min, get_y)
        x = 0
        edge_codels = find_all_edge_codels(y, get_y)
        if cd: 
            x = find_extrema(edge_codels, min, get_x)
        else:
            x = find_extrema(edge_codels, max, get_x)
        return [x, y - 1]