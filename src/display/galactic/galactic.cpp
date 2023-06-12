#include "display.hpp"

using namespace pimoroni;

namespace display {
    uint8_t buffer[BUFFER_SIZE];
    PicoGraphics_PenRGB888 graphics(WIDTH, HEIGHT, &buffer);
    GalacticUnicorn galactic_unicorn;

    void init() {
        galactic_unicorn.init();
        galactic_unicorn.set_brightness(0.5);

        info("rdy");
    }

    void info(std::string_view text) {
        graphics.set_pen(0, 0, 0);
        graphics.clear();
        graphics.set_pen(255, 255, 255);
        graphics.set_font("bitmap5");
        graphics.text(text, Point(0, 0), WIDTH, 1);
        update();
    }

    void update() {
        galactic_unicorn.update(&graphics);
    }
}