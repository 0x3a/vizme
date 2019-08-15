"""
    Taken from https://lospec.com/palette-list/dawnbringers-8-color

    This is more an example how to dynamically generate palettes from an even number of colors in the palette.
"""

from colour import Color
palette = [
    '#000000', '#55415f', '#646964', '#d77355', '#508cd7', '#64b964', '#e6c86e', '#dcf5ff'
]
palette = [Color(c) for c in palette]
steps =int(256 / len(palette))

stepped_colors = []
for i in range(0, len(palette) - 1):
    stepped_colors += palette[i].range_to(palette[i + 1] , steps)
palette = [((int(i.get_red() * 255), int(i.get_green() * 255), int(i.get_blue() * 255))) for i in stepped_colors]

name = "dawnbringer"