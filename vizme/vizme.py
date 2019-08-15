#!/usr/bin/env python3

import os
import png
import math
import argparse
from colors import *

from vizme.utils import *
from vizme.palettes import palettes

def parse_args():
    parser = argparse.ArgumentParser(prog='vizme')

    parser.add_argument('-t', '--terminal', dest="terminal_mode", action="store_true",
                        help="Sets output to be terminal (colored) ANSI.")
    parser.add_argument('-w', '--width', dest='width', default=16, type=int,
                                help='Output columns width')
    parser.add_argument('-s', '--scale', dest='scale', default=1, type=int,
                        help='Scales the output pixels (2 means 2 times the amount of columns/rows for the same data)')
    parser.add_argument('-p', '--palette', dest='palette', choices=palettes.keys(), default='pixd',
                        help='Sets the palette to use for output')

    parser.add_argument('INPUT', nargs='?', type=str, default="/dev/stdin",
                        help="Data to convert (can be a file, don't specify for stdin)")
    parser.add_argument('OUTPUT', nargs='?', type=str, default="/dev/stdout",
                        help="Where to write output to (can be a file, don't specify for stdout)")

    args = parser.parse_args()
    args.palette = palettes[args.palette]

    return args

def generate_image(fhandle, requested_width):
    pixel_data = []
    end_of_stream = False

    while not end_of_stream:
        rdata = fhandle.read(requested_width)
        pdata_line = [d for d in rdata]
        pdata_line_len = len(pdata_line)
        if pdata_line_len > 0:
            if pdata_line_len < requested_width:
                pdata_line = pdata_line + ((requested_width - pdata_line_len) * [0])
                end_of_stream = True

            pixel_data.append(pdata_line)
        else:
            end_of_stream = True

    return pixel_data

def rescale_image(pbuffer, scale):
    width = int(len(pbuffer[0]) * scale)
    height = int(len(pbuffer) * scale)
    rescaled_buffer = [[0 for i in range(width)] for j in range(height)]

    for y in range(0, height):
        for x in range(0, width):
            rescaled_buffer[y][x] = pbuffer[y // scale][x // scale]

    return rescaled_buffer

def main():
    options = parse_args()

    options.INPUT = open(options.INPUT, 'rb')
    img_buffer = generate_image(
            requested_width=options.width,
            fhandle=options.INPUT,
        )
    options.INPUT.close()

    buf_width = len(img_buffer[0])
    buf_height = len(img_buffer)

    img_buffer = rescale_image(
        pbuffer=img_buffer,
        scale=options.scale
    )

    options.OUTPUT = open(options.OUTPUT, 'wb')

    if options.terminal_mode:
        def _get_tcolor(val):
            pval = options.palette[val]
            return '#%02x%02x%02x' % (pval[0], pval[1], pval[2])

        for i in range(len(img_buffer)):
            for elem in img_buffer[i]:
                options.OUTPUT.write(bytes(color(u"\u2588", fg=_get_tcolor(elem)), encoding='utf-8'))
            options.OUTPUT.write(bytes('\n', encoding='utf-8'))
    else:
        png_w = png.Writer(
            width=buf_width * options.scale,
            height=buf_height * options.scale,
            palette=options.palette,
        )

        png_w.write(options.OUTPUT, img_buffer)

    options.OUTPUT.close()

