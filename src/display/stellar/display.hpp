#pragma once

#include "libraries/pico_graphics/pico_graphics.hpp"
#include "stellar_unicorn.hpp"

namespace display {
    const int WIDTH = 16;
    const int HEIGHT = 16;
    const int BUFFER_SIZE = WIDTH * HEIGHT * 4;

    void init();
    void update();
    void info(std::string_view text);
    extern uint8_t buffer[BUFFER_SIZE];
}