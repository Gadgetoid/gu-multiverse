/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <string_view>

#include "display.hpp"
#include "pico/bootrom.h"
#include "hardware/structs/rosc.h"
#include "hardware/watchdog.h"
#include "pico/timeout_helper.h"

#include "bsp/board.h"
#include "tusb.h"

#include "cdc_uart.h"
#include "get_serial.h"

// UART0 for Picoprobe debug
// UART1 for picoprobe to target device

using namespace pimoroni;

const size_t COMMAND_LEN = 4;
uint8_t command_buffer[COMMAND_LEN];
std::string_view command((const char *)command_buffer, COMMAND_LEN);

bool cdc_wait_for(std::string_view data, uint timeout_ms=1000) {
    timeout_state ts;
    absolute_time_t until = delayed_by_ms(get_absolute_time(), timeout_ms);
    check_timeout_fn check_timeout = init_single_timeout_until(&ts, until);

    for(auto expected_char : data) {
        char got_char;
        while(1){
            tud_task();
            if (cdc_task((uint8_t *)&got_char, 1) == 1) break;
            if(check_timeout(&ts)) return false;
        }
        if (got_char != expected_char) return false;
    }
    return true;
}

size_t cdc_get_bytes(const uint8_t *buffer, const size_t len, const uint timeout_ms=1000) {
    memset((void *)buffer, len, 0);

    uint8_t *p = (uint8_t *)buffer;

    timeout_state ts;
    absolute_time_t until = delayed_by_ms(get_absolute_time(), timeout_ms);
    check_timeout_fn check_timeout = init_single_timeout_until(&ts, until);

    size_t bytes_remaining = len;
    while (bytes_remaining && !check_timeout(&ts)) {
        tud_task(); // tinyusb device task
        size_t bytes_read = cdc_task(p, std::min(bytes_remaining, MAX_UART_PACKET));
        bytes_remaining -= bytes_read;
        p += bytes_read;
    }
    return len - bytes_remaining;
}

int main(void) {
    board_init(); // Wtf?
    usb_serial_init(); // ??
    //cdc_uart_init(); // From cdc_uart.c
    tusb_init(); // Tiny USB?

    display::init();

    while (1) {
        tud_task();

        if(!cdc_wait_for("multiverse:")) {
            //display::info("mto");
            continue; // Couldn't get 16 bytes of command
        }

        if(cdc_get_bytes(command_buffer, COMMAND_LEN) != COMMAND_LEN) {
            //display::info("cto");
            continue;
        }

        if(command == "data") {
            if (cdc_get_bytes(display::buffer, display::BUFFER_SIZE) == display::BUFFER_SIZE) {
                display::update();
            }
            continue;
        }

        if(command == "_rst") {
            display::info("RST");
            sleep_ms(500);
            save_and_disable_interrupts();
            rosc_hw->ctrl = ROSC_CTRL_ENABLE_VALUE_ENABLE << ROSC_CTRL_ENABLE_LSB;
            watchdog_reboot(0, 0, 0);
            continue;
        }

        if(command == "_usb") {
            display::info("USB");
            sleep_ms(500);
            save_and_disable_interrupts();
            rosc_hw->ctrl = ROSC_CTRL_ENABLE_VALUE_ENABLE << ROSC_CTRL_ENABLE_LSB;
            reset_usb_boot(0, 0);
            continue;
        }
    }

    return 0;
}