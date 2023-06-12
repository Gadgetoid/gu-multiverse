import numpy
# import scipy
import time
import random
from multiverse import Multiverse, Display
from colorsys import hsv_to_rgb

display = Multiverse(
    #       Serial Port,       W,  H,  X,  Y
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661AC8863389C27-if00", 16, 16, 0, 0),
)

display.setup()

# Full buffer size
WIDTH = 16
HEIGHT = 16
BYTES_PER_PIXEL = 4

# Fire stuff
FIRE_SPAWNS = 5
DAMPING_FACTOR = 0.98
matrix = 4.0

# Palette conversion, this is actually pretty nifty
PALETTE = numpy.array([
    [0, 0, 0, 0],
    [0, 20, 0, 0],
    [0, 30, 0, 0],
    [0, 160, 0, 0],
    [0, 255, 0, 0],
    [0, 255, 30, 30],
    [0, 255, 100, 100],
    [0, 255, 200, 200],
    [0, 255, 245, 245],
    [0, 255, 255, 255],
    [0, 255, 255, 255]
], dtype=numpy.uint8)


matrix = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float32)
last_update = 0


def update(fps):
    global last_update

    if time.time() - last_update < (1.0 / fps):
        return
    
    last_update = time.time()

    matrix[:] *= 0.65

    for _ in range(10):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT // 2)
        matrix[y][x] = random.randint(128, 255) / 255.0

    # Propagate downwards
    old = matrix * 0.5
    matrix[:] = numpy.roll(matrix, 1, axis=0)
    matrix[:] += old


# Framerate counters, don't mind these
sum_total = 0
num_frames = 0


while True:
    t_start = time.time()

    # Update the fire
    update(60)

    # Convert the fire buffer to RGB 888X (uint32 as four bytes)
    buf = matrix
    # buf = scipy.ndimage.rotate(buf, (t_start * 45) % 360, reshape=False)
    buf = buf.clip(0.0, 1.0) * (len(PALETTE) - 1)
    buf = buf.astype(numpy.uint8)
    buf = PALETTE[buf]

    #            b, g, r,   _
    h = time.time() / 10.0
    r, g, b = [int(c * 255) for c in hsv_to_rgb(h, 1.0, 1.0)]
    for y in range(16):
        for x in range(16):
            buf[y][x] = (b, g, r, 0)

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
