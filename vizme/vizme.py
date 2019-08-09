#!/usr/bin/env python3

import os
import png
import sys
import math
import argparse


def expand(v):
    """Split a 24 bit integer into 3 bytes

    >>> expand(0xff2001)
    (255, 32, 1)
    """
    return ( ((v)>>16 & 0xFF), ((v)>>8 & 0xFF), ((v)>>0 & 0xFF) )


# Our palette, converted for pypng
palette = [
    0x000000, 0x560000, 0x640000, 0x750000, 0x870000, 0x9b0000, 0xb00000, 0xc60000, 0xdd0000, 0xf50000, 0xff0f0f, 0xff2828, 0xff4343, 0xff5e5e, 0xff7979, 0xfe9595,
    0x4c1600, 0x561900, 0x641e00, 0x752300, 0x872800, 0x9b2e00, 0xb03400, 0xc63b00, 0xdd4200, 0xf54900, 0xff570f, 0xff6928, 0xff7b43, 0xff8e5e, 0xffa179, 0xfeb595,
    0x4c3900, 0x564000, 0x644b00, 0x755700, 0x876500, 0x9b7400, 0xb08400, 0xc69400, 0xdda600, 0xf5b800, 0xffc30f, 0xffc928, 0xffd043, 0xffd65e, 0xffdd79, 0xfee495,
    0x4c4c00, 0x565600, 0x646400, 0x757500, 0x878700, 0x9b9b00, 0xb0b000, 0xc6c600, 0xdddd00, 0xf5f500, 0xffff0f, 0xffff28, 0xffff43, 0xffff5e, 0xffff79, 0xfffe95,
    0x324c00, 0x395600, 0x426400, 0x4e7500, 0x5a8700, 0x679b00, 0x75b000, 0x84c600, 0x93dd00, 0xa3f500, 0xafff0f, 0xb7ff28, 0xc0ff43, 0xc9ff5e, 0xd2ff79, 0xdbfe95,
    0x1f4c00, 0x235600, 0x296400, 0x307500, 0x388700, 0x409b00, 0x49b000, 0x52c600, 0x5cdd00, 0x66f500, 0x73ff0f, 0x82ff28, 0x91ff43, 0xa1ff5e, 0xb1ff79, 0xc1fe95,
    0x004c00, 0x005600, 0x006400, 0x007500, 0x008700, 0x009b00, 0x00b000, 0x00c600, 0x00dd00, 0x00f500, 0x0fff0f, 0x28ff28, 0x43ff43, 0x5eff5e, 0x79ff79, 0x95fe95,
    0x004c19, 0x00561c, 0x006421, 0x007527, 0x00872d, 0x009b33, 0x00b03a, 0x00c642, 0x00dd49, 0x00f551, 0x0fff5f, 0x28ff70, 0x43ff81, 0x5eff93, 0x79ffa6, 0x95feb8,
    0x004c4c, 0x005656, 0x006464, 0x007575, 0x008787, 0x009b9b, 0x00b0b0, 0x00c6c6, 0x00dddd, 0x00f5f5, 0x0ffffe, 0x28fffe, 0x43fffe, 0x5efffe, 0x79ffff, 0x95fffe,
    0x00394c, 0x004056, 0x004b64, 0x005775, 0x006587, 0x00749b, 0x0084b0, 0x0094c6, 0x00a6dd, 0x00b8f5, 0x0fc3ff, 0x28c9ff, 0x43d0ff, 0x5ed6ff, 0x79ddff, 0x95e4fe,
    0x00264c, 0x002b56, 0x003264, 0x003a75, 0x004387, 0x004d9b, 0x0058b0, 0x0063c6, 0x006edd, 0x007af5, 0x0f87ff, 0x2893ff, 0x43a1ff, 0x5eaeff, 0x79bcff, 0x95cafe,
    0x00134c, 0x001556, 0x001964, 0x001d75, 0x002187, 0x00269b, 0x002cb0, 0x0031c6, 0x0037dd, 0x003df5, 0x0f4bff, 0x285eff, 0x4372ff, 0x5e86ff, 0x799aff, 0x95b0fe,
    0x19004c, 0x1c0056, 0x210064, 0x270075, 0x2d0087, 0x33009b, 0x3a00b0, 0x4200c6, 0x4900dd, 0x5100f5, 0x5f0fff, 0x7028ff, 0x8143ff, 0x935eff, 0xa679ff, 0xb895fe,
    0x33004c, 0x390056, 0x420064, 0x4e0075, 0x5a0087, 0x67009b, 0x7500b0, 0x8400c6, 0x9300dd, 0xa300f5, 0xaf0fff, 0xb728ff, 0xc043ff, 0xc95eff, 0xd279ff, 0xdb95fe,
    0x4c004c, 0x560056, 0x640064, 0x750075, 0x870087, 0x9b009b, 0xb000b0, 0xc600c6, 0xdd00dd, 0xf500f5, 0xfe0fff, 0xfe28ff, 0xfe43ff, 0xfe5eff, 0xfe79ff, 0xfe95fe,
    0x4c0032, 0x560039, 0x640042, 0x75004e, 0x87005a, 0x9b0067, 0xb00075, 0xc60084, 0xdd0093, 0xf500a3, 0xff0faf, 0xff28b7, 0xff43c0, 0xff5ec9, 0xff79d2, 0xffffff,

]

