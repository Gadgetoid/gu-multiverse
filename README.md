# Galactic Unicorn: Multiverse

A firmware and Python library/examples for driving multiple Galactic Unicorn displays as a single display from a host computer.

## Using Multiverse

Flash `galactic-multiverse.uf2` to each Galactic Unicorn you want to use.

Follow the udev guide below to give each a unique alias, use `/dev/serial/by-id` or hope that the `/dev/ttyACMx` nodes assigned automatically don't mess up your layout.

### Running Examples

From the examples directory, run:

```
PYTHONPATH=../lib python3 multi_fire.py
```

You can install the multiverse lib to avoid having to specify `PYTHONPATH`.

### Getting Started

Set up your displays like so:

```python
from multiverse import Multiverse, Display

display = Multiverse(
    #       Serial Port,       W,  H,  X,  Y
    Display("/dev/Fire-Alice", 53, 11, 0, 0),  # /dev/ttyACMx, udev rule alias or /dev/serial/by-id/usb-Pimoroni_Multiverse_XXXXXXXXXXXXXXXX-if00
    Display("/dev/Fire-James", 53, 11, 0, 11),
    Display("/dev/Fire-Susan", 53, 11, 0, 22),
)

display.setup()
```

To update the displays call `display.update(buffer)`.

It expects a 3d numpy array with a 4 byte (32bit) RGBx value for each pixel.

It must be wide enough to accomodate your displays and their offsets.

```python
buffer = numpy.random.rand(HEIGHT, WIDTH, BYTES_PER_PIXEL) * 255
display.update(buffer.astype(numpy.uint8))
```

### Using /dev/serial/by-id

You might need this patch: https://raw.githubusercontent.com/yuwata/systemd/5286da064c97d2ac934cb301066aaa8605a3c8f9/rules.d/60-serial.rules

Each board has a unique name/ID based on its serial number. For example:

```
/dev/serial/by-id/usb-Pimoroni_Multiverse_E6614864D3853334-if00
```

You should see them listed if you run:

```
ls /dev/serial/by-id
```

### UDev Rules (or, avoiding your displays getting all messed-up like)

See `99-fire.rules` for an example.

Each board should have a unique `iSerial`.

Connect your boards, either one at a time or all together and find their unique IDs with:

```
sudo lsusb -v -d0xcafe: | grep iSerial
```

Plug these into `99-fire.rules`, adding additional entries as necessary.

Give your boards friendly names or numbers or whatever makes sense to you.

Copy your rules into `/etc/udev/rules.d/`:

```
sudo cp 99-fire.rules /etc/udev/rules.d/
```

Reload udev's rules:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

And you should see your new friendly names in `/dev`.