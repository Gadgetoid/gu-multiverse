#pragma once

#include "libraries/pico_graphics/pico_graphics.hpp"
#include "cosmic_unicorn.hpp"

namespace display {
    const int WIDTH = 32;
    const int HEIGHT = 32;
    const int BUFFER_SIZE = WIDTH * HEIGHT * 4;

    void init();
    void update();
    void info(std::string_view text);
    extern uint8_t buffer[BUFFER_SIZE];
}