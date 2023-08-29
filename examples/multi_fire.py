import numpy
import time
import random
import sys
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

if len(sys.argv) == 2:
    if sys.argv[1] == "bl":
        display.bootloader()
    if sys.argv[1] == "rst":
        display.reset()
    sys.exit(0)

# Full buffer size
WIDTH = 160
HEIGHT = 32
BYTES_PER_PIXEL = 4

# Fire stuff
FIRE_SPAWNS = 5
DAMPING_FACTOR = 0.97
HEAT = 10.0

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


# Palette conversion, this is actually pretty nifty
PALETTE = numpy.array([
    Color(0, 0, 0),
    Color(20, 20, 20),
    Color(0, 30, 180),
    Color(0, 160, 220),
    Color(180, 255, 255)
], dtype=numpy.uint32)

# FIIIREREEEEEEE
heat = numpy.zeros((HEIGHT + 5, WIDTH), dtype=numpy.float32)
buf = numpy.zeros((HEIGHT, WIDTH), dtype=numpy.uint32)
last_update = 0

# UPDATE THE FIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEEEEEEEEE
def update(fps):
    global last_update

    if time.time() - last_update < (1.0 / fps):
        return
    
    last_update = time.time()

    # Clear the bottom two rows (off screen)
    heat[HEIGHT + 4][:] = 0.0
    heat[HEIGHT + 3][:] = 0.0

    # Add random fire spawns
    for c in range(FIRE_SPAWNS):
        x = random.randint(0, WIDTH - 4) + 2
        heat[HEIGHT + 4][x - 1:x + 1] = HEAT / 2.0
        heat[HEIGHT + 3][x - 1:x + 1] = HEAT

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
    heatbuf = heat.clip(0.0, 1.0) * 4
    heatbuf = heatbuf[:HEIGHT]
    heatbuf = heatbuf.astype(numpy.uint8)
    heatbuf = PALETTE[heatbuf]
    
    #buf = numpy.concatenate((buf[::2, :], buf[1::2, :]), axis=1)

    buf[::,::2] = heatbuf[:int(HEIGHT / 2)].reshape(32, 80)
    buf[::,1::2] = heatbuf[int(HEIGHT / 2):].reshape(32, 80)

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
