__author__ = 'Federico Tomassetti'

from PIL import Image
from drawing_functions import *

try:
    from worldgen.geo import antialias
except:
    from geo import antialias

from biome import *


def draw_plates(plates, filename):
    WIDTH = len(plates[0])
    HEIGHT = len(plates)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            n = plates[y][x] * 255 / N_PLATES
            pixels[x, y] = (n, n, n, 255)
    img.save(filename)


def draw_land_profile(elevation, sea_level, filename):
    WIDTH = len(elevation[0])
    HEIGHT = len(elevation)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if elevation[y][x] > sea_level:
                pixels[x, y] = (0, 255, 0, 255)
            else:
                pixels[x, y] = (0, 0, 255, 255)
    img.save(filename)


def draw_simple_elevation(data, filename, shadow, width, height):
    COLOR_STEP = 1.5

    def my_color(c):
        if c < 0.5:
            return (0.0, 0.0, 0.25 + 1.5 * c)
        elif c < 1.0:
            return (0.0, 2 * (c - 0.5), 1.0)
        else:
            c -= 1.0;
            if c < 1.0 * COLOR_STEP:
                return (0.0, 0.5 +
                        0.5 * c / COLOR_STEP, 0.0)
            elif (c < 1.5 * COLOR_STEP):
                return (2 * (c - 1.0 * COLOR_STEP) / COLOR_STEP, 1.0, 0.0)
            elif (c < 2.0 * COLOR_STEP):
                return (1.0, 1.0 - (c - 1.5 * COLOR_STEP) / COLOR_STEP, 0)
            elif (c < 3.0 * COLOR_STEP):
                return (1.0 - 0.5 * (c - 2.0 *
                                     COLOR_STEP) / COLOR_STEP,
                        0.5 - 0.25 * (c - 2.0 *
                                      COLOR_STEP) / COLOR_STEP, 0)
            elif (c < 5.0 * COLOR_STEP):
                return (0.5 - 0.125 * (c - 3.0 *
                                       COLOR_STEP) / (2 * COLOR_STEP),
                        0.25 + 0.125 * (c - 3.0 *
                                        COLOR_STEP) / (2 * COLOR_STEP),
                        0.375 * (c - 3.0 *
                                 COLOR_STEP) / (2 * COLOR_STEP))
            elif (c < 8.0 * COLOR_STEP):
                return (0.375 + 0.625 * (c - 5.0 *
                                         COLOR_STEP) / (3 * COLOR_STEP),
                        0.375 + 0.625 * (c - 5.0 *
                                         COLOR_STEP) / (3 * COLOR_STEP),
                        0.375 + 0.625 * (c - 5.0 *
                                         COLOR_STEP) / (3 * COLOR_STEP))
            else:
                c -= 8.0 * COLOR_STEP
                while (c > 2.0 * COLOR_STEP):
                    c -= 2.0 * COLOR_STEP
                return (1, 1 - c / 4.0, 1)

    img = Image.new('RGBA', (width, height))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(height):
        for x in xrange(width):
            e = data[y * width + x]
            if min_elev == None or e < min_elev:
                min_elev = e
            if max_elev == None or e > max_elev:
                max_elev = e
    elev_delta = max_elev - min_elev

    for y in range(0, height):
        for x in range(0, width):
            e = data[y * width + x]
            # c = 255-int(((e-min_elev)*255)/elev_delta)
            #pixels[x,y] = (c,c,c,255)
            r, g, b = my_color(e)
            pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255), 255)
    img.save(filename)


def generate_riversmap(world_path, map_path):
    import pickle

    with open(world_path, 'r') as f:
        w = pickle.load(f)

    # Generate images
    draw_riversmap(w, map_path)


def draw_riversmap(world, filename):
    img = Image.new('RGBA', (world.width, world.height))
    pixels = img.load()

    for y in xrange(world.height):
        for x in xrange(world.width):
            if world.ocean[y][x]:
                pixels[x, y] = sea_color
            else:
                pixels[x, y] = land_color

    draw_riversmap_on_image(world, pixels)

    img.save(filename)


def draw_bw_heightmap(world, filename):
    img = Image.new('RGBA', (world.width, world.height))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(world.height):
        for x in xrange(world.width):
            e = world.elevation['data'][y][x]
            if min_elev == None or e < min_elev:
                min_elev = e
            if max_elev == None or e > max_elev:
                max_elev = e
    elev_delta = max_elev - min_elev

    for y in xrange(world.height):
        for x in xrange(world.width):
            e = world.elevation['data'][y][x]
            c = int(((e - min_elev) * 255) / elev_delta)
            pixels[x, y] = (c, c, c, 255)
    img.save(filename)


