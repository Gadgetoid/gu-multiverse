#include "display.hpp"

using namespace pimoroni;

namespace display {
    uint8_t buffer[BUFFER_SIZE];
    PicoGraphics_PenRGB888 graphics(WIDTH, HEIGHT, &buffer);
    Hub75 hub75(WIDTH, HEIGHT, nullptr, PANEL_GENERIC, false, Hub75::COLOR_ORDER::RGB);

    void __isr dma_complete() {
        hub75.dma_complete();
    }

    void init() {
        hub75.start(dma_complete);

        info("rdy");
    }

    void info(std::string_view text) {
        graphics.set_pen(0, 0, 0);
        graphics.clear();
        graphics.set_pen(255, 255, 255);
        graphics.set_font("bitmap8");
        graphics.text(text, Point(0, 0), WIDTH, 1);
        update();
    }

    void update() {
        hub75.update(&graphics);
    }

    void play_note(uint8_t channel, uint16_t freq, uint8_t waveform, uint16_t a, uint16_t d, uint16_t s, uint16_t r, uint8_t phase) {
        // No audio support on i75
    }

    void play_audio(uint8_t *audio_buffer, size_t len) {
        // No audio support on i75
    }
}