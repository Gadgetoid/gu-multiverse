#pragma once

#include "libraries/pico_graphics/pico_graphics.hpp"
#include "galactic_unicorn.hpp"

namespace display {
    const int WIDTH = 53;
    const int HEIGHT = 11;
    const size_t BUFFER_SIZE = WIDTH * HEIGHT * 4;

    void init();
    void update();
    void info(std::string_view text);
    void play_audio(uint8_t *audio_buffer, size_t len);
    void play_note(uint8_t channel, uint16_t freq, uint8_t waveform, uint16_t a, uint16_t d, uint16_t s, uint16_t r, uint8_t phase);
    extern uint8_t buffer[BUFFER_SIZE];
}