def draw_bw_heightmap_for_a_biome(world, filename, biome):
    img = Image.new('RGBA', (world.width, world.height))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(world.height):
        for x in xrange(world.width):
            e = world.elevation['data'][y][x]
            if min_elev == None or e < min_elev:
                min_elev = e
            if max_elev == None or e > max_elev:
                max_elev = e
    elev_delta = max_elev - min_elev

    for y in xrange(world.height):
        for x in xrange(world.width):
            e = world.elevation['data'][y][x]
            c = int(((e - min_elev) * 255) / elev_delta)
            if not world.biome[y][x] == biome:
                a = 0
            else:
                a = 255
            pixels[x, y] = (c, c, c, a)
    img.save(filename)


def draw_elevation(world, filename, shadow=True):
    WIDTH = world.width
    HEIGHT = world.height

    data = world.elevation['data']
    ocean = world.ocean
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(HEIGHT):
        for x in xrange(WIDTH):
            if not ocean[y][x]:
                e = data[y][x]
                if min_elev == None or e < min_elev:
                    min_elev = e
                if max_elev == None or e > max_elev:
                    max_elev = e
    elev_delta = max_elev - min_elev

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            else:
                e = data[y][x]
                c = 255 - int(((e - min_elev) * 255) / elev_delta)
                if shadow and y > 2 and x > 2:
                    if data[y - 1][x - 1] > e:
                        c -= 15
                    if data[y - 2][x - 2] > e and data[y - 2][x - 2] > data[y - 1][x - 1]:
                        c -= 10
                    if data[y - 3][x - 3] > e and data[y - 3][x - 3] > data[y - 1][x - 1] and data[y - 3][x - 3] > \
                            data[y - 2][x - 2]:
                        c -= 5
                    if c < 0:
                        c = 0
                pixels[x, y] = (c, c, c, 255)
    img.save(filename)


