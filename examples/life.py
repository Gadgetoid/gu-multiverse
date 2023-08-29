import numpy
import time
import random
import colorsys
from multiverse import Multiverse, Display

display = Multiverse(
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614104031C5E38-if00", 160, 32, 0,  0),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614104037D9F30-if00", 53, 11, 0,  0),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661410403422430-if00", 53, 11, 0, 11),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661410403868C2C-if00", 53, 11, 0, 22),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614103E7301237-if00", 53, 11, 0, 33),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614C311B425233-if00", 53, 11, 0, 44),
    #Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614103E786A622-if00", 53, 11, 0, 55)
)

display.setup(use_threads=True)

# Full buffer size
WIDTH = 160
HEIGHT = 32
BYTES_PER_PIXEL = 4

INITIAL_LIFE = 200 * 5         # Number of live cells to seed
GENERATION_TIME = 0.1     # MS between generations
MINIMUM_LIFE = 100         # Auto reseed when only this many alive cells remain
SMOOTHED = True           # Enable for a more organic if somewhat unsettling feel

DECAY = 0.95              # Rate at which smoothing effect decays, higher number = more persistent, 1.0 = no decay
TENACITY = 32             # Rate at which smoothing effect increases

HSV_OFFSET = 0.3

GAMMA_10BIT = [
    0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8,
    8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16,
    16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 25,
    26, 27, 29, 30, 31, 33, 34, 35, 37, 38, 40, 41, 43, 44, 46, 47,
    49, 51, 53, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78,
    80, 82, 85, 87, 89, 92, 94, 96, 99, 101, 104, 106, 109, 112, 114, 117,
    120, 122, 125, 128, 131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 161, 164,
    168, 171, 174, 178, 181, 185, 188, 192, 195, 199, 202, 206, 210, 214, 217, 221,
    225, 229, 233, 237, 241, 245, 249, 253, 257, 261, 265, 270, 274, 278, 283, 287,
    291, 296, 300, 305, 309, 314, 319, 323, 328, 333, 338, 343, 347, 352, 357, 362,
    367, 372, 378, 383, 388, 393, 398, 404, 409, 414, 420, 425, 431, 436, 442, 447,
    453, 459, 464, 470, 476, 482, 488, 494, 499, 505, 511, 518, 524, 530, 536, 542,
    548, 555, 561, 568, 574, 580, 587, 593, 600, 607, 613, 620, 627, 633, 640, 647,
    654, 661, 668, 675, 682, 689, 696, 703, 711, 718, 725, 733, 740, 747, 755, 762,
    770, 777, 785, 793, 800, 808, 816, 824, 832, 839, 847, 855, 863, 872, 880, 888,
    896, 904, 912, 921, 929, 938, 946, 954, 963, 972, 980, 989, 997, 1006, 1015, 1023
]


def Color(r, g, b):
    return (GAMMA_10BIT[r] << 20) | (GAMMA_10BIT[g] << 10) | (GAMMA_10BIT[b])


def palette(offset=0.3):
    for c in range(256):
        yield Color(c, 0, c // 2)

    #for h in range(256):
    #    for c in colorsys.hsv_to_rgb(offset + h / 1024.0, 1.0, h / 255.0):
    #        yield int(c * 255)
    #    yield 0 # padding byte


# Palette conversion, this is actually pretty nifty
PALETTE = numpy.fromiter(palette(HSV_OFFSET), dtype=numpy.uint32).reshape((256, 1))


life = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float32)


# UPDATE THE FIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEEEEEEEEE
def update():
    global last_gen

    duration[:] += life * TENACITY
    duration[:] *= DECAY

    if time.time() - last_gen < GENERATION_TIME:
        return

    last_gen = time.time()

    if numpy.sum(life) < MINIMUM_LIFE:
        seed_life()
        return

    # Rollin' rollin' rollin.
    _N = numpy.roll(life, -1, axis=0)
    _NW = numpy.roll(_N, -1, axis=1)
    _NE = numpy.roll(_N, 1, axis=1)
    _S = numpy.roll(life, 1, axis=0)
    _SW = numpy.roll(_S, -1, axis=1)
    _SE = numpy.roll(_S, 1, axis=1)
    _W = numpy.roll(life, -1, axis=1)
    _E = numpy.roll(life, 1, axis=1)

    # Compute the total neighbours for each cell
    neighbours[:] = _N + _NW + _NE + _S + _SW + _SE + _W + _E

    next_generation[:] = life[:]

    # Any cells with exactly three neighbours should always stay alive
    next_generation[:] += neighbours[:] == 3

    # Any alive cells with less than two neighbours should die
    next_generation[:] -= (neighbours[:] < 2) * life

    # Any alive cells with more than three neighbours should die
    next_generation[:] -= (neighbours[:] > 3) * life

    life[:] = numpy.clip(next_generation, 0, 1)


def seed_life():
    global PALETTE

    HSV_OFFSET = random.randint(0, 360) / 360.0

    #PALETTE = numpy.fromiter(palette(HSV_OFFSET), dtype=numpy.uint8).reshape((256, 4))

    for _ in range(INITIAL_LIFE):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        life[y][x] = int(True)  # Avoid: TypeError: 'bool' object isn't iterable



life = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
buf = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint32)
next_generation = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
neighbours = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint8)
duration = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float64)
last_gen = time.time()

# Framerate counters, don't mind these
sum_total = 0
num_frames = 0


seed_life()

while True:
    t_start = time.time()

    # Update the fire
    update()

    # Convert the fire buffer to RGB 888X (uint32 as four bytes)
    temp = numpy.clip(duration.round(0), 0, 255).astype(numpy.uint8)
    temp = PALETTE[temp]

    buf[::,::2] = temp[:int(HEIGHT / 2)].reshape(32, 80)
    buf[::,1::2] = temp[int(HEIGHT / 2):].reshape(32, 80)

    # Update the displays from the buffer
    display.update(buf)

    # Just FPS stuff, move along!
    t_end = time.time()
    t_total = t_end - t_start

    sum_total += t_total
    num_frames += 1

    time.sleep(1.0 / 60)

    if num_frames == 60:
        print(f"Took {sum_total:.04f}s for 60 frames, {num_frames / sum_total:.02f} FPS")
        num_frames = 0
        sum_total = 0
