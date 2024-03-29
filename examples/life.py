import numpy
import time
import random
import colorsys
from multiverse import Multiverse, Display

display = Multiverse(
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614104037D9F30-if00", 53, 11, 0,  0),
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661410403422430-if00", 53, 11, 0, 11),
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661410403868C2C-if00", 53, 11, 0, 22),
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614103E7301237-if00", 53, 11, 0, 33),
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614C311B425233-if00", 53, 11, 0, 44),
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614103E786A622-if00", 53, 11, 0, 55)
)

display.setup(use_threads=True)

# Full buffer size
WIDTH = 53
HEIGHT = len(display.displays) * 11
BYTES_PER_PIXEL = 4

INITIAL_LIFE = 200 * len(display.displays)         # Number of live cells to seed
GENERATION_TIME = 0.1     # MS between generations
MINIMUM_LIFE = 10         # Auto reseed when only this many alive cells remain
SMOOTHED = True           # Enable for a more organic if somewhat unsettling feel

DECAY = 0.95              # Rate at which smoothing effect decays, higher number = more persistent, 1.0 = no decay
TENACITY = 32             # Rate at which smoothing effect increases

HSV_OFFSET = 0.3


def palette(offset=0.3):
    for c in range(256):
        yield c
        yield 0
        yield c // 2
        yield 0
    #for h in range(256):
    #    for c in colorsys.hsv_to_rgb(offset + h / 1024.0, 1.0, h / 255.0):
    #        yield int(c * 255)
    #    yield 0 # padding byte


# Palette conversion, this is actually pretty nifty
PALETTE = numpy.fromiter(palette(HSV_OFFSET), dtype=numpy.uint8).reshape((256, 4))


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
    buf = numpy.clip(duration.round(0), 0, 255).astype(numpy.uint8)
    buf = PALETTE[buf]

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
