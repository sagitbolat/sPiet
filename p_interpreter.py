from p_parser import *
from p_stack import *
import operator as op


color_rows = [[ 0,  1,  2,  3,  4,  5],
              [ 6,  7,  8,  9, 10, 11],
              [12, 13, 14, 15, 16, 17]]

def find_hue_change(color1, color2):
    """finds hue steps from color1 to color2"""
    def normalize_val(val):
        if val <= 5:
            return val
        else:
            return normalize_val(val - 6)
    c1, c2 = normalize_val(color1), normalize_val(color2)
    if color1 == 18 or color1 == 19 or color1 == 20: return 0
    if c1 < c2:
        return c2 - c1
    elif c1 > c2:
        return 6 - c1 - c2
    else:
        return 0

def find_shade_change(color1, color2):
    def normalize_val(val):
        if val <= 5:
            return 0
        elif val <= 11:
            return 1
        elif val <= 17:
            return 2
    c1, c2 = normalize_val(color1), normalize_val(color2)
    if color1 == 18 or color1 == 19 or color1 == 20 or c1 is None or c2 is None: return 0
    if c1 < c2:
        return c2 - c1
    elif c1 > c2:
        return 3 - c1 - c2
    else:
        return 0
    


def init(initial_coord, stack, img, palette):
    current_codels = get_adjacent_codels(initial_coord, img, palette)
    stack.current_col = coord_to_color_value(initial_coord, img, palette)
    stack.current_val = len(current_codels)
    while stack.current_col != 20:
        next_coord = loop_iteration(current_codels, stack, img, palette)
        current_codels = get_adjacent_codels(next_coord, img, palette)

def loop_iteration(codels, stack, img, palette):
    next_coord = find_adjacent_block_coord(codels, img, stack._pointer)
    next_codels = get_adjacent_codels(next_coord, img, palette)


    prev_color = coord_to_color_value(codels[0], img, palette)
    next_color = coord_to_color_value(next_coord, img, palette)
    resolve_operation(stack, img, prev_color, next_color, codels, next_codels)
    #print(stack.current_col)
    stack.current_val = len(next_codels)
    stack.current_col = next_color
    return next_coord

def resolve_operation(stack, img, color1, color2, codels1, codels2):
    if color2 == 19:
        stack._pointer.attemp_to_unstuck()
    if color1 == 18:
        #do nothing
        return
    if color2 == 20:
        #do nothing
        return
    else:
        hue, shade = find_hue_change(color1, color2), find_shade_change(color1, color2)
        if hue == 0:
            if shade == 1: stack.push(stack.current_val)
            elif shade == 2: stack.pop()
            else: return
        elif hue == 1:
            if shade == 0: stack.resolve_operator(op.add)
            elif shade == 1: stack.resolve_operator(op.sub)
            else: stack.resolve_operator(op.mul)
        elif hue == 2:
            if shade == 0: stack.resolve_operator(op.floordiv)
            elif shade == 1: stack.resolve_operator(op.mod)
            else: stack._not()
        elif hue == 3:
            if shade == 0: stack.greater()
            elif shade == 1: stack.pointer()
            else: stack.switch()
        elif hue == 4:
            if shade == 0: stack.duplicate()
            elif shade == 1: stack.roll()
            else: stack.input_num()
        else:
            if shade == 0: stack.input_char()
            elif shade == 1: stack.output_num()
            else: stack.output_char()

"""
pointer starts on the first coord.
while current codel is not gray:
    pointer saves value of current codel
    pointer moves forward and executes command appropiately
"""
stack = Stack()

img_file = '10.png'
img = read_img(img_file)
palette = read_img('palette.png')
init([0,0], stack, img, palette)

# print(palette[0])
# for color in palette[0]:
#     print(rgb_to_value(color, palette))
# print((palette[0][0] == img[0][0]).all())


