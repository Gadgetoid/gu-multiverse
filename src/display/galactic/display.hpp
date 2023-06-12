#pragma once

#include "libraries/pico_graphics/pico_graphics.hpp"
#include "galactic_unicorn.hpp"

namespace display {
    const int WIDTH = 53;
    const int HEIGHT = 11;
    const int BUFFER_SIZE = WIDTH * HEIGHT * 4;

    void init();
    void update();
    void info(std::string_view text);
    extern uint8_t buffer[BUFFER_SIZE];
}