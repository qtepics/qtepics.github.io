""" adl2colour.py
    Singleton module class to manage colours
"""

from collections import namedtuple

RGB = namedtuple("RGB", ["r", "g", "b"])
RGBA = namedtuple("RGBA", ["r", "g", "b", "a"])


def image(x):
    if isinstance(x, RGBA):
        return "rgba(%d, %d, %d, %d)" % (x.r, x.g, x.b, x.a)

    if isinstance(x, RGB):
        return "rgb(%d, %d, %d)" % (x.r, x.g, x.b)

    return str(x)


# ------------------------------------------------------------------------------
#
def set_colour_map(colour_list):
    """
    """
    global _colour_map

    colour_set = []
    for hex_text in colour_list:
        colour = eval('0x' + hex_text)
        r = (colour >> 16) & 255
        g = (colour >> 8) & 255
        b = (colour >> 0) & 255
        item = RGB(r, g, b)
        colour_set.append(item)

    _colour_map = tuple(colour_set)


# ------------------------------------------------------------------------------
#
def clear_colour_map():
    """
    """
    global _colour_map
    colour_map = ()


# ------------------------------------------------------------------------------
#
def get_rgb(number):
    """ Returns an RGB tuple  (red, green, blue)
    """
    if number >= 0 and number < len(_colour_map):
        result = _colour_map[number]
    else:
        result = RGB(255, 225, 225)

    return result


# ------------------------------------------------------------------------------
#
def get_style(background, foreground=None):
    """
    :param background: back ground colour - an RGB/A or int
    :param foreground: fore ground colour - an RGB/A or int or None.
    :return: style sheet
    """

    if isinstance(background, (RGB, RGBA)):
        # background is alread an RGB/A objecxt
        #
        b = background
    else:
        # Hypothosize background is a colour number.
        #
        b = get_rgb(background)

    if foreground is None:
        # Select white or black font based on background colour
        # Note: 299 + 587 + 114 = 1000
        #
        wc = ((299 * b.r) + (587 * b.g) + (114 * b.b)) // 1000

        # Dark or bright background colour ?
        #
        is_dark = (wc < 124)
        if is_dark:
            f = RGB(255, 255, 255)    # white font
        else:
            f = RGB(0, 0, 0)          # black font

    elif isinstance(foreground, (RGB, RGBA)):
        # foreground is alread an RGB/A objecxt
        #
        f = foreground

    else:
        f = get_rgb(foreground)

    template = "QWidget { background-color: %s; color: %s; }"
    result = template % (image(b), image(f))
    return result


_colour_map = ()

# end
