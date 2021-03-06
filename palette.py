#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  palette.py
#  palette_detect
#

"""
Detect the main colors used in an image.
"""

from __future__ import print_function

import colorsys
import multiprocessing
import sys
import csv
import webcolors
import re
from types import *
from PIL import Image, ImageChops, ImageDraw
from collections import Counter, namedtuple
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cmc
from colormath.color_conversions import convert_color
from operator import itemgetter, mul, attrgetter


from colorific import config
title = input()
fh ='{0}Palette.csv'.format(title)


Color = namedtuple('Color', ['value', 'prominence'])
Palette = namedtuple('Palette', 'colors bgcolor')


def color_stream_st(istream=sys.stdin, save_palette=False, **kwargs):
    """
    Read filenames from the input stream and detect their palette.
    """
    for line in istream:
        filename = line.strip()
        try:
            palette = extract_colors(filename, **kwargs)

        except Exception as e:
            print(filename, e, file=sys.stderr)
            continue

        print_colors(filename, palette)
        if save_palette:
            save_palette_as_image(filename, palette)


def color_stream_mt(istream=sys.stdin, n=config.N_PROCESSES, **kwargs):
    """
    Read filenames from the input stream and detect their palette using
    multiple processes.
    """
    queue = multiprocessing.Queue(1000)
    lock = multiprocessing.Lock()

    pool = [multiprocessing.Process(target=color_process, args=(queue, lock),
            kwargs=kwargs) for i in range(n)]
    for p in pool:
        p.start()

    block = []
    for line in istream:
        block.append(line.strip())
        if len(block) == config.BLOCK_SIZE:
            queue.put(block)
            block = []
    if block:
        queue.put(block)

    for i in range(n):
        queue.put(config.SENTINEL)

    for p in pool:
        p.join()


def color_process(queue, lock):
    "Receive filenames and get the colors from their images."
    while True:
        block = queue.get()
        if block == config.SENTINEL:
            break

        for filename in block:
            try:
                palette = extract_colors(filename)
            except:  # TODO: it's too broad exception.
                continue
            lock.acquire()
            try:
                print_colors(filename, palette)
            finally:
                lock.release()


def distance(c1, c2):
    """
    Calculate the visual distance between the two colors.
    """
    return delta_e_cmc(
        convert_color(sRGBColor(*c1, is_upscaled=True), LabColor),
        convert_color(sRGBColor(*c2, is_upscaled=True), LabColor)
    )


def rgb_to_hex(color):
    return '#%.02x%.02x%.02x' % color


def hex_to_rgb(color):
    assert color.startswith('#') and len(color) == 7
    return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)


def extract_colors(
        filename_or_img, min_saturation=config.MIN_SATURATION,
        min_distance=config.MIN_DISTANCE, max_colors=config.MAX_COLORS,
        min_prominence=config.MIN_PROMINENCE, n_quantized=config.N_QUANTIZED):
    """
    Determine what the major colors are in the given image.
    """
    if Image.isImageType(filename_or_img):
        im = filename_or_img
    else:
        im = Image.open(filename_or_img)

    # get point color count
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im = autocrop(im, config.WHITE)  # assume white box
    im = im.convert(
        'P', palette=Image.ADAPTIVE, colors=n_quantized).convert('RGB')
    data = im.getdata()
    dist = Counter(data)
    n_pixels = mul(*im.size)

    # aggregate colors
    to_canonical = {config.WHITE: config.WHITE, config.BLACK: config.BLACK}
    aggregated = Counter({config.WHITE: 0, config.BLACK: 0})
    sorted_cols = sorted(dist.items(), key=itemgetter(1), reverse=True)
    for c, n in sorted_cols:
        if c in aggregated:
            # exact match!
            aggregated[c] += n
        else:
            d, nearest = min((distance(c, alt), alt) for alt in aggregated)
            if d < min_distance:
                # nearby match
                aggregated[nearest] += n
                to_canonical[c] = nearest
            else:
                # no nearby match
                aggregated[c] = n
                to_canonical[c] = c

    # order by prominence
    colors = sorted(
        [Color(c, n / float(n_pixels)) for c, n in aggregated.items()],
        key=attrgetter('prominence'), reverse=True)

    colors, bg_color = detect_background(im, colors, to_canonical)

    # keep any color which meets the minimum saturation
    sat_colors = [c for c in colors if meets_min_saturation(c, min_saturation)]
    if bg_color and not meets_min_saturation(bg_color, min_saturation):
        bg_color = None
    if sat_colors:
        colors = sat_colors
    else:
        # keep at least one color
        colors = colors[:1]

    # keep any color within 10% of the majority color
    color_list = []
    color_count = 0

    for color in colors:
        if color.prominence >= colors[0].prominence * min_prominence:
            color_list.append(color)
            color_count += 1

        if color_count >= max_colors:
            break

    return Palette(color_list, bg_color)


