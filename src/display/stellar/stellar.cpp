#include "display.hpp"

using namespace pimoroni;


namespace display {
    uint8_t buffer[BUFFER_SIZE];
    PicoGraphics_PenRGB888 graphics(WIDTH, HEIGHT, &buffer);
    StellarUnicorn stellar_unicorn;

    void init() {
        stellar_unicorn.init();
        stellar_unicorn.set_brightness(0.5);

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
        stellar_unicorn.update(&graphics);
    }

    void play_note(uint8_t channel, uint16_t freq, uint8_t waveform, uint16_t a, uint16_t d, uint16_t s, uint16_t r, uint8_t phase) {
        stellar_unicorn.play_synth();
        AudioChannel &ch = stellar_unicorn.synth_channel(channel);
        ch.waveforms = waveform;
        ch.frequency = freq;
        ch.attack_ms = a;
        ch.decay_ms = d;
        ch.sustain = s;
        ch.release_ms = r;
        switch((ADSRPhase)phase) {
            case ADSRPhase::ATTACK:
                ch.trigger_attack();
                break;
            case ADSRPhase::DECAY:
                ch.trigger_decay();
                break;
            case ADSRPhase::SUSTAIN:
                ch.trigger_sustain();
                break;
            case ADSRPhase::RELEASE:
                ch.trigger_release();
                break;
        }
    }

    void play_audio(uint8_t *audio_buffer, size_t len) {
        stellar_unicorn.play_sample(audio_buffer, len);
    }
}