def draw_irrigation(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    data = world.irrigation
    ocean = world.ocean
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(HEIGHT):
        for x in xrange(WIDTH):
            if not ocean[y][x]:
                e = data[y][x]
                if min_elev == None or e < min_elev:
                    min_elev = e
                if max_elev == None or e > max_elev:
                    max_elev = e
    elev_delta = max_elev - min_elev

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            else:
                e = data[y][x]
                c = int(((e - min_elev) * 255) / elev_delta)
                pixels[x, y] = (0, 0, c, 255)
    img.save(filename)


def draw_humidity(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    ocean = world.ocean
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()

    min_elev = None
    max_elev = None
    for y in xrange(HEIGHT):
        for x in xrange(WIDTH):
            if not ocean[y][x]:
                e = world.humidity['data'][y][x]
                if min_elev == None or e < min_elev:
                    min_elev = e
                if max_elev == None or e > max_elev:
                    max_elev = e
    elev_middle = world.humidity['quantiles']['50']
    elev_delta_plus = max_elev - elev_middle
    elev_delta_minus = elev_middle - min_elev

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            else:
                e = world.humidity['data'][y][x]
                if e < elev_middle:
                    c = int(((elev_middle - e) * 255) / elev_delta_minus)
                    pixels[x, y] = (c, 0, 0, 255)
                else:
                    c = int(((e - elev_middle) * 255) / elev_delta_plus)
                    pixels[x, y] = (0, c, 0, 255)

    img.save(filename)


def draw_watermap(world, filename, th):
    WIDTH = world.width
    HEIGHT = world.height

    ocean = world.ocean
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()

    # min_elev = None
    # max_elev = None
    # for y in xrange(HEIGHT):
    # for x in xrange(WIDTH):
    #       if not ocean[y][x]:
    #           e = _watermap[y][x]**1.5
    #           if min_elev==None or e<min_elev:
    #               min_elev=e
    #           if max_elev==None or e>max_elev:
    #               max_elev=e              
    # elev_delta = max_elev-min_elev    
    # if elev_delta<1:
    #   elev_delta=1

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            else:
                e = world.watermap[y][x]
                if e > th:
                    c = 255
                else:
                    c = 0
                    #c = int(((e-min_elev)*255)/elev_delta)
                pixels[x, y] = (c, 0, 0, 255)
    img.save(filename)


def draw_basic_elevation(elevation, filename):
    WIDTH = len(elevation[0])
    HEIGHT = len(elevation)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            e = int(elevation[y][x] * 255 / MAX_ELEV)
            if e < 0:
                e = 0
            if e > 255:
                e = 255
            pixels[x, y] = (e, e, e, 255)
    img.save(filename)


def draw_land(elevation, ocean_map, hill_level, mountain_level, filename):
    WIDTH = len(elevation[0])
    HEIGHT = len(elevation)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean_map[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            elif elevation[y][x] > mountain_level:
                pixels[x, y] = (255, 255, 255, 255)
            elif elevation[y][x] > hill_level:
                pixels[x, y] = (30, 140, 30, 255)
            else:
                pixels[x, y] = (0, 230, 0, 255)

    img.save(filename)


def draw_ocean(ocean, filename):
    WIDTH = len(ocean[0])
    HEIGHT = len(ocean)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 255, 255)
            else:
                pixels[x, y] = (0, 255, 255, 255)
    img.save(filename)


def draw_temp(temp, filename):
    WIDTH = len(temp[0])
    HEIGHT = len(temp)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            c = int(temp[y][x] * 255)
            pixels[x, y] = (c, 0, 0, 255)
    img.save(filename)


def draw_precipitation(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    data = world.precipitation['data']
    ocean = world.ocean
    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if ocean[y][x]:
                pixels[x, y] = (0, 0, 0, 255)
            else:
                c = int((data[y][x] + 1.0) * 127.5)
                pixels[x, y] = (0, 0, c, 255)
    img.save(filename)


def draw_sea(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    img = Image.new('RGBA', (WIDTH, HEIGHT))

    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if world.is_land((x, y)):
                pixels[x, y] = (255, 255, 255, 255)
            else:
                c = int(world.sea_depth[y][x] * 200 + 50)
                pixels[x, y] = (0, 0, 255 - c, 255)
    img.save(filename)


class Counter:
    def __init__(self):
        self.c = {}

    def count(self, what):
        if not what in self.c:
            self.c[what] = 0
        self.c[what] += 1

    def printself(self):
        for w in self.c.keys():
            print("%s : %i" % (w, self.c[w]))


biome_colors = {
    'iceland': (208, 241, 245),
    'jungle': (54, 240, 17),
    'tundra': (180, 120, 130),
    'ocean': (23, 94, 145),
    'forest': (10, 89, 15),
    'grassland': (69, 133, 73),
    'steppe': (90, 117, 92),
    'sand desert': (207, 204, 58),
    'rock desert': (94, 93, 25),
    'swamp': (255, 0, 0),
    'glacier': (255, 255, 255),
    'alpine': (100, 70, 5),
    'savanna': (200, 140, 20)
}


def draw_world(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    img = Image.new('RGBA', (WIDTH, HEIGHT))

    counter = Counter()

    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if world.is_land((x, y)):
                biome = world.biome_at((x, y))
                pixels[x, y] = biome_colors[biome]
            else:
                c = int(world.sea_depth[y][x] * 200 + 50)
                pixels[x, y] = (0, 0, 255 - c, 255)

    counter.printself()
    img.save(filename)


def draw_temperature_levels(world, filename):
    WIDTH = world.width
    HEIGHT = world.height

    img = Image.new('RGBA', (WIDTH, HEIGHT))

    pixels = img.load()
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            if world.is_land((x, y)):
                e = world.elevation['data'][y][x]
                if world.is_temperature_very_low((x, y)):
                    pixels[x, y] = (0, 0, 255, 255)
                elif world.is_temperature_low((x, y)):
                    pixels[x, y] = (80, 120, 255, 255)
                elif world.is_temperature_medium((x, y)):
                    pixels[x, y] = (180, 255, 180, 255)
                elif world.is_temperature_high((x, y)):
                    pixels[x, y] = (255, 0, 0, 255)
            else:
                pixels[x, y] = (0, 0, 0, 255)
    img.save(filename)


biome_colors = {
    'iceland': (208, 241, 245),
    'jungle': (54, 240, 17),
    'tundra': (180, 120, 130),
    'ocean': (23, 94, 145),
    'forest': (10, 89, 15),
    'grassland': (69, 133, 73),
    'steppe': (90, 117, 92),
    'sand desert': (207, 204, 58),
    'rock desert': (94, 93, 25),
    'swamp': (255, 0, 0),
    'glacier': (255, 255, 255),
    'alpine': (100, 70, 5),
    'savanna': (200, 140, 20)
}


def draw_biome(temp, filename):
    WIDTH = len(temp[0])
    HEIGHT = len(temp)

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    pixels = img.load()

    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            v = temp[y][x]
            pixels[x, y] = biome_colors[v]
    img.save(filename)  