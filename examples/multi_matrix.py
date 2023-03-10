import numpy
# import scipy
import time
import random
from multiverse import Multiverse, Display

display = Multiverse(
    #       Serial Port,       W,  H,  X,  Y
    Display("/dev/Fire-Alice", 53, 11, 18, 28),
    Display("/dev/Fire-James", 53, 11, 18, 39),
    Display("/dev/Fire-Susan", 53, 11, 18, 51),
)

display.setup()

# Full buffer size
WIDTH = 90
HEIGHT = 90
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


def update():
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
    update()

    # Convert the fire buffer to RGB 888X (uint32 as four bytes)
    buf = matrix
    # buf = scipy.ndimage.rotate(buf, (t_start * 45) % 360, reshape=False)
    buf = buf.clip(0.0, 1.0) * (len(PALETTE) - 1)
    buf = buf.astype(numpy.uint8)
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
