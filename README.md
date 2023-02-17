# Galactic Unicorn: Multiverse

A firmware and Python ... software ... for driving multiple Galactic Unicorn displays as a single display from a host computer.

## UDev Rules (or, avoiding your displays getting all messed-up like)

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