#!/usr/bin/env python3

import os
import re
import io
import png
import sys
import math

import argparse

BITS = 3

colormap = [
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

def expand(v):
    """Split a 24 bit integer into 3 bytes

    >>> expand(0xff2001)
    (255, 32, 1)
    """
    return ( ((v)>>16 & 0xFF), ((v)>>8 & 0xFF), ((v)>>0 & 0xFF) )


def format_offset(offset):
    """Return a right-aligned hexadecimal representation of offset.

    >>> format_offset(128)
    '    0080'
    >>> format_offset(3735928559)
    'deadbeef'
    """
    return '%5x%03x' % (offset >> 12, offset & 0xFFF)

def generate_image(width, height, foffset, fhandle):
    global BITS
    pixel_data = [[0 for i in range(width * BITS)] for j in range(height)]

    for y in range(0, height):
        for x in range(0, width):

            fpos = (y * width) + x + foffset
            fhandle.seek(fpos)
            val = fhandle.read(1)

            if not val:
                pval = 0
            else:
                pval = ord(val)

            if pval > 255:
                pval = 255
            elif pval < 0:
                pval = 0

            pixel_data[y][(x * BITS) + 0] = ((colormap[pval])>>16 & 0xFF)   # R
            pixel_data[y][(x * BITS) + 1] = ((colormap[pval])>>8 & 0xFF)    # G
            pixel_data[y][(x * BITS) + 2] = ((colormap[pval])>>0 & 0xFF)    # B

    return pixel_data

def rescale_image(pbuffer, scale):
    global BITS

    width = int((len(pbuffer[0]) / BITS) * scale)
    height = int(len(pbuffer) * scale)
    rescaled_buffer = [[0 for i in range(width * BITS)] for j in range(height)]

    for y in range(0, height):
        for x in range(0, width):
            rescaled_buffer[y][(x * BITS) + 0] = pbuffer[y // scale][((x // scale) * BITS) + 0]  # R
            rescaled_buffer[y][(x * BITS) + 1] = pbuffer[y // scale][((x // scale) * BITS) + 1]   # G
            rescaled_buffer[y][(x * BITS) + 2] = pbuffer[y // scale][((x // scale) * BITS) + 2]   # B

    return rescaled_buffer

def parse_range(s):
    """Return (start, end) parsed from "[start]-[end]" or "<start>+<size>".

    >>> parse_range('0-')
    (0, None)
    >>> pixd.parse_range('3-10')
    (3, 10)
    pixd.parse_range('3+10')
    (3, 13)
    """
    match = re.match(r'(\d*)([-+])(\d*)', s)
    if not match:
        raise ValueError("Not a valid range: '%s'" % s)

    start, end = 0
    first, delim, second = match.groups()

    if delim == '-':
        start = int(first) if first else 0
        end = int(second) if second else None
    else:
        if not start:
            raise ValueError("Start unspecified in range: '%s'" %s)
        start = int(first)
        if not end:
            raise ValueError("End unspecified in range: '%s'" %s)
        end = start + int(second)

    if end is not None and end < start:
        raise ValueError("End %i was less than start %i" % (end, start))

    return (start, end)

def parse_args():
    parser = argparse.ArgumentParser(prog='vizme')
    parser.add_argument('-s', '--scale', dest='scale', default=1, type=int)
    parser.add_argument('-r', '--range', dest='range', default=(0, None), type=parse_range)
    parser.add_argument('-w', '--width', dest='width', default=64, type=int)
    parser.add_argument('-o', '--out', default=None, type=str,
                        help="Output filename, defaults to <original filename>.png")

    parser.add_argument('file', nargs='?', type=str, default=None,
                        help="File to convert (data can also be supplied on stdin)")

    args = parser.parse_args()
    if args.out == None:
        args.out = os.path.join(os.getcwd(), args.file + ".png")

    return args

def main():
    options = parse_args()
    options.file = open(options.file, 'rb')
    flength = len(options.file.read())

    calc_width = options.width if flength >= options.width else flength
    calc_height = 0
    if calc_width < options.width:
        calc_height = 1
    elif options.range[1] and options.range[1] <= flength:
        calc_height = int(math.ceil(float(options.range[1] - options.range[0]) / float(calc_width)))
    else:
        calc_height = int(math.ceil(float(flength) / float(calc_width)))

    img_buffer = generate_image(
            width=calc_width,
            height=calc_height,
            foffset=options.range[0],
            fhandle=options.file,
        )

    if options.scale > 1:
        img_buffer = rescale_image(
                            pbuffer=img_buffer,
                            scale=options.scale
                        )



    file_handle = open(options.out, 'wb')
    png_w = png.Writer(width=calc_width * options.scale, height=calc_height * options.scale, greyscale=False)
    png_w.write(file_handle, img_buffer)
    file_handle.close()

    options.file.close()