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
#include <string.h>

#include "libraries/pico_graphics/pico_graphics.hpp"
#include "galactic_unicorn.hpp"
#include "pico/bootrom.h"
#include "hardware/structs/rosc.h"

#include "bsp/board.h"
#include "tusb.h"

#include "cdc_uart.h"
#include "get_serial.h"

// UART0 for Picoprobe debug
// UART1 for picoprobe to target device

using namespace pimoroni;

const int WIDTH = 53;
const int HEIGHT = 11;

const int BUFF_SIZE = WIDTH * HEIGHT * 4;
const int MAX_UART_PKT = 64;


uint8_t buf[BUFF_SIZE];

PicoGraphics_PenRGB888 graphics(WIDTH, HEIGHT, &buf);
GalacticUnicorn galactic_unicorn;

int main(void) {

    galactic_unicorn.init();
    galactic_unicorn.set_brightness(0.5);

    graphics.set_pen(0, 0, 0);
    graphics.clear();
    graphics.set_pen(255, 255, 255);
    graphics.set_font("bitmap8");
    graphics.text("Ready", Point(0, 0), 53);
    galactic_unicorn.update(&graphics);

    board_init(); // Wtf?
    usb_serial_init(); // ??
    //cdc_uart_init(); // From cdc_uart.c
    tusb_init(); // Tiny USB?

    uint bytes_total = 0;
    while (1) {
        tud_task(); // tinyusb device task
        uint bytes_recvd = cdc_task(buf + bytes_total, MAX_UART_PKT); // CDC serial task
        bytes_total += bytes_recvd;
        if(bytes_total >= BUFF_SIZE) {
            if (strncmp((const char* )buf, "multiverse:0000", 16) == 0) {
                rosc_hw->ctrl = ROSC_CTRL_ENABLE_VALUE_ENABLE << ROSC_CTRL_ENABLE_LSB;
                reset_usb_boot(0, 0);
                break;
            }
            bytes_total = 0;
            galactic_unicorn.update(&graphics);
        }
    }

    return 0;
}