def norm_color(c):
    r, g, b = c
    return r / 255.0, g / 255.0, b / 255.0


def detect_background(im, colors, to_canonical):
    # more then half the image means background
    if colors[0].prominence >= config.BACKGROUND_PROMINENCE:
        return colors[1:], colors[0]

    # work out the background color
    w, h = im.size
    points = [
        (0, 0), (0, h / 2), (0, h - 1), (w / 2, h - 1), (w - 1, h - 1),
        (w - 1, h / 2), (w - 1, 0), (w / 2, 0)]
    edge_dist = Counter(im.getpixel(p) for p in points)

    (majority_col, majority_count), = edge_dist.most_common(1)
    if majority_count >= 3:
        # we have a background color
        canonical_bg = to_canonical[majority_col]
        bg_color, = [c for c in colors if c.value == canonical_bg]
        colors = [c for c in colors if c.value != canonical_bg]
    else:
        # no background color
        bg_color = None

    return colors, bg_color
#####insert color name####
##########################################################
##########################################################
##########################################################
##########################################################
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


#### My inserted code##
# def color_average(closest_name):
#     r=0
#     o=0
#     y=0
#     b=0
#     i=0
#     v=0
#     if closest_name == 'red':
#         r+=1
#     elif closest_name == 'pink':
#     elif closest_name == 'yellow':
#     elif closest_name == 'orange':
#     elif closest_name == 'green':
#     elif closest_name == 'blue':
#     elif closest_name == 'purple':
#     elif closest_name == 'white':
#     elif closest_name == 'black':
#     elif closest_name == 'gray'or 'grey':


##########################################################
##########################################################
##########################################################
##########################################################

