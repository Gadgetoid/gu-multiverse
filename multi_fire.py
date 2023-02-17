import serial
import numpy
import time
import threading
import random

# Class to represent a single Galactic Unicorn display
# handy place to store the serial port opening and such
class Display:
    # Just in case we get fancy and use RGB565
    BYTES_PER_PIXEL = 4

    def __init__(self, port, w, h, x, y):
        self.fd = port
        self.port = serial.Serial(port, baudrate=230400)
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def write(self, buffer):
        self.port.write(buffer[self.y:self.y+self.h, self.x:self.x+self.w].tobytes())

    def flush(self):
        self.port.flush()

    def __del__(self):
        # Clear the displays to black when the program bails
        self.port.write(numpy.zeros((self.w, self.h, self.BYTES_PER_PIXEL), dtype=numpy.uint8).tobytes())
        self.port.flush()
        self.port.close()


# Array of serial ports and display offsets
# port, width, height, offset x, offset y
displays = [
    Display("/dev/ttyACM0", 53, 11, 0, 0),
    Display("/dev/ttyACM1", 53, 11, 0, 11),
    Display("/dev/ttyACM2", 53, 11, 0, 22),
]

# Full buffer size
WIDTH = 53
HEIGHT = 33 + 4
BYTES_PER_PIXEL = 4

# Fire stuff
FIRE_SPAWNS = 5
DAMPING_FACTOR = 0.98
HEAT = 4.0

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

# Ignore me, test data
def random_noise():
    data = numpy.random.rand(HEIGHT, WIDTH, BYTES_PER_PIXEL)
    data *= 255
    return data.astype(numpy.uint8)

# UPDATE THE FIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEEEEEEEEE
def update():
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
    update()

    # Convert the fire buffer to RGB 888X (uint32 as four bytes)
    buf = heat.clip(0.0, 1.0) * 4
    buf = buf.astype(numpy.uint8)
    buf = PALETTE[buf]

    # Update the displays from the buffer
    for display in displays:
        threading.Thread(target=display.write, args=(buf,)).start()

    # Make sure the frames are all flushed!
    for display in displays:
        display.flush()

    # Just FPS stuff, move along!
    t_end = time.time()
    t_total = t_end - t_start

    sum_total += t_total
    num_frames += 1

    if num_frames == 60:
        print(f"Took {sum_total}s for 60 frames, {num_frames / sum_total:.02f} FPS")
        num_frames = 0
        sum_total = 0