clamp = lambda value, minv, maxv: max(min(value, maxv), minv)
palette = [expand(color) for color in palette]


def generate_image(width, height, fhandle):
    pixel_data = [[0 for i in range(width)] for j in range(height)]

    for y in range(0, height):
        for x in range(0, width):

            fpos = (y * width) + x
            fhandle.seek(fpos)
            val = fhandle.read(1)
            pixel_data[y][x] = int.from_bytes(val, byteorder='big')

    return pixel_data

def rescale_image(pbuffer, scale):
    width = int(len(pbuffer[0]) * scale)
    height = int(len(pbuffer) * scale)
    rescaled_buffer = [[0 for i in range(width)] for j in range(height)]

    for y in range(0, height):
        for x in range(0, width):
            rescaled_buffer[y][x] = pbuffer[y // scale][x // scale]

    return rescaled_buffer

def parse_args():
    parser = argparse.ArgumentParser(prog='vizme')

    parser.add_argument('-w', '--width', dest='width', default=16, type=int,
                                help='Output width (png: pixels, terminal:characters)')
    parser.add_argument('FILE', nargs='?', type=str, default=None,
                        help="File to convert (data can also be supplied on stdin)")

    parser.add_argument('-o', '--output', dest='output', choices=['png', 'terminal'], default='png',
                        help='Output type (defaults to terminal)')
    parser.add_argument('-s', '--scale', dest='scale', default=1, type=int,
                        help='Scales the output PNG')

    args = parser.parse_args()
    if args.output == 'png':
        fname = args.FILE
        if fname == None:
            args.FILE = sys.stdin
            fname = 'stream'
        else:
            args.FILE = open(fname, 'rb')

        args.output_fname = os.path.join(os.getcwd(), fname + ".png")

    return args

def main():
    options = parse_args()
    flength = len(options.FILE.read())

    print('length:', str(flength))

    calc_width = options.width  if flength >= options.width else flength
    calc_height = int(math.ceil(float(flength) / float(calc_width)))

    print('height:', calc_height)
    print('width:', calc_width)
    print('scale:', options.scale)

    img_buffer = generate_image(
            width=calc_width,
            height=calc_height,
            fhandle=options.FILE,
        )
    options.FILE.close()

    if options.output == 'png':
        if options.scale > 1:
            img_buffer = rescale_image(
                                pbuffer=img_buffer,
                                scale=options.scale
                            )

        file_handle = open(options.output_fname, 'wb')
        png_w = png.Writer(
            width=calc_width * options.scale,
            height=calc_height * options.scale,
            palette=palette
            #greyscale=True,
        )

        png_w.write(file_handle, img_buffer)
        file_handle.close()
