import time
import random
import sys
import math
import numpy
from multiverse import Multiverse, Display

display = Multiverse(
    Display("/dev/serial/by-id/usb-Pimoroni_Multiverse_E661AC8863389C27-if00", 16, 16, 0, 0, rotate=90)
)

display.setup(False)

notes = [440, 880, 400]

while True:
    display.play_note(0, notes[0], attack=300)
    display.play_note(1, notes[1], attack=10, waveform=Display.WAVEFORM_SAW)
    notes += [notes.pop(0)]
    time.sleep(0.5)
