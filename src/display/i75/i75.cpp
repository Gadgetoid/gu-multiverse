#include "display.hpp"
#include <cstdlib>

using namespace pimoroni;

Hub75 *hub75;

void __isr dma_complete() {
    hub75->dma_complete();
}

namespace display {

    uint8_t buffer[BUFFER_SIZE * 2];

    void init() {
        hub75 = new Hub75(WIDTH, HEIGHT, (Pixel *)&buffer);
        hub75->start(dma_complete);
    }

    void info(std::string_view text) {
    }

    void update() {
        hub75->flip();
    }

    void play_note(uint8_t channel, uint16_t freq, uint8_t waveform, uint16_t a, uint16_t d, uint16_t s, uint16_t r, uint8_t phase) {
        // No audio support on i75
    }

    void play_audio(uint8_t *audio_buffer, size_t len) {
        // No audio support on i75
    }
}