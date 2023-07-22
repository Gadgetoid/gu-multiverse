import numpy
import time
import random
import sys
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

if len(sys.argv) == 2:
    if sys.argv[1] == "bl":
        display.bootloader()
    if sys.argv[1] == "rst":
        display.reset()
    sys.exit(0)

# Full buffer size
WIDTH = 53
HEIGHT = len(display.displays) * 11
BYTES_PER_PIXEL = 4

# Fire stuff
FIRE_SPAWNS = 5
DAMPING_FACTOR = 0.97
HEAT = 10.0

# Palette conversion, this is actually pretty nifty
PALETTE = numpy.array([
    [0, 0, 0, 0],
    [20, 20, 20, 0],
    [0, 30, 180, 0],
    [0, 160, 220, 0],
    [180, 255, 255, 0]
], dtype=numpy.uint8)

# FIIIREREEEEEEE
heat = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.float32)
last_update = 0

# UPDATE THE FIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEEEEEEEEE
def update(fps):
    global last_update

    if time.time() - last_update < (1.0 / fps):
        return
    
    last_update = time.time()

    # Clear the bottom two rows (off screen)
    heat[HEIGHT - 1][:] = 0.0
    heat[HEIGHT - 2][:] = 0.0

    # Add random fire spawns
    for c in range(FIRE_SPAWNS):
        x = random.randint(0, WIDTH - 4) + 2
        heat[HEIGHT - 1][x - 1:x + 1] = HEAT / 2.0
        heat[HEIGHT - 2][x - 1:x + 1] = HEAT

    # Propagate the fire upwards
    a = numpy.roll(heat, -1, axis=0)  # y + 1, x
    b = numpy.roll(heat, -2, axis=0)  # y + 2, x
    c = numpy.roll(heat, -1, axis=0)  # y + 1
    d = numpy.roll(c, 1, axis=1)      # y + 1, x + 1
    e = numpy.roll(c, -1, axis=1)     # y + 1, x - 1

    # Average over 5 adjacent pixels and apply damping
    heat[:] += a + b + d + e
    heat[:] *= DAMPING_FACTOR / 5.0


# Framerate counters, don't mind these
sum_total = 0
num_frames = 0


while True:
    t_start = time.time()

    # Update the fire
    update(60)

    # Convert the fire buffer to RGB 888X (uint32 as four bytes)
    buf = heat.clip(0.0, 1.0) * 4
    buf = buf.astype(numpy.uint8)
    buf = PALETTE[buf]

    # Update the displays from the buffer
    display.update(buf)

    # Just FPS stuff, move along!
    t_end = time.time()
    t_total = t_end - t_start

    sum_total += t_total
    num_frames += 1

    if num_frames == 60:
        print(f"Took {sum_total:.04f}s for 60 frames, {num_frames / sum_total:.02f} FPS")
        num_frames = 0
        sum_total = 0