def print_colors(filename, palette):
    colors = '%s\t%s\t%s' % (
        filename, ','.join(rgb_to_hex(c.value) for c in palette.colors),
        palette.bgcolor and rgb_to_hex(palette.bgcolor.value) or '')
    with open(fh,'a') as f1:
        writer=csv.writer(f1)
        row = []
        row.append(filename)
        for c in palette.colors:
            r = c.value[0]
            g = c.value[1]
            b = c.value[2]
            #row.append(c.value)
            requested_colour = (r,g,b) # create rgb tuple
            actual_name, closest_name = get_colour_name(requested_colour) ##get color name
            row. append(closest_name)
        #     # color emotion association
            if closest_name == 'red'or closest_name =='lightsalmon'or closest_name =='darksalmon'or closest_name =='lighcoral'or closest_name =='indianred'or closest_name =='crimson'or closest_name =='firebrick' or closest_name =='darkred':
                emotion = ['anger', 'passion', 'love']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'pink' or closest_name =='lightpink' or closest_name =='hotpink' or closest_name =='deeppink' or closest_name =='palevioletred'or closest_name =='mediumvioletred':
                emotion = ['love', 'playful', 'happy']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'yellow'or closest_name =='lightyellow'or closest_name =='lemonchiffon'or closest_name =='lightgoldenrodyellow'or closest_name =='papayawhip' or closest_name =='moccasin' or closest_name =='peachpuff' or closest_name =='palegoldenrod' or closest_name =='khaki'or closest_name =='darkkhaki':
                emotion = ['happy', 'anxious', 'danger']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name =='orange' or closest_name =='tomato' or closest_name =='orangered' or closest_name =='gold' or closest_name =='darkorange':
                emotion = ['happy', 'content', 'social']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'green'or closest_name =='lawngreen' or closest_name =='chartreuse' or closest_name =='limegreen' or closest_name =='lime' or closest_name =='forestgreen'or closest_name =='darkgreen' or closest_name =='greenyellow' or closest_name =='yellowgreen' or closest_name =='springgreen'or closest_name =='mediumspringgreen' or closest_name =='lightgreen' or closest_name =='palegreen' or closest_name =='darkseagreen' or closest_name =='mediumseagreen' or closest_name=='seagreen' or closest_name =='olive' or closest_name =='darkolivegreen' or closest_name =='olivedrab':
                emotion = ['jealous', 'content', 'danger']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name =='blue'or closest_name =='powderblue' or closest_name =='lightblue' or closest_name =='lightskyblue' or closest_name =='skyblue'or closest_name =='deepskyblue'or closest_name =='lightsteelblue'or closest_name =='dodgerblue' or closest_name =='cornflowerblue' or closest_name =='steelblue' or closest_name =='royalblue' or closest_name =='mediumblue' or closest_name =='darkblue' or closest_name =='navy' or closest_name =='midnightblue' or closest_name=='mediumslateblue' or closest_name =='slateblue' or closest_name =='darkslateblue' or closest_name =='lightcyan' or closest_name =='cyan' or closest_name =='aqua' or closest_name =='aquamarine' or closest_name =='mediumaquamarine' or closest_name =='paleturquoise' or closest_name =='turquoise' or closest_name =='mediumturquoise'or closest_name =='darkturquoise' or closest_name =='lightseagreen' or closest_name =='cadetblue' or closest_name =='darkcyan' or closest_name=='teal':
                emotion = ['sad', 'content', 'ominous']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name =='purple'or closest_name =='lavender'or closest_name =='thistle' or closest_name =='plum'or closest_name =='violet'or closest_name =='orchid' or closest_name =='fuchsia' or closest_name =='magenta' or closest_name =='mediumorchid'or closest_name =='mediumpurple' or closest_name =='blueviolet'or closest_name =='darkviolet'or closest_name =='darkorchid' or closest_name =='darkmagenta' or closest_name =='indigo':
                emotion = ['erotic', 'mysterious', 'ominous']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'white'or closest_name =='snow' or closest_name =='honeydew'or closest_name =='mintcream' or closest_name =='azure' or closest_name =='aliceblue' or closest_name =='ghostwhite'or closest_name =='whitesmoke' or closest_name =='seashell' or closest_name =='beige' or closest_name =='oldlace'or closest_name =='floralwhite' or closest_name =='ivory'or closest_name =='antiquewhite' or closest_name =='linen'or closest_name =='lavenderblush' or closest_name=='mistyrose':
                emotion = ['pure', 'content', 'simple']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'black':
                emotion = ['danger', 'sad', 'anxious']
                # row. append(emotion[0])
                # row. append(emotion[1])
                # row. append(emotion[2])
                # break
            elif closest_name == 'gray'or closest_name =='grey' or closest_name =='gainsboro' or closest_name =='lightgrey' or closest_name =='lightgray' or closest_name =='silver' or closest_name =='darkgray'or closest_name =='darkgrey' or closest_name =='dimgray'or closest_name =='dimgrey' or closest_name =='lightslategray' or closest_name =='lightslategrey'or closest_name =='slategray' or closest_name =='slategrey' or closest_name =='darkslategray' or closest_name =='darkslategrey':
                emotion = ['mourning', 'detached', 'content']
                # row.append(emotion[0])
                # row.append(emotion[1])
                # row.append(emotion[2])
                # break
            elif closest_name == 'brown' or closest_name =='cornsilk' or closest_name =='blanchedalmond' or closest_name =='bisque' or closest_name =='navajowhite' or closest_name =='wheat' or closest_name =='burlywood'or closest_name =='tan' or closest_name =='rosybrown'or closest_name =='sandybrown' or closest_name =='goldenrod' or closest_name =='peru'or closest_name =='chocolate' or closest_name =='saddlebrown' or closest_name =='sienna' or closest_name =='maroon':
                emotion = ['simple', 'content']
                # row.append(emotion[0])
                # row.append(emotion[1])
                # break
            else:
                row.append("Not Available")
                #break
            row.append(emotion)
        writer.writerow(row)
    # print(colors)
    sys.stdout.flush()


def save_palette_as_image(filename, palette):
    "Save palette as a PNG with labeled, colored blocks"
    output_filename = '%s_palette.png' % filename[:filename.rfind('.')]
    size = (80 * len(palette.colors), 80)
    im = Image.new('RGB', size)
    draw = ImageDraw.Draw(im)
    for i, c in enumerate(palette.colors):
        v = colorsys.rgb_to_hsv(*norm_color(c.value))[2]
        (x1, y1) = (i * 80, 0)
        (x2, y2) = ((i + 1) * 80 - 1, 79)
        draw.rectangle([(x1, y1), (x2, y2)], fill=c.value)
        if v < 0.6:
            # white with shadow
            draw.text((x1 + 4, y1 + 4), rgb_to_hex(c.value), (90, 90, 90))
            draw.text((x1 + 3, y1 + 3), rgb_to_hex(c.value))
        else:
            # dark with bright "shadow"
            draw.text((x1 + 4, y1 + 4), rgb_to_hex(c.value), (230, 230, 230))
            draw.text((x1 + 3, y1 + 3), rgb_to_hex(c.value), (0, 0, 0))
    im.save(output_filename, "PNG")


def meets_min_saturation(c, threshold):
    return colorsys.rgb_to_hsv(*norm_color(c.value))[1] > threshold


def autocrop(im, bgcolor):
    "Crop away a border of the given background color."
    if im.mode != "RGB":
        im = im.convert("RGB")
    bg = Image.new("RGB", im.size, bgcolor)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

    return im  # no contents, don't crop to